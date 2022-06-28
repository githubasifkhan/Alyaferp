# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime


class ApproveProduct(models.Model):
    _inherit = 'product.template'

    approve_state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Waiting for Approval'),
        ('confirmed', 'Confirmed')
    ], default='draft')

    def confirm_product_approval(self):
        for rec in self:
            rec.approve_state = 'confirmed'

    def submit_product_approval(self):
        for rec in self:
            rec.approve_state = 'submit'

        mail_template = self.env.ref('alwathba_customization.product_template_mail_alwathba')
        product_manager_group = self.env['res.groups'].search([('name', '=', 'Product Manager')])        
        for user in product_manager_group.users:
            mail_template.email_to = user.email
            mail_template.send_mail(self.id, force_send=True)

    def reset_product_approval(self):
        for rec in self:
            rec.approve_state = 'draft'

    def confirm_products(self):
        active_ids = self.env.context.get('active_ids')
        products = self.env['product.template'].browse(active_ids)
        products.confirm_product_approval()


# class MaterialRequisition(models.Model):
#     _inherit = 'material.requisition'
#
#     def confirm_requisition(self):
#         self.ensure_one()
#         res = self.write({
#             'state': 'department_approval',
#             'confirmed_by_id': self.env.user.id,
#             'confirmed_date': datetime.now()
#         })
#
#         mail_template = self.env.ref('alwathba_customization.requisition_review_template_mail_alwathba')
#         req_review_group = self.env['res.groups'].search([('name', '=', 'Material Purchase Requistion Department Manager')])
#         for user in req_review_group.users:
#             mail_template.email_to = user.email
#             mail_template.send_mail(self.id, force_send=True)
#
#     def department_approve(self):
#         res = self.write({
#                             'state':'ir_approve',
#                             'department_manager_id':self.env.user.id,
#                             'department_approval_date' : datetime.now()
#                         })
#
#         mail_template = self.env.ref('alwathba_customization.requisition_approval_template_mail_alwathba')
#         req_approve_group = self.env['res.groups'].search([('name', '=', 'Material Purchase Requisition Manager')])
#         for user in req_approve_group.users:
#             mail_template.email_to = user.email
#             mail_template.send_mail(self.id, force_send=True)
#
#         return res
#

class SaleOder(models.Model):
    _inherit = 'sale.order'

    def action_submit(self):
        self.write({
            'state': 'to_review'
        })
        mail_template = self.env.ref('alwathba_customization.sale_review_template_mail_alwathba')
        sale_review_group = self.env['res.groups'].search([('name', '=', 'Sale Order Review')])        
        for user in sale_review_group.users:
            mail_template.email_to = user.email
            mail_template.send_mail(self.id, force_send=True)

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_sale_order'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

        mail_template = self.env.ref('alwathba_customization.sale_approve_template_mail_alwathba')
        sale_approve_group = self.env['res.groups'].search([('name', '=', 'Sale Order Approve')])        
        for user in sale_approve_group.users:
            mail_template.email_to = user.email
            mail_template.send_mail(self.id, force_send=True)


class PurchaseOder(models.Model):
    _inherit = 'purchase.order'

    def action_submit(self):
        self.write({
            'state': 'to_review'
        })

        mail_template = self.env.ref('alwathba_customization.purchase_review_template_mail_alwathba')
        purchase_review_group = self.env['res.groups'].search([('name', '=', 'Purchase Order Review')])        
        for user in purchase_review_group.users:
            mail_template.email_to = user.email
            mail_template.send_mail(self.id, force_send=True)


    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_purchase_order'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

        mail_template = self.env.ref('alwathba_customization.purchase_approve_template_mail_alwathba')
        purchase_approve_group = self.env['res.groups'].search([('name', '=', 'Purchase Order Approve')])        
        for user in purchase_approve_group.users:
            mail_template.email_to = user.email
            mail_template.send_mail(self.id, force_send=True)