{
    'name': 'Material Request',
    'version': '15.0.1.0',
    'depends': ['base', 'purchase', 'product', 'stock', 'hr'],
    'author': "dilshad",
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'security/user_group.xml',
        'view/material_request.xml',

    ],
    'license': 'LGPL-3'
}