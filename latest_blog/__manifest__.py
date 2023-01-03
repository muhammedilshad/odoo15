{
    'name': 'Latest Blog',
    'version': '15.0.1.0',
    'depends': ['base', 'website', 'website_blog'],
    'author': "dilshad",
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/latest_blog/static/src/js/dynamic.js',
        ],
    },
    'data': [
        'views/snippet_template.xml',
    ],
    'license': 'LGPL-3'
    }
