# qiz_integration/__manifest__.py
{
    'name': 'Qiz Integration',
    'version': '1.0',
    'summary': 'Import form templates and aggregated results.',
    'category': 'Extra Tools',
    'author': 'Susmoy Debnath',
    'depends': ['base'], 
    'data': [
        'security/ir.model.access.csv',
        'views/qiz_template_views.xml',
        'views/qiz_question_views.xml',
        'views/qiz_menus.xml',
        'wizard/import_qiz_data_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
