from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        move = super().create(vals)
        if move.move_type == 'out_invoice' and move.journal_id.usar_ncf:
            ncf_type = move.journal_id.default_ncf_type
            ncf_range = self.env['ncf.range'].search([
                ('ncf_type', '=', ncf_type),
                ('state', '=', 'active')
            ], order='sequence_start', limit=1)
            if not ncf_range:
                raise ValidationError(_(
                    'No available NCF range for type %s.') % ncf_type)
            ncf = ncf_range.assign_ncf()
            if not ncf:
                raise ValidationError(_('NCF range exhausted.'))
            move.ncf_number = ncf
        return move

    def action_post(self):
        for move in self:
            if move.journal_id.usar_ncf:
                if not move.ncf_number:
                    raise ValidationError(_('Invoice requires a valid NCF.'))
        return super().action_post()
