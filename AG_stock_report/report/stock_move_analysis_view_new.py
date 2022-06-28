# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from odoo import tools
from odoo.exceptions import UserError, AccessError

class N2NStockMoveAnalysisView(models.Model):
	_name = "n2n.stock.move.analysis.view"
	_description = "N2N Stock Move Analysis"
	_auto = False
	_order = 'date'
	_rec_name = 'date'

	date = fields.Date(string="Date")
	move_id = fields.Many2one('stock.move',string='Stock  Move')
	product_id = fields.Many2one('product.product', string='Product')
	location = fields.Many2one('stock.location',string='Location')
	qty = fields.Float(string='Quantity')
	value = fields.Float(string='Value')
	origin = fields.Char(string='Origin')
	ref = fields.Char(string='Reference')
	warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse')
	batch_name = fields.Char(string="Batch Name")
	source = fields.Many2one('stock.location', string='Source')
	destination = fields.Many2one('stock.location', string='Destination')
	categ_id = fields.Many2one('product.category',string='Category')
	# nn_pdt_group_id = fields.Many2one('nn.product.group',string='Group')
	# nn_pdt_sub_group_id = fields.Many2one('nn.product.sub.group',string='Sub Group')
	# nn_pdt_type_id = fields.Many2one('nn.product.type',string='Type')
	src_usage = fields.Char(string='Src Usage')
	des_usage = fields.Char(sring='Des Usage')
	move = fields.Char(string='Move')
	type = fields.Char(string='Operation Type')
	uom_id = fields.Many2one('uom.uom',string='UOM')
	partner_id = fields.Many2one('res.partner',string='Partner')
	# analytic_id =fields.Many2one('account.analytic.account',string="Cost Center")
	# task_id = fields.Many2one('project.task', string="Task")
	price_unit = fields.Float(string='Unit Price')

	
	def init(self):  
		tools.drop_view_if_exists(self.env.cr, self._table)
		self.env.cr.execute("""
		CREATE OR REPLACE VIEW n2n_stock_move_analysis_view AS
		SELECT row_number() OVER () AS id,
		--sp.scheduled_date::timestamp::date AS date,
		CASE
            WHEN (sp.id is null) THEN (sm.date)::date
            ELSE (sp.scheduled_date)::date
        END AS date,
		CASE
            WHEN (sp.id is null) THEN (sm.reference)
            ELSE (sm.origin)
        END AS origin,
		sm.id AS move_id,
		sm.product_id,
		svl.quantity AS qty,
		svl.value AS value,
		--sm.origin AS origin, 
		sp.name AS ref,
		sm.warehouse_id,
		sml.lot_name AS batch_name,
		sm.location_id AS source,
		sm.location_dest_id AS destination,
		sp.partner_id,
		pt.categ_id,
		svl.unit_cost as price_unit,
		sm.location_id AS location,
		pt.uom_id,
		srcloc.usage AS src_usage,
		desloc.usage AS des_usage,
			CASE
				WHEN (svl.quantity < (0)::numeric) THEN 'Outgoing'::text
				ELSE 'Incoming'::text
			END AS move,
			CASE
				WHEN (((srcloc.usage)::text = 'internal'::text) AND ((desloc.usage)::text = 'production'::text)) THEN 'Production'::text
				WHEN (((srcloc.usage)::text = 'production'::text) AND ((desloc.usage)::text = 'internal'::text)) THEN 'Production'::text
				WHEN (((srcloc.usage)::text = 'internal'::text) AND ((desloc.usage)::text = 'customer'::text)) THEN 'Sales'::text
				WHEN (((srcloc.usage)::text = 'customer'::text) AND ((desloc.usage)::text = 'internal'::text)) THEN 'Sales Return'::text
				WHEN (((srcloc.usage)::text = 'supplier'::text) AND ((desloc.usage)::text = 'internal'::text)) THEN 'Purchase'::text
				WHEN (((srcloc.usage)::text = 'internal'::text) AND ((desloc.usage)::text = 'supplier'::text)) THEN 'Purchase Return'::text
				WHEN (((srcloc.usage)::text = 'internal'::text) AND ((desloc.usage)::text = 'inventory'::text)) THEN 'Inventory Adjustment'::text
				WHEN (((srcloc.usage)::text = 'inventory'::text) AND ((desloc.usage)::text = 'internal'::text)) THEN 'Inventory Adjustment'::text
				ELSE 'xxxx'::text
			END AS type
	   FROM (((((((stock_move sm
		 LEFT JOIN stock_location srcloc ON ((sm.location_id = srcloc.id)))
		 LEFT JOIN stock_location desloc ON ((sm.location_dest_id = desloc.id)))
		 LEFT JOIN stock_picking sp ON ((sm.picking_id = sp.id)))
		 LEFT JOIN stock_move_line sml ON ((sm.id = sml.move_id)))
		 LEFT JOIN stock_valuation_layer svl ON ((sm.id = svl.stock_move_id)))
		 JOIN product_product pp ON ((sm.product_id = pp.id)))
		 JOIN product_template pt ON ((pp.product_tmpl_id = pt.id)))
		 
		  GROUP BY sp.id,sm.product_id, sp.scheduled_date, sm.id, desloc.id, srcloc.id,
		  svl.quantity,
		  svl.unit_cost,
		  svl.value,
		  sm.origin,sp.name, sm.warehouse_id, sml.lot_name, sm.location_id, sm.location_dest_id, sp.partner_id, pt.categ_id, pt.uom_id, srcloc.usage, desloc.usage;
		""")
