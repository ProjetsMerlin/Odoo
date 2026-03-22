{
    'name': 'Mon Blog Custom',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Blog custom avec modèles Odoo',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'data/config.xml',
        'views/dashboard.xml',
        'views/includes/page_header.xml',
        'views/includes/blog_filter.xml',
        'views/includes/blog_list.xml',
        'views/comments.xml',
        'views/articles_wizards.xml',
        'views/templates.xml',
        'views/articles.xml',
        'views/article.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'mon_blog/static/src/css/blog.css',
        ],
    },
    'installable': True,
    'application': True,
}