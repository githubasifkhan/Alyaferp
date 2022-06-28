# -*- encoding: utf-8 -*-

{
    'name': 'MRP Community features for Quality Control',
    'version': '1.0',
    'category': 'Manufacturing/Quality',
    'sequence': 50,
    'summary': 'Quality Management with MRP',
    'depends': ['quality_ctrl_community', 'mrp'],
    'description': """
    Adds workcenters to Quality Control
""",
    "data": [
        'security/qlty_mrp.xml',
        'views/qlty_views.xml',
        'views/mrp_production_views.xml',
        'report/wk_custom_report_templates.xml',
    ],
    "demo": [],
    'auto_install': True,
}
