# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

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
                milestone.sale_line_id.milestone_id = milestone.id
        
        return milestones
    
    def write(self, vals):
        """Al modificar el milestone, actualiza la asociación con sale order line"""
        result = super().write(vals)
        
        # Si se modifica la sale_line_id asociada
        if 'sale_line_id' in vals:
            for milestone in self:
                # Limpiar asociaciones anteriores de este milestone
                old_lines = self.env['sale.order.line'].search([
                    ('milestone_id', '=', milestone.id),
                    ('id', '!=', milestone.sale_line_id.id if milestone.sale_line_id else False)
                ])
                if old_lines:
                    old_lines.write({'milestone_id': False})
                
                # Asociar la nueva línea si existe
                if milestone.sale_line_id:
                    milestone.sale_line_id.milestone_id = milestone.id
                    
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
