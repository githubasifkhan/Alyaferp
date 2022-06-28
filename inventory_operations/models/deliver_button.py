from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    state = fields.Selection(selection_add=[
       ('delivery', 'Delivered') ,  ('done',)
    ])

    # def action_delivery(self):
    #     print("click")
    #     self.write({'state': 'delivery'})

    # def action__in_delivery(self):
    #     print("click")
    #     self.write({'state': 'delivery'})



