from datetime import timedelta

from freezegun import freeze_time
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo import fields


class TestNCFRange(TransactionCase):
    def setUp(self):
        super().setUp()
        self.range = self.env['ncf.range'].create({
            'name': 'Test Range',
            'ncf_type': 'B01',
            'sequence_start': 'B0100000001',
            'sequence_end': 'B0100000010',
            'expiration_date': fields.Date.today() + timedelta(days=1),
        })
        self.range.action_activate()
        self.journal = self.env['account.journal'].create({
            'name': 'NCF Journal',
            'type': 'sale',
            'code': 'NCF1',
            'usar_ncf': True,
            'default_ncf_type': 'B01',
        })

    @freeze_time((fields.Date.today() + timedelta(days=2)).strftime('%Y-%m-%d'))
    def test_assign_ncf_expired(self):
        with self.assertRaises(ValidationError):
            self.range.assign_ncf()

    @freeze_time((fields.Date.today() + timedelta(days=2)).strftime('%Y-%m-%d'))
    def test_invoice_creation_blocked(self):
        with self.assertRaises(ValidationError):
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'journal_id': self.journal.id,
                'partner_id': self.env['res.partner'].create({'name': 'P'}).id,
                'apply_ncf': True,
                'invoice_line_ids': [(0, 0, {'name': 'l', 'price_unit': 10})],
            })

    def test_partner_default_apply_ncf(self):
        partner = self.env['res.partner'].create({
            'name': 'Requiring Partner',
            'ncf_required': True,
            'default_ncf_type': 'B01',
        })
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'journal_id': self.journal.id,
            'partner_id': partner.id,
            'invoice_line_ids': [(0, 0, {'name': 'l', 'price_unit': 10})],
        })
        self.assertTrue(invoice.apply_ncf)
        self.assertEqual(invoice.ncf_type, 'B01')

    def test_post_without_ncf(self):
        partner = self.env['res.partner'].create({'name': 'No NCF'})
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'journal_id': self.journal.id,
            'partner_id': partner.id,
            'apply_ncf': False,
            'invoice_line_ids': [(0, 0, {'name': 'l', 'price_unit': 10})],
        })
        invoice.action_post()
        self.assertFalse(invoice.ncf_number)


