

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    is_price = fields.Boolean('Is Price',compute='_compute_purchase_line_price',default=False)

    receipt_count = fields.Integer("Receipt count", compute='_compute_picking_count')
    rec_picking_ids = fields.One2many('stock.picking', 'purchase_id',string='Receptions', copy=False,
                                   store=True)

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('rfqsent', 'RFQ Sent'),
        ('to_review', 'Waiting For Review'),
        ('approve', 'Waiting For Approval'),
        ('approved','Approved'),
        ('to approve', 'To Approve'),
        ('sent', 'PO Sent'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_confirm(self):
        for order in self:

            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def action_view_rec_pickings(self):
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_purchase_id': self.id,
           

        })

        return {
            'name': _('Receipts'),
            'domain': [('origin', '=', self.name)],
            'res_model': 'stock.picking',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context': ctx

        }


    def _compute_picking_count(self):
        for rec in self:
            rec.receipt_count = len(self.env['stock.picking'].search([('origin','=',rec.name)]))



    
    
    def action_submit(self):
        self.write({
            'state': 'to_review'
        })

    def _compute_purchase_line_price(self):
        for rec in self:
            for line in rec.order_line:
                if line.price_unit and line.price_unit > 0:
                    rec.is_price =True
                else:
                    rec.is_price = False

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

           # template_id = int(self.env['ir.config_parameter'].sudo().get_param('manager_all_approvals.email_template_edi_sale_template'))
        template_id = self.env['ir.model.data']._xmlid_to_res_id('manager_all_approvals.email_template_edi_purchase_template',raise_if_not_found=False)
        template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
        if not template_id:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('purchase.email_template_edi_purchase', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('purchase.email_template_edi_purchase_done', raise_if_not_found=False)

        return template_id
    
    
    def _find_rfq_mail_template(self, force_confirmation_template=False):
        template_id = False

           # template_id = int(self.env['ir.config_parameter'].sudo().get_param('manager_all_approvals.email_template_edi_sale_template'))
        template_id = self.env['ir.model.data']._xmlid_to_res_id('manager_all_approvals.email_template_edi_rfq_template',raise_if_not_found=False)
        template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
        if not template_id:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('manager_all_approvals.email_template_edi_rfq_template', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('manager_all_approvals.email_template_edi_rfq_template', raise_if_not_found=False)

        return template_id


    def action_send_draft_rfq(self):

        if self.state == 'draft':
            self.write({
                'state': 'rfqsent'
            })

        self.ensure_one()
        template_id = self._find_rfq_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'purchase.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_rfq_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


    def action_rfq_send(self):

        if self.state == 'approved':
            self.write({
                'state': 'sent'
            })

        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'purchase.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_rfq_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }





    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_purchase_order'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })



    def button_approved(self):
        
        if self.env.user.has_group('manager_all_approvals.group_approve_purchase_order'):
            self.approve_by_id = self.env.user.id
        self.write({

            'state': 'approved'
        })
        # for order in self:
        #     if order.state not in ['draft', 'sent', 'approve']:
        #         continue
        #     order._add_supplier_to_product()
        #     # Deal with double validation process
        #     if order.company_id.po_double_validation == 'one_step' \
        #             or (order.company_id.po_double_validation == 'two_step' \
        #                 and order.amount_total < self.env.company.currency_id._convert(
        #                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
        #                 order.date_order or fields.Date.today())) \
        #             or order.user_has_groups('purchase.group_purchase_manager'):
        #         order.button_approve()
        #     else:
        #         order.write({'state': 'to approve'})
        #     if order.partner_id not in order.message_partner_ids:
        #         order.message_subscribe([order.partner_id.id])
        # return True

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def button_approve_reject(self):
        self.write({
            'state': 'rejected'
        })


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')
    new_mrp_count = fields.Integer(string="Manufacturing", compute='_compute_new_mrp_count')
    #manu_ids = fields.One2many('mrp.production', 'sale_id', string='Requisition')

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('to_review', 'Waiting For Review'),
        ('approve', 'Waiting For Approval'),
        ('approved', 'Approved'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    delivery_type = fields.Selection([
        ('standard','Standard'),
        ('pick','Pick UP')
    ],string='Delivery Type',default='standard')


    def action_submit(self):
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_sale_order'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_sale_order'):
            self.approve_by_id = self.env.user.id
        self.write({

            'state':'approved'
        })
        # rec = super(SaleOrderInh, self).action_confirm()
        # return rec


    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def button_approve_reject(self):
        self.write({
            'state': 'rejected'
        })

    def button_client_approve(self):
        rec = super(SaleOrderInh, self).action_confirm()
        return rec

    def button_client_reset(self):
        self.write({
            'state': 'draft'
        })


    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False
        if force_confirmation_template or (self.state == 'approved') or (self.state == 'sale'):
           # template_id = int(self.env['ir.config_parameter'].sudo().get_param('manager_all_approvals.email_template_edi_sale_template'))
            template_id = self.env['ir.model.data']._xmlid_to_res_id('manager_all_approvals.email_template_edi_sale_template',raise_if_not_found=False)
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data']._xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)

        return template_id





    def action_quotation_send(self):
        res = super(SaleOrderInh, self).action_quotation_send()
        if self.state == 'approved':
            self.write({
                'state':'sent'
            })


        return res

    def _compute_new_mrp_count(self):
        for rec in self:
            rec.new_mrp_count = len(self.env['mrp.production'].search([('origin', 'like', rec.name)]))

    def compute_new_mrp_count(self):
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_origin': self.name,

        })

        return {
            'name': _('Manufacturing'),
            'domain': [('origin', 'like', self.name)],
            'res_model': 'mrp.production',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context': ctx

        }

    



class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('to_review', 'Waiting For Review'),
        ('approve', 'Waiting For Approval'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    def action_post(self):
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_invoice_bill'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_invoice_bill'):
            self.approve_by_id = self.env.user.id
        rec = super(AccountMoveInh, self).action_post()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def button_approve_reject(self):
        self.write({
            'state': 'rejected'
        })

# class StockPicking(models.Model):
#     _inherit ='stock.picking'
#
#     rec_purchase_id = fields.Many2one( string="Purchase Order", store=True, readonly=False)


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    # state = fields.Selection([('draft', 'Draft'),
    #                           ('approve', 'Waiting For Approval'),
    #                           ('posted', 'Validated'),
    #                           ('sent', 'Sent'),
    #                           ('reconciled', 'Reconciled'),
    #                           ('cancelled', 'Cancelled'),
    #                           ('reject', 'Reject')
    #                           ], readonly=True, default='draft', copy=False, string="Status")

    def action_post(self):
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_payment'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_payment'):
            self.approve_by_id = self.env.user.id
        rec = super(AccountPaymentInh, self).action_post()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def button_approve_reject(self):
        self.write({
            'state': 'rejected'
        })
