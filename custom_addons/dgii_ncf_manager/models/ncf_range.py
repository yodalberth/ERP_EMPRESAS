from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class NCFRange(models.Model):
    _name = 'ncf.range'
    _description = 'NCF Range'
    _order = 'ncf_type, sequence_start'

    name = fields.Char(required=True)
    ncf_type = fields.Selection([
        ('B01', 'B01 - Factura de Cr\u00e9dito Fiscal'),
        ('B02', 'B02 - Factura de Consumo'),
        ('B03', 'B03 - Reg\u00edmenes Especiales'),
        ('B04', 'B04 - Gasto Menor'),
        ('E31', 'E31 - e-CF Factura de Cr\u00e9dito Fiscal'),
        ('E32', 'E32 - e-CF Factura de Consumo'),
    ], required=True)
    sequence_start = fields.Char(required=True)
    sequence_end = fields.Char(required=True)
    expiration_date = fields.Date(required=True)
    current_ncf = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('exhausted', 'Exhausted'),
        ('expired', 'Expired'),
    ], default='draft', compute='_compute_state', store=True)

    @api.constrains('sequence_start', 'sequence_end', 'ncf_type')
    def _check_overlap(self):
        for rec in self:
            overlaps = self.search([
                ('id', '!=', rec.id),
                ('ncf_type', '=', rec.ncf_type),
                ('state', 'in', ['draft', 'active']),
                ('sequence_start', '<=', rec.sequence_end),
                ('sequence_end', '>=', rec.sequence_start),
            ], limit=1)
            if overlaps:
                raise ValidationError(_('NCF range overlaps with existing range.'))

    @api.depends('expiration_date', 'current_ncf')
    def _compute_state(self):
        today = fields.Date.today()
        for rec in self:
            if rec.expiration_date and rec.expiration_date < today:
                rec.state = 'expired'
            elif rec.current_ncf and rec.current_ncf > rec.sequence_end:
                rec.state = 'exhausted'
            elif rec.current_ncf:
                rec.state = 'active'
            else:
                rec.state = 'draft'

    def action_activate(self):
        for rec in self:
            rec.current_ncf = rec.sequence_start
            rec.state = 'active'

    def _get_next_ncf(self):
        self.ensure_one()
        if not self.current_ncf:
            next_ncf = self.sequence_start
        else:
            prefix = self.current_ncf[:3]
            number = int(self.current_ncf[3:])
            next_num = number + 1
            next_ncf = prefix + str(next_num).zfill(len(self.current_ncf) - 3)
        if next_ncf > self.sequence_end:
            self.state = 'exhausted'
            return None
        self.current_ncf = next_ncf
        self._compute_state()
        return next_ncf

    def assign_ncf(self):
        self.ensure_one()
        if self.state != 'active':
            raise ValidationError(_('NCF range is not active.'))
        ncf = self.current_ncf or self.sequence_start
        next_ncf = self._get_next_ncf()
        if not next_ncf:
            ncf = None
        return ncf

    @api.model
    def _cron_check_expiration(self):
        for rec in self.search([('state', 'in', ['draft', 'active'])]):
            rec._compute_state()
