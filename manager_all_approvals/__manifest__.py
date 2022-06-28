# -*- coding: utf-8 -*-
{
    'name': "All Document Approvals",

    'summary': """
        Approval On All Document""",

    'description': """
        Approval On All Document
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'All',
    'version': '15.0.0.0',
    'sequence': 1,

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'sale', 'account','sale_mrp'],

    # always loaded
    'data': [
        'security/security.xml',
        'reports/sale_template.xml',
        'reports/sale_report.xml',
        'reports/purchase_report.xml',
        'reports/rfq_report.xml',
        'reports/report_header_footer_layout.xml',
        'views/approval_all_manager_views.xml',
        'views/quality.xml',
        #'views/mrp.xml',
        'data/email_template.xml',


    ],
    'assets': {
        'web.assets_backend': [
            'manager_all_approvals/static/src/css/report.css',
        ]
    }

}
