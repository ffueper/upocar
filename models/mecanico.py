'''
Created on 29 nov. 2019

@author: usuario
'''
from odoo import api, fields, models


class mecanico(models.Model):
    _name = "upocar.mecanico"
    
    _rec_name = "nombre_apellidos"
    nombre = fields.Char("Nombre", size=32, required=True)
    apellidos = fields.Char("Apellidos", size=64, required=True)
    especialidad = fields.Char("Especialidad", size=64, required=True)
    num_reparaciones = fields.Integer(string="Número de reparaciones", compute="_compute_num_reparaciones", store=True)
    
    reparacion_ids = fields.Many2many("upocar.reparacion", string="Reparaciones")
    taller_id = fields.Many2one("upocar.taller", string="Taller")
    
    nombre_apellidos = fields.Char(compute="_compute_nombre_apellidos")
    
    @api.depends("nombre", "apellidos")
    def _compute_nombre_apellidos(self):
        for record in self:
            record.nombre_apellidos = record.nombre + " " + record.apellidos
    
    @api.depends("reparacion_ids")
    def _compute_num_reparaciones(self):
        for record in self:
            if(record.reparacion_ids):
                record.num_reparaciones = len(record.reparacion_ids)
