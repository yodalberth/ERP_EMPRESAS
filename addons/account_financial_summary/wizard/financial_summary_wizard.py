from odoo import fields, models


class AccountFinancialSummaryWizard(models.TransientModel):
    _name = 'account.financial.summary.wizard'
    _description = 'Financial Summary Wizard'
    _check_company_auto = True

    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
        readonly=True
    )
    date_from = fields.Date(required=True, default=fields.Date.context_today)
    date_to = fields.Date(required=True, default=fields.Date.context_today)
    report_type = fields.Selection([
        ('ledger', 'Libro Mayor'),
        ('partner_balance', 'Estado de Cuentas'),
        ('balance_sheet', 'Balance General'),
    ], default='ledger', required=True)
    partner_id = fields.Many2one('res.partner')
    line_ids = fields.One2many('account.financial.summary.line', 'wizard_id')
    xls_file = fields.Binary()

    def action_generate(self):
        self.ensure_one()
        self.line_ids.unlink()
        if self.report_type == 'ledger':
            query = """
                SELECT account_id, SUM(debit) AS debit, SUM(credit) AS credit
                FROM account_move_line
                WHERE company_id = %s AND date >= %s AND date <= %s AND parent_state = 'posted'
                GROUP BY account_id
            """
            params = (self.company_id.id, self.date_from, self.date_to)
            self.env.cr.execute(query, params)
            results = self.env.cr.fetchall()
            lines = [
                (0, 0, {
                    'account_id': account_id,
                    'label': self.env['account.account'].browse(account_id).display_name,
                    'debit': debit,
                    'credit': credit,
                    'balance': debit - credit,
                })
                for account_id, debit, credit in results
            ]
        elif self.report_type == 'partner_balance':
            query = """
                SELECT partner_id, SUM(debit) AS debit, SUM(credit) AS credit
                FROM account_move_line
                WHERE company_id = %s AND date >= %s AND date <= %s AND parent_state = 'posted' %s
                GROUP BY partner_id
            """
            extra = ''
            params = [self.company_id.id, self.date_from, self.date_to]
            if self.partner_id:
                extra = 'AND partner_id = %s'
                params.append(self.partner_id.id)
            self.env.cr.execute(query % extra, tuple(params))
            results = self.env.cr.fetchall()
            lines = [
                (0, 0, {
                    'partner_id': partner_id,
                    'label': self.env['res.partner'].browse(partner_id).display_name,
                    'debit': debit,
                    'credit': credit,
                    'balance': debit - credit,
                })
                for partner_id, debit, credit in results
            ]
        else:  # balance_sheet
            query = """
                SELECT aa.internal_group, SUM(l.debit) AS debit, SUM(l.credit) AS credit
                FROM account_move_line l
                JOIN account_account aa ON l.account_id = aa.id
                WHERE l.company_id = %s AND l.date >= %s AND l.date <= %s AND l.parent_state = 'posted'
                GROUP BY aa.internal_group
            """
            params = (self.company_id.id, self.date_from, self.date_to)
            self.env.cr.execute(query, params)
            results = self.env.cr.fetchall()
            group_labels = dict(self.env['account.account'].fields_get()['internal_group']['selection'])
            lines = [
                (0, 0, {
                    'label': group_labels.get(group) or group,
                    'debit': debit,
                    'credit': credit,
                    'balance': debit - credit,
                })
                for group, debit, credit in results
            ]
        self.line_ids = lines
        return {
            'type': 'ir.actions.act_window',
            'name': 'Financial Summary',
            'res_model': 'account.financial.summary.line',
            'view_mode': 'tree',
            'target': 'new',
            'domain': [('wizard_id', '=', self.id)],
        }

    def action_export_xlsx(self):
        self.ensure_one()
        if not self.line_ids:
            self.action_generate()
        import base64
        import io
        from odoo.tools.misc import xlsxwriter

        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        headers = ['Label', 'Debit', 'Credit', 'Balance']
        worksheet.write_row(0, 0, headers)
        for row, line in enumerate(self.line_ids, start=1):
            worksheet.write(row, 0, line.label)
            worksheet.write_number(row, 1, line.debit)
            worksheet.write_number(row, 2, line.credit)
            worksheet.write_number(row, 3, line.balance)
        workbook.close()
        buffer.seek(0)
        self.xls_file = base64.b64encode(buffer.getvalue())
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': (
                '/web/content?model=account.financial.summary.wizard&field=xls_file'
                '&download=true&filename=Financial_Summary.xlsx&id=%d' % self.id
            ),
        }


class AccountFinancialSummaryLine(models.TransientModel):
    _name = 'account.financial.summary.line'
    _description = 'Financial Summary Line'
    _order = 'sequence'

    sequence = fields.Integer()
    wizard_id = fields.Many2one('account.financial.summary.wizard', ondelete='cascade')
    account_id = fields.Many2one('account.account', readonly=True)
    partner_id = fields.Many2one('res.partner', readonly=True)
    label = fields.Char(readonly=True)
    debit = fields.Monetary(currency_field='currency_id', readonly=True)
    credit = fields.Monetary(currency_field='currency_id', readonly=True)
    balance = fields.Monetary(currency_field='currency_id', readonly=True)
    currency_id = fields.Many2one(
        'res.currency',
        related='wizard_id.company_id.currency_id',
        readonly=True
    )

