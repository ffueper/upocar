'''
Created on 27 nov. 2019

@author: usuario
'''

from odoo import models, fields, api

class repuesto(models.Model):
    _name = 'upocar.repuesto'
    
    _rec_name = "nombre_repuesto"
    nombre_repuesto = fields.Char('Nombre', size=64, required=True)
    descripcion = fields.Char('Descripcion', size=256, required=True)
    precio = fields.Float('Precio', (7, 2))
    cantidad = fields.Integer("Cantidad",size=3)
    
    taller_id = fields.Many2one("upocar.taller", "Taller")
    modelo_id = fields.Many2one('upocar.modelo', "Modelo")
    proveedor_id = fields.Many2one('upocar.proveedor', "Proveedor")
    linea_repuesto_ids = fields.One2many("upocar.linea_repuesto", "repuesto_id", string="Líneas repuesto")