from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    ncf_number = fields.Char(
        string='NCF',
        help='Fiscal receipt number.'
    )
