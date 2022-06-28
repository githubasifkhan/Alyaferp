
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderReport(models.AbstractModel):
    _name = 'report.manager_all_approvals.sale_template'
    _description = 'Sale Order Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        for doc in docs:
            if doc.state not in ('approved','sent','sale','done'):
                raise ValidationError(_('Report Can Be printed Only After Approval'))

        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
        }


class PurchaseOrderReport(models.AbstractModel):
    _name = 'report.manager_all_approvals.purchase_template'
    _description = 'Purchase Order Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        for doc in docs:
            if doc.state not in ('approve','sent','purchase'):
                raise ValidationError(_('Report Can Be printed Only After Approval'))

        return {
            'doc_ids': docs.ids,
            'doc_model': 'purchase.order',
            'docs': docs,
        }