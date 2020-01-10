'''
Created on 27 nov. 2019

@author: grupo 5
'''
from odoo import models, fields, api


class modelo(models.Model):
    _name = 'upocar.modelo'
    
    _rec_name = "nombre_modelo"
    nombre_modelo = fields.Char('Nombre', size=64, required=True)

    marca_id = fields.Many2one("upocar.marca", string="Marca del modelo")

    repuesto_ids = fields.One2many("upocar.repuesto", "modelo_id", string="Repuestos")
    vehiculo_ids = fields.One2many("upocar.vehiculo", "modelo_id", string="Vehículos")
