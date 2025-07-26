from odoo import fields, models


# Extiende el diario contable para definir el uso de NCF
class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # Indica si el diario debe generar NCF
    usar_ncf = fields.Boolean(string='Usar NCF')
    # Tipo de NCF que utilizará por defecto este diario
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
