'''
Created on 27 nov. 2019

@author: usuario
'''

from odoo import models, fields, api

class repuesto(models.Model):
    _name = 'upocar.repuesto'
    
    nombre_repuesto = fields.Char('Nombre', size=64, required=True)
    descripcion = fields.Char('Descripcion', size=256, required=True)
    precio = fields.Float('Precio', (7, 2))
    cantidad = fields.Integer("Cantidad",size=3)
    
    taller_id = fields.Many2one("upocar.taller", "Taller")
    modelo_id = fields.Many2one('upocar.modelo', "Modelo")
    proveedor_id = fields.Many2one('upocar.proveedor', "Proveedor")
    reparacion_id = fields.Many2one("upocar.reparacion", "Reparación")