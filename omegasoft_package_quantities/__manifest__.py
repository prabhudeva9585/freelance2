# -*- coding: utf-8 -*-
{
    'name': "Omegasoft Package Quantities",
    'version': '17.0',
    'summary': """Add utilities to specifiy the number of Sacks/Packages of your pickings.""",
    'description': """
Add fields and models that holds detailed information about the
number of sacks and packages stored in stock pickings and dispatch
controls
""",
    'author': "Omegasoft C.A",
    'contributor': [
        'Gabriel Peraza - gabriel.peraza@omegasoftve.com',
    ],
    'website': "https://www.omegasoftve.com/",
    'category': 'Inventory/Inventory',
    'depends': [
        'omegasoft_dispatch_control',
        'omegasoft_goods_movement_authorization',
    ],
    'data': [
        'views/stock_picking.xml',
        'views/dispatch_control.xml',
    ],
    'license': 'LGPL-3',
}