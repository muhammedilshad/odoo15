{
    'name': 'Weather Notification',
    'version': '15.0.1.0',
    'depends': ['base'],
    'author': 'Dilshad',
    'assets': {
        'web.assets_backend': {
            'custom_weather_notification/static/src/js/systray_icon.js',
            'https://unpkg.com/sweetalert/dist/sweetalert.min.js'
        },
        'web.assets_qweb': {
            'custom_weather_notification/static/src/xml/systray_icon.xml',
        },
    },
    'licence': 'LGPL-3'
}
