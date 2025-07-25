{
    'name': 'Custom ERP Extension',
    'summary': 'Sales, Accounting, Purchase, and optional Payroll tools',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
        'account',
        'purchase',
        'stock',
        'point_of_sale',
        'hr',
    ],
    'data': [
        # Data files, views, security, etc.
    ],
    'installable': True,
    'application': False,
}
