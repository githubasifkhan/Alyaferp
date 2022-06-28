from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class QualityCheckInherited(models.Model):
    _inherit = "quality.check"

    quality_state = fields.Selection([
        ('none', 'To do'),
        ('under','Under Inspection'),
        ('pass', 'Approved'),
        ('fail', 'Rejected')], string='Status', tracking=True,
        default='none', copy=False)

    @api.depends('quality_state')
    def under_inspection(self):
        for rec in self:
            rec.write({'quality_state': 'under'})


class QualityCheckWizardInherited(models.TransientModel):
    _inherit = 'quality.check.wizard'
    
    def under_inspection(self):

        self.current_check_id.under_inspection()
        return self.action_generate_next_window()
