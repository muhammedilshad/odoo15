{
    'name': 'import lot/serial',
    'version': '15.0.1.0',
    'depends': ['base', 'stock'],
    'author': "dilshad",
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_for_lot_import.xml',
        'views/import_lot_xlsx_file.xml'
    ],
    'license': 'LGPL-3'
}
