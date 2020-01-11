'''
Created on 11 jan. 2020

@author: usuario
'''

from odoo import models, fields, api

class pedido(models.Model):
    _name = 'upocar.pedido'
    
    _rec_name = "identificador"
    
    identificador = fields.Char('Identificador', size=64, required=True)
    
    taller_id = fields.Many2one("upocar.taller", "Taller")
    proveedor_id = fields.Many2one('upocar.proveedor', "Proveedor")
    linea_pedido_ids = fields.One2many("upocar.linea_pedido","pedido_id", string="Líneas reparacion")
