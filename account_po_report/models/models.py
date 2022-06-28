# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    lpo_no = fields.Char('LPO No')
    d_note_no = fields.Char('D/Note No')
    invoice_type = fields.Selection(selection=[
        ('cash', 'Cash Customer'),
        ('credit', 'Credit Customer'),
        ('standard', 'Standard'),

    ], string='Invoice Type', required=True, copy=False, tracking=True, default='standard')

    def get_amount_in_words(self, amount):
        print(amount)
        text = self.currency_id.amount_to_text(amount['amount_total'])
        return text.title()


class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    def get_amount_in_words(self, amount):
        print(amount)
        text = self.currency_id.amount_to_text(amount['amount_total'])
        return text.title()
