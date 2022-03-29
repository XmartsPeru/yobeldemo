{
    'name': "Yobel SCM Integration",

    'summary': """
        Yobel SCM API Integration""",

    'description': """
        Yobel SCM API for the Integration of Customer Masters, Orders, 
        Shipments and Products, in addition to Order and Shipment 
        confirmations.
    """,

    'author': "XMarts",
    'website': "https://www.xmarts.com",

    'category': 'Integration',
    'version': '1.0.20220101',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock', 'l10n_pe'],

    # always loaded
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Menus
        # Views
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/stock_picking_views.xml',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',
        'views/error_msg_views.xml',
        # Cron Jobs
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'data/xmpe.error.msg.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
