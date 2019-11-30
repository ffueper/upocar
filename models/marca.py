'''
Created on 27 nov. 2019

@author: Fernando Fuentes
'''
from odoo import models, fields, api

class marca(models.Model):
    _name = 'upocar.marca'
    
    nombre_marca = fields.Char('Nombre', size=64, required=True)
    
    modelo_ids = fields.Many2many("upocar.modelo", string="Modelo de la marca")