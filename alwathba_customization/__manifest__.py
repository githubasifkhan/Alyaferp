# -*- coding: utf-8 -*-

{
    'name': 'Alwathba Customization',
    'version': '15.0.1.0',
    'category': 'Sales',
    "sequence": 3,
    'summary': 'Manage Activities',
    'complexity': "easy",
    'author': 'Appsgate',
    'depends': ['sale','sale_requisition_report','manager_all_approvals','material_purchase_requisitions','stock','account_po_report'],
    'data': [
        'data/data.xml',
        'security/product_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/product_views.xml',
        'report/report_mrp.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}