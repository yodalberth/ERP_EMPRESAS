from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    apply_ncf = fields.Boolean(string='¿Aplicar NCF?')
    ncf_type = fields.Selection([
        ('B01', 'B01'),
        ('B02', 'B02'),
        ('B03', 'B03'),
        ('B04', 'B04'),
        ('E31', 'E31'),
        ('E32', 'E32'),
    ], string='Tipo de NCF')
    ncf_number = fields.Char(string='NCF')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            if 'apply_ncf' not in vals:
                vals['apply_ncf'] = partner.ncf_required
            if vals.get('apply_ncf') and not vals.get('ncf_type'):
                vals['ncf_type'] = partner.default_ncf_type or vals.get('journal_id') and self.env['account.journal'].browse(vals['journal_id']).default_ncf_type
        moves = super().create(vals_list)
        for move, vals in zip(moves, vals_list):
            if move.move_type == 'out_invoice' and move.apply_ncf:
                ncf_type = move.ncf_type or move.journal_id.default_ncf_type
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
        return moves

    def action_post(self):
        for move in self:
            if move.apply_ncf:
                if not move.ncf_number:
                    raise ValidationError(_('Invoice requires a valid NCF.'))
        return super().action_post()
