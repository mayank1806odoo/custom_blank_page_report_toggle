from odoo import models
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO

class ReportBlankPageMixin(models.AbstractModel):
    _inherit = 'ir.actions.report'

    def _post_pdf_processing(self, pdf_content):
        input_pdf = PdfFileReader(BytesIO(pdf_content))
        output_pdf = PdfFileWriter()

        for page_num in range(input_pdf.getNumPages()):
            output_pdf.addPage(input_pdf.getPage(page_num))

        if input_pdf.getNumPages() % 2 != 0:
            output_pdf.addBlankPage()

        output_stream = BytesIO()
        output_pdf.write(output_stream)
        return output_stream.getvalue()

    def _render_qweb_pdf(self, report_name=None, docids=None, data=None):
        pdf_content, content_type = super()._render_qweb_pdf(report_name, docids, data)

        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        if not report.enable_blank_page_fix:
            return pdf_content, content_type

        if isinstance(docids, list) and len(docids) > 1:
            final_pdf = PdfFileWriter()
            for doc_id in docids:
                single_pdf, _ = super()._render_qweb_pdf(report_name, [doc_id], data)
                processed_pdf = self._post_pdf_processing(single_pdf)
                reader = PdfFileReader(BytesIO(processed_pdf))
                for page_num in range(reader.getNumPages()):
                    final_pdf.addPage(reader.getPage(page_num))

            stream = BytesIO()
            final_pdf.write(stream)
            return stream.getvalue(), content_type
        else:
            return self._post_pdf_processing(pdf_content), content_type
