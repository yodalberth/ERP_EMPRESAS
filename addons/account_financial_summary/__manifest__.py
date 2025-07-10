{
    'name': 'Financial Summary Reports',
    'version': '1.2',
    'category': 'Accounting',
    'summary': 'Quick summary for ledger, partner balance and balance sheet',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/financial_summary_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
