{
    'name': 'Purchase Tree Button',
    'version': '15.0.1.0',
    'depends': ['base', 'purchase'],
    'author': 'Dilshad',
    'application': True,
    'assets': {
        'web.assets_backend': [
            '/purchase_tree_view_button/static/src/js/tree_button.js'
        ],
        'web.assets_qweb': [
            '/purchase_tree_view_button/static/src/xml/tree_custom_button.xml',
        ],
    },
    'data': [
        ''
        'views/tree_view_button.xml'
    ],
    'license': 'LGPL-3'
}
