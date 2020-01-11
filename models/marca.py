'''
Created on 27 nov. 2019

@author: Fernando Fuentes
'''
from odoo import models, fields, api


class marca(models.Model):
    _name = 'upocar.marca'
    
    _rec_name = "nombre_marca"
    nombre_marca = fields.Char('Nombre', size=64, required=True)
    
    modelo_ids = fields.One2many("upocar.modelo", "marca_id", string="Modelo de la marca", required=True)
