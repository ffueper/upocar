'''
Created on 11 ene. 2020

@author: usuario
'''

from odoo import models, fields, api


class linea_pedido(models.Model):
    _name = 'upocar.linea_pedido'
    
    cantidad = fields.Integer("Cantidad", size=3)
    
    repuesto_id = fields.Many2one("upocar.repuesto", string="Repuesto", required=True)
    pedido_id = fields.Many2one("upocar.pedido", string="Pedido")
    
    