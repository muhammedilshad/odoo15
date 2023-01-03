{
    'name': 'Pos Rating',
    'version': '15.0.1.0',
    'depends': ['base', 'sale_management'],
    'author': "dilshad",
    'application': True,
    'assets': {
        'web.assets_backend': [
            'pos_rating/static/src/js/pos_prod_rating.js',
            'pos_rating/static/src/js/pos_reciept_rating.js'
        ],
        'web.assets_qweb': [
            'pos_rating/static/src/xml/pos_custom.xml',
            'pos_rating/static/src/xml/pos_custom_reciept.xml'
        ],
    },
    'data': [
        'views/pos_rating.xml',
    ],
    'license': 'LGPL-3'
}
