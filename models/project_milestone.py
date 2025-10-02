# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'
    
    project_manager_id = fields.Many2one(
        'res.users',
        string='Project Manager',
        related='project_id.user_id',
        store=True,  
        readonly=True,
        index=True
    )

