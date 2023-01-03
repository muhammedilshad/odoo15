{
    'name': 'Daily Attendance Report',
    'version': '15.0.1.0',
    'depends': ['base', 'hr_attendance'],
    'author': "dilshad",
    'application': True,
    'assets': {
        'web.assets_backend': [
            'daily_attendance_report/static/src/js/action_manager.js'
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'wizard/button_wizard.xml',
        'report/pdf_report.xml',
        'report/pdf_template.xml',
        'views/attendance_menuitem.xml',

    ],
    'license': 'LGPL-3'
}
