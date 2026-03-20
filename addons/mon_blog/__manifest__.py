{
    'name': 'Mon Blog Custom',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Blog custom avec modèles Odoo',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'mon_blog/static/src/css/blog.css',
        ],
    },
    'installable': True,
    'application': True,
}