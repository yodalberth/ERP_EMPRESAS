{
    'name': 'DGII NCF Manager',
    'version': '1.0.0',
    'summary': 'Manage DGII NCF ranges for Dominican Republic',
    'category': 'Accounting',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': [
        'account'
    ],
    'data': [
        'security/dgii_ncf_security.xml',
        'security/ir.model.access.csv',
        'views/ncf_range_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'wizard/import_ncf_wizard_views.xml',
        'report/ncf_range_report.xml',
        'report/ncf_range_templates.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': True,
}
