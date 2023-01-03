{
    'name': 'College Erp',
    'version': '15.0.1.0',
    'depends': ['base', 'mail', 'website'],
    'author': "dilshad",
    'assets': {
        'web.assets_backend': [
            'college_erp/static/src/js/action_manager.js'],
    },
    'data': [
        'report/pdf_report.xml',
        'report/report_template.xml',
        'security/ir.model.access.csv',
        'views/college_views.xml',
        'views/college_class_exam_view.xml',
        'views/exam_view.xml',
        'views/promotion.xml',
        'views/mark_sheet_view.xml',
        'views/mark_sheet_view.xml',
        'views/website_menu.xml',
        'views/admission_template.xml',
        'wizard/reporting_wizard.xml'
    ],
    'license': 'LGPL-3'
}
