{
    'name': 'DGII NCF Manager',
    'version': '1.0.0',
    'summary': 'Gestión de rangos de NCF otorgados por la DGII',
    'category': 'Accounting',
    'author': 'Your Company',
    'description': 'Módulo para administrar rangos de comprobantes fiscales de la DGII y asignarlos a las facturas.',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'custom_erp'
    ],
    'data': [
        'security/dgii_ncf_security.xml',
        'security/ir.model.access.csv',
        'views/ncf_range_views.xml',
        'views/account_journal_views.xml',
        'wizard/import_ncf_wizard_views.xml',
        'report/ncf_range_report.xml',
        'report/ncf_range_templates.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
