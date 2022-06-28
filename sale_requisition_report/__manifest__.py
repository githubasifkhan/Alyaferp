# -*- coding: utf-8 -*-
{
    'name': "Sale Requisition Report",

    'summary': """
        Print Sale And Requisition Report""",

    'description': """
        Print Sale And Requisition Report
    """,

    'author': "Musadiq Fiaz CHaudhary",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '15.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'purchase', 'material_purchase_requisitions'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/views.xml',
        'reports/sale_report.xml',
        'reports/sale_template.xml',
        'reports/requisition_report.xml',
        'reports/requisition_template.xml',
    ],

}
