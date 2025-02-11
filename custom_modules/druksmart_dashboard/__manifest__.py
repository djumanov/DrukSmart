{
    'name': 'Custom Dashboard',
    'version': '1.0',
    'summary': 'A custom dashboard for Sales, Accounting, and HR',
    'description': 'This module provides a custom dashboard with charts for Sales, Cash Flow, Revenue, Expenses, and HR metrics.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Tools',
    'depends': ['base', 'sale', 'account', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'druksmart_dashboard/static/src/css/dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
}
