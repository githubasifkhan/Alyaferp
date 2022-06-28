
# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quality Community',
    'version': '1.0',
    'category': 'Manufacturing/Quality',
    'sequence': 50,
    'summary': 'Basic Feature for Quality In Community Version',
    'depends': ['stock'],
    'description': """
Quality Base
===============
* Define quality points that will generate quality checks on pickings,
  manufacturing orders or work orders (quality_mrp)
* Quality alerts can be created independently or related to quality checks
* Possibility to add a measure to the quality check with a min/max tolerance
* Define your stages for the quality alerts
""",
    'data': [
        'security/qlty_security.xml',
        'security/ir.model.access.csv',
        'data/qlty_data.xml',
        'views/qlty_views.xml',
    ],
    'demo': [],
    'application': False,

    'assets': {
        'web.assets_backend': [
            'quality_community/static/src/js/tablet_image_widget.js',
            'quality_community/static/src/scss/tablet_view.scss',
        ],
        'web.assets_qweb': [
            'quality_community/static/src/xml/**/*',
        ],
    }
}
