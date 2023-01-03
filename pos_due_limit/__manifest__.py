{
    'name': 'Pos Due Limit',
    'version': '15.0.1.0',
    'depends': ['base'],
    'author': "dilshad",
    'application': True,
    'assets': {
        'web.assets_backend': [
            'pos_due_limit/static/src/js/pos_partner_custom.js'
        ],
    },
    'data': [
            'views/partner_custom_field.xml'
        ],

    'license': 'LGPL-3'
}
