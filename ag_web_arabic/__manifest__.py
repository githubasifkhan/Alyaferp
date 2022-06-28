# -*- coding: utf-8 -*-
{
    'name': 'Odoo Arabic (Right to Left) - RTL',
    'version': '13.0.0.2',
    'category': 'Technical Settings',
    'sequence': 1,
    'summary': 'Odoo Arabic (Right to Left)',
    'description':
        """
Adding RTL (Right to Left) Support for Odoo.
===========================================

This module provide RTL support in odoo based on user language settings. 
Language have option to choose the direction such as whether from Right to Left or 
Left to Right.
        """,
    'author': 'APPSGATE FZC LLC',
    'price': 0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['web'],
    'data': ['views/templates.xml'],
    'demo': [],
    'qweb': [],
   # 'images': ['images/odoo_arabic_screenshot.png'],
    "installable": True,
    "application": True,
    "auto_install": False,
    #'live_test_url': 'https://www.youtube.com/watch?v=l32pK_XpOBE&t=111s'
}
