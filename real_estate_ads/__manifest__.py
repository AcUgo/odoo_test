{
    "name": "Real Estate Ads",
    "Version": "0.1",
    "website": "https://www.makeitsimple.be",
    "author": "arcueid",
    "description": """
        Real estate module to show available properties
    """,
    "category": "Sales",
    "depends": ["base", "mail", "website"],
    "data": [
        #groups
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',
        #
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/menu_items.xml',

        # Data Files
        #'data/property_type.xml',
        'data/estate.property.type.csv'
    ],
    'demo': [
        'demo/property_tag.xml'
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}