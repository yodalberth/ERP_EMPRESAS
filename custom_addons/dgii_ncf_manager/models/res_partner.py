from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ncf_required = fields.Boolean(string='Requiere NCF')
    default_ncf_type = fields.Selection([
        ('B01', 'B01'),
        ('B02', 'B02'),
        ('B03', 'B03'),
        ('B04', 'B04'),
        ('E31', 'E31'),
        ('E32', 'E32'),
    ], string='Tipo de NCF Predeterminado')
