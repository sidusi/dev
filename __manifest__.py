{
    "name":"Real Estate",
    "version":"1.0",
    "website":"mpe.co.id",
    "author":"sidusi",
    "description":"""
        Real Estate module to show available properties
    """,
    "category":"Sales",
    "depends":["base"],
    "data":[
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/property_offer.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/menu_items.xml',

    #Data Files from .csv and .xml file
        # you can add data from .csv file or .xml file , but for csv file the name of csv file must be the same as model name
        # 'data/property_type.xml',
        'data/estate.property.type.csv',
    ],
    # the different of data files and demo files is, for the demo files you must check the checkbox Demo data from initial instalation first
    # before it store to the model
    "demos":[
        'demo/property_tag.xml'
    ],
    "installable":True,
    "application":True,
    "license":"LGPL-3",
}