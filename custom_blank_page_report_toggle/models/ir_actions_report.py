from odoo import fields, models

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    enable_blank_page_fix = fields.Boolean(string="Enable Blank Page Padding")
