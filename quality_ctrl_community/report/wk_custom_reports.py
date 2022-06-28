# -*- coding: utf-8 -*-

from odoo import api, models


class QualityCustomReport(models.AbstractModel):
    _name = 'report.quality_ctrl_community.quality_worksheet'
    _description = 'Quality Worksheet Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['quality.check'].browse(docids).sudo()

        return {
            'doc_ids': docids,
            'doc_model': 'quality.check',
            'docs': docs,
        }

class QualityCustomInternalReport(models.AbstractModel):
    _name = 'report.quality_ctrl_community.quality_worksheet_internal'
    _description = 'Quality Worksheet Internal Report'
    _inherit = 'report.quality_ctrl_community.quality_worksheet'
