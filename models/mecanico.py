'''
Created on 29 nov. 2019

@author: usuario
'''
from odoo import api, fields, models

class mecanico(models.Model):
    _name = "upocar.mecanico"
    
    nombre = fields.Char("Nombre", size=32, required = True)
    apellidos = fields.Char("Apellidos", size=64, required = True)
    especialidad = fields.Char("Especialidad", size=64, required = True)
    
    reparacion_ids = fields.Many2many("upocar.reparacion", string="Reparaciones")
    taller_id = fields.Many2one("upocar.taller", string="Taller")