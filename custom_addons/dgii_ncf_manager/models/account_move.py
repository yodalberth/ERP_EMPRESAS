from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        move = super().create(vals)
        # Asignar NCF al crear la factura si el diario lo requiere
        if move.move_type == 'out_invoice' and move.journal_id.usar_ncf:
            ncf_type = move.journal_id.default_ncf_type
            ncf_range = self.env['ncf.range'].search([
                ('ncf_type', '=', ncf_type),
                ('state', '=', 'active')
            ], order='sequence_start', limit=1)
            if not ncf_range:
                raise ValidationError(
                    _('No existe un rango de NCF disponible para el tipo %s.') % ncf_type)
            ncf = ncf_range.assign_ncf()
            if not ncf:
                raise ValidationError(_('El rango de NCF está agotado.'))
            move.ncf_number = ncf
        return move

    def action_post(self):
        # Validar que la factura tenga un NCF antes de publicarla
        for move in self:
            if move.journal_id.usar_ncf:
                if not move.ncf_number:
                    raise ValidationError(_('La factura requiere un NCF válido.'))
        return super().action_post()
