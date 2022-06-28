# -*- coding: utf-8 -*-
#############################################################################
#
#
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Internal Picking',
    'category': 'Inventory',
    'summary': "Internal Picking",
    'author': 'APPSGATE FZC LLC',
    'depends': ['stock','alwathba_customization'],

    'description': """ 
            Inventory 
            Picking    

		
		Materials,
	 	stock,
		

     """,

    'data': [
        'security/ir.model.access.csv',
        'views/internal_picking.xml',

        'data/sequence.xml',

    ],


    'demo': [
    ],
    'license': 'AGPL-3',
    'price': '12',
    'currency': 'USD',
    'application': True,
    'installable': True,
    'auto_install': False,
}
