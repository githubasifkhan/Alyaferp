# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quality Control Community ',
    'version': '1.0',
    'category': 'Manufacturing/Quality',
    'sequence': 120,
    'summary': 'Control the quality of your products',
    'depends': ['quality_community'],
    'description': """
Quality Control
===============
* Define quality points that will generate quality checks on pickings,
  manufacturing orders or work orders (quality_mrp)
* Quality alerts can be created independently or related to quality checks
* Possibility to add a measure to the quality check with a min/max tolerance
* Define your stages for the quality alerts
""",
    'data': [
        'data/qlty_ctrl_data.xml',
        'report/wk_custom_reports.xml',
        'report/wk_custom_report_templates.xml',
        'views/qlty_views.xml',
        'views/product_views.xml',
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
        'wizard/qlty_check_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/qlty_ctrl_demo.xml',
    ],
    'application': True,
    'assets': {
        'web.assets_backend': [
            'quality_ctrl_community/static/src/**/*',
        ],
    }
}
