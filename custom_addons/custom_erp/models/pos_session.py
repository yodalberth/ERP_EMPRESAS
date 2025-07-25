from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    ncf_required = fields.Boolean(
        string='Add NCF in POS',
        help='Enable NCF field in POS orders.'
    )
