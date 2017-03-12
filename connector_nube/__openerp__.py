# -*- coding: utf-8 -*-
# Copyright 2011-2013 Camptocamp
# Copyright 2011-2013 Akretion
# Copyright 2015 AvanzOSC
# Copyright 2015-2016 Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "TiendaNube-Odoo connector",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account",
        "product",
        "product_m2mcategories",
        "connector_ecommerce",
        "product_multi_image",
        "purchase",
        "product_variant_supplierinfo",
        "product_variant_cost_price",
    ],
    "external_dependencies": {
        'python': [
            "html2text",
            # "tiendanube" # hay que instalarlo manualmente porque tiene modificaciones.
        ],
    },
    "author": "jeo Software"
              "Akretion,"
              "Camptocamp,"
              "AvanzOSC,"
              "Tecnativa,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/jobiols/jeo",
    "category": "Connector",
    "data": [
        'data/cron.xml',
        'data/product_decimal_precision.xml',
        'views/tienda_nube_model_view.xml',
        'views/product_view.xml',
        'views/product_category_view.xml',
        'views/image_view.xml',
        'views/delivery_view.xml',
        'views/partner_view.xml',
        'views/sale_view.xml',
        'views/account_view.xml',
        'views/stock_view.xml',
        'views/connector_tienda_nube_menu.xml',
        'security/ir.model.access.csv',
        'security/tienda_nube_security.xml',
        'data/ecommerce_data.xml',
    ],
    "installable": False,
    "application": True,
}
