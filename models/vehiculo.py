'''
Created on 27 nov. 2019

@author: Pedro
'''
from odoo import api, models, fields

class vehiculo(models.Model):
    _name="upocar.vehiculo"
    
    matricula = fields.Char("Matrícula", required = True, size = 8)
    numero_bastidor = fields.Char("Número de bastidor", required = True, size=17)
    kilometros = fields.Integer("Kilómetros", required = True)
    reparacion_ids = fields.One2many("upocar.reparacion", "vehiculo_id", string="Reparaciones")
    #cliente_id = fields.Many2one("upocar.cliente", string="Dueño del vehiculo")
    
    #modelo_id = fields.Many2one("upocar.modelo", string="Modelo del vehiculo")