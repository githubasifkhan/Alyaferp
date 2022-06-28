# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta
import math
from odoo.exceptions import UserError, AccessError, ValidationError



class InternalPicking(models.Model):
    _name = "internal.picking"
    _inherit = 'mail.thread'
    _rec_name = 'sequence'
    _order = 'sequence desc'

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('internal.picking') or '/'
        vals['prepared_by'] = self.env.uid
        return super(InternalPicking, self).create(vals)

    # @api.onchange('employee_id')
    # def get_emp_dest_location(self):
    #     if self.employee_id:
    #         self.destination_location_id = self.employee_id.destination_location_id.id

    @api.model
    def default_get(self, flds):
        result = super(InternalPicking, self).default_get(flds)
        # result['employee_id'] = self.env.user.partner_id.id
        result['requisition_date'] = datetime.now()
        return result

    def confirm_requisition(self):
        self.ensure_one()
        picking_count = len(self.pickings_line_ids)
        if picking_count == 0:
            raise UserError('Please Fill The Product Lines')
        else:
            res = self.write({
                'state': 'internal_picking',
                'confirmed_by_id': self.env.user.id,
                'confirmed_date': datetime.now()
            })

        # ir_model_data = self.env['ir.model.data']
        # try:
        # 	template_id = ir_model_data._xmlid_lookup('AG_material_requisition.email_employee_purchase_requisition_new')[2]
        # except ValueError:
        # 	template_id = False
        # try:
        # 	compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        # except ValueError:
        # 	compose_form_id = False
        #
        # ctx = {
        # 	'default_model': 'material.requisition',
        # 	'default_res_id': self.ids[0],
        # 	'default_use_template': bool(template_id),
        # 	'default_template_id': template_id,
        # 	'default_composition_mode': 'comment',
        # 	'force_email': True
        # }
        # return {
        # 	'name': _('Compose Email'),
        # 	'type': 'ir.actions.act_window',
        # 	'view_mode': 'form',
        # 	'res_model': 'mail.compose.message',
        # 	'views': [(compose_form_id, 'form')],
        # 	'view_id': compose_form_id,
        # 	'target': 'new',
        # 	'context': ctx,
        # }

        return res

    def product_available(self):
        for line in self.pickings_line_ids:
            avail_qty = line.product_id.with_context({'location_id': self.source_location_id.id}).qty_available
            line.write({'available_qty': avail_qty})


    def action_cancel(self):
        for res in self:
            stock_req = self.env['stock.picking'].search([('origin', '=', res.sequence)])
            if stock_req:
                for stock in stock_req:
                    stock.action_cancel()
                    stock.unlink()

        res = self.write({
            'state': 'cancel',
        })
        return res

    def action_received(self):
        pickings = self.env['stock.picking'].search([('origin', '=', self.sequence), ('backorder_id', '=', False)])
        print('======pickingsss====', pickings)
        for picking in pickings:
            print('======picking====', picking)
            if picking.state == 'done':
                print('======state=====', )
                self.write({
                    'state': 'received',
                    'received_date': datetime.now()
                })
            else:
                print('======ELSE=====')
                raise UserError(_('You cant received the product,because picking is not completed'))

    def action_reject(self):
        for res in self:
            stock_req = self.env['stock.picking'].search([('origin', '=', res.sequence)])
            if stock_req:
                for stock in stock_req:
                    stock.action_cancel()
                    stock.unlink()

        res = self.write({
            'state': 'cancel',
            'rejected_date': datetime.now(),
            'rejected_by': self.env.user.id
        })
        return res

    def action_reset_draft(self):
        for res in self:
            stock_req = self.env['stock.picking'].search([('origin', '=', res.sequence)])
            if stock_req:
                for stock in stock_req:
                    stock.action_cancel()
                    stock.unlink()

            res.write({
                'state': 'new',
            })
        return res



    def _get_internal_picking_count(self):
    	for picking in self:
    		picking_ids = self.env['stock.picking'].search([('picking_mat_picking_id','=',picking.id)])
    		picking.internal_picking_count = len(picking_ids)

    def create_picking(self):
        for line in self.pickings_line_ids.filtered(lambda r: r.available_qty < r.qty):
            raise UserError(_('Please create purchase tender,because available qty is less than that of actual qty'))
        else:
            self.sudo().create_picking_new()

    def create_picking_new(self):
        stock_picking_obj = self.env['stock.picking']
        stock_move_obj = self.env['stock.move']
        stock_picking_type_obj = self.env['stock.picking.type']
        picking_type_ids = stock_picking_type_obj.search([('sequence_code', '=', 'ST-PR')])
        if not picking_type_ids:
            raise UserError(_('Please define Internal Picking.'))
        for res in self:
            val = {
                'origin': res.sequence,
                'picking_type_id': picking_type_ids[0].id,
                'company_id': self.env.user.company_id.id,
                'location_id': res.source_location_id.id,
                'location_dest_id': res.destination_location_id.id,
                'picking_mat_picking_id': res.id,
                # 'analytic_id': res.analytic_id.id,
                # 'task_id': res.task_id.id
            }
            stock_picking = stock_picking_obj.create(val)
        for line in self.pickings_line_ids:
            pic_line_val = {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'product_uom': line.uom_id.id,
                'location_id': res.source_location_id.id,
                #'available_qty':line.available_qty,
                # 'location_id': self.source_location_id.id,
                'location_dest_id': res.destination_location_id.id,
                'picking_id': stock_picking.id

            }
            stock_move = stock_move_obj.create(pic_line_val)
        res = self.write({
            'state': 'io_created',
        })
        return res

    def internal_picking_button(self):
    	self.ensure_one()
    	return {
    		'name': 'Internal Picking',
    		'type': 'ir.actions.act_window',
    		'view_mode': 'tree,form',
    		'res_model': 'stock.picking',
    		'domain': [('picking_mat_picking_id', '=', self.id)],
    	}



    def _get_emp_destination(self):
        if not self.employee_id.destination_location_id:
            return
        self.destination_location_id = self.employee_id.destination_location_id

    @api.model
    def _default_picking_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not types:
            types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return types[:1]

    @api.model
    def _default_picking_internal_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)])
        if not types:
            types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
        return types[:1]



    def _default_destination_location(self):
        location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1)
        return location_dest_id

    def _default_source_location(self):
        location_id = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        return location_id

    sequence = fields.Char(string='Sequence', readonly=True, copy=False)
    employee_id = fields.Many2one('hr.employee', string="Requestor", required=True, track_visibility='always',
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)],
                                                                                      limit=1))
    requisition_date = fields.Date(string="Requisition Date", required=True, track_visibility='always')
    received_date = fields.Date(string="Received Date", readonly=True)
    requisition_deadline_date = fields.Date(string="Requisition Deadline")
    state = fields.Selection([
        ('new', 'New'),
        ('internal_picking', 'Internal Picking'),
        ('io_created', 'Picking Created'),
        ('received', 'Received'),
        ('cancel', 'Cancel')], string='Stage', default="new")
    pickings_line_ids = fields.One2many('internal.picking.line', 'picking_id', string="Picking Line ID")
    confirmed_by_id = fields.Many2one('res.users', string="Confirmed By")
    #department_manager_id = fields.Many2one('res.users', string="Department Manager")
    approved_by_id = fields.Many2one('res.users', string="Approved By")
    prepared_by = fields.Many2one('res.users', string="Prepared By")
    rejected_by = fields.Many2one('res.users', string="Rejected By")
    confirmed_date = fields.Date(string="Confirmed Date", readonly=True)
    #department_approval_date = fields.Date(string="Department Approval Date", readonly=True)
    approved_date = fields.Date(string="Approved Date", readonly=True)
    rejected_date = fields.Date(string="Rejected Date", readonly=True)
    reason_for_requisition = fields.Text(string="Reason For Requisition")
    source_location_id = fields.Many2one('stock.location', string="Source Location", related='picking_type_id.default_location_src_id')#default=_default_source_location
    destination_location_id = fields.Many2one('stock.location', string="Destination Location",
                                              related='picking_type_id.default_location_dest_id')#default=_default_destination_location
    internal_picking_id = fields.Many2one('stock.picking.type', string="Delivery Order",
                                          default=_default_picking_internal_type)
    internal_picking_count = fields.Integer('Internal Picking', compute='_get_internal_picking_count')
    #purchase_order_count = fields.Integer('Purchase Tender', compute='_get_purchase_order_count')
    company_id = fields.Many2one('res.company', string="Company")
    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', required=True, default=_default_picking_type)


# analytic_id =fields.Many2one('account.analytic.account',string="Project", required=True,track_visibility='always')
# task_id = fields.Many2one('project.task', string="Task", required=True,track_visibility='always')
    #picking_id = fields.One2many('stock.picking', 'requisition_picking_id')


class RequisitionLine(models.Model):
    _name = "internal.picking.line"
    _rec_name = 'picking_id'

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        self.description = self.product_id.name

        #self.available_qty = self.product_id.virtual_available
        self.forcasted_qty = self.product_id.qty_available

    product_id = fields.Many2one('product.product', string="Product", required=True)
    description = fields.Text(string="Description")
    qty = fields.Float(string="Quantity", default=1.0, required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit Of Measure")
    picking_id = fields.Many2one('internal.picking', string="Requisition Line")
    available_qty = fields.Float(string="Onhand Qty", compute='_compute_available_location_qty', store=True)
    forcasted_qty = fields.Float(string="Forcasted Qty", related="product_id.virtual_available", store=True)



    @api.depends('available_qty','picking_id')
    def _compute_available_location_qty(self):
        for rec in self:
            avail_qty = rec.product_id.with_context({'location': rec.picking_id.source_location_id.id}).qty_available
            rec.available_qty = avail_qty


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_confirm(self):
        for rec in self:
            pick = super(StockPicking, self).action_confirm()

            for line in rec.move_lines:
                avail_qty = line.product_id.with_context({'location': rec.location_id.id}).qty_available
                line.write({'available_qty': avail_qty})
            return pick

    picking_mat_picking_id = fields.Many2one('internal.picking', string="Internal Picking",
                                                 ondelete="cascade")


# analytic_id =fields.Many2one('account.analytic.account',string="Project")
# task_id = fields.Many2one('project.task', string="Task")



class StockMove(models.Model):
    _inherit = "stock.move"

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id):
    	res = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id)
    	# if self.picking_id.analytic_id:
    	# 	res['credit_line_vals']['analytic_account_id'] = self.picking_id.analytic_id.id
    	return res

   # available_qty = fields.Float(string="Available Qty")
