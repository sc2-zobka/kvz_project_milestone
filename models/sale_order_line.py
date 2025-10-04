# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    milestone_id = fields.Many2one(
        comodel_name='project.milestone',
        string='Milestone',
        readonly=True,
        help='Milestone associated with this sale order line',
    )
    
    milestone_deadline = fields.Date(
        string='Milestone Deadline',
        related='milestone_id.deadline',
        store=True,  
        readonly=True,
    )