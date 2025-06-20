# simple_module/__manifest__.py
{
    'name': 'Simple Module',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'A minimal module with one model, list and form views',
    'depends': ['base','project'],
    'data': [
        'views/simple_group_views.xml',
        'security/simple_model_access.xml',
        'views/sql_query_wizard_views.xml',
        'views/module_wizard_views.xml',

    ],
    'installable': True,
    'application': True,
}
