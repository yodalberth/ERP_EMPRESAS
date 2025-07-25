from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    usar_ncf = fields.Boolean(string='Usar NCF')
    default_ncf_type = fields.Selection(
        selection=[
            ('B01', 'B01'),
            ('B02', 'B02'),
            ('B03', 'B03'),
            ('B04', 'B04'),
            ('E31', 'E31'),
            ('E32', 'E32'),
        ],
        string='Tipo de NCF'
    )
