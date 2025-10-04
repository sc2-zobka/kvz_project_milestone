# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
import json

_logger = logging.getLogger(__name__)


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

    @api.model_create_multi
    def create(self, vals_list):
        """Al crear un milestone, asocia automáticamente la línea de venta"""
        milestones = super().create(vals_list)
        
        for milestone in milestones:
            if milestone.sale_line_id:
                update_vals = {'milestone_id': milestone.id}
                
                # Only update if fields are empty
                if not milestone.sale_line_id.project_id:
                    update_vals['project_id'] = milestone.project_id.id
                
                if not milestone.sale_line_id.project_manager:
                    update_vals['project_manager'] = milestone.project_manager_id.id
                
                milestone.sale_line_id.write(update_vals)
                print(json.dumps(update_vals.read()[0], indent=4, default=str))
    
        return milestones
    
    def write(self, vals):
        """Al modificar el milestone, actualiza la asociación con sale order line"""
        result = super().write(vals)
        
        if 'sale_line_id' in vals:
            for milestone in self:
                # Clear old associations
                old_lines = self.env['sale.order.line'].search([
                    ('milestone_id', '=', milestone.id),
                    ('id', '!=', milestone.sale_line_id.id if milestone.sale_line_id else False)
                ])
                if old_lines:
                    old_lines.write({'milestone_id': False})
                
                # Associate new line
                if milestone.sale_line_id:
                    milestone.sale_line_id.write({'milestone_id': milestone.id})
                    
        return result
    
    def unlink(self):
        """Al eliminar el milestone, limpia la referencia en sale order line"""
        # Guardar las líneas asociadas antes de eliminar
        sale_lines = self.mapped('sale_line_id')
        result = super().unlink()
        
        # Limpiar la referencia del milestone eliminado
        if sale_lines:
            sale_lines.write({'milestone_id': False})
            return result
