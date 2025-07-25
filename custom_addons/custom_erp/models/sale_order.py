from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ncf_required = fields.Boolean(
        string='Add NCF',
        help='Check if this order requires a NCF reference.'
    )
