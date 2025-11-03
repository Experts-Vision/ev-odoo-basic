{
    'name': 'Estate',
    'version': '1.0.0',
    'category': 'Real Estate',
    'summary': 'Estate Management',
    'description': 'Estate Management',
    'author': 'Estate',
    'website': 'https://www.estate.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/menus.xml',
        'views/views.xml',
        'views/res_users.xml'
    ],
    'installable': True,
    'application': True,
}