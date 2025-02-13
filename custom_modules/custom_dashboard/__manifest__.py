{
    'name': 'Custom Dashboard',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'A custom dashboard for Odoo',
    'depends': ['base', 'sale', 'account', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
}