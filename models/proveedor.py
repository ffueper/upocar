'''
Created on 17 nov. 2019

@author: Juan Carlos Ruiloba
'''
from odoo import models,fields,api

class proveedor(models.Model):
    _name = 'upocar.proveedor'
    _rec_name = "nombre"
    cif = fields.Char("CIF del proveedor",size=9,required=True)
    nombre = fields.Char("Nombre del proveedor",size=64,required=True)
    telefono=fields.Integer("Telefono del proveedor",size=9,required=True)
    direccion = fields.Char("Direccion del proveedor",size=64)
    email = fields.Char("Correo electronico del proveedor",size=64)
    
    pedido_ids=fields.One2many("upocar.pedido","proveedor_id",string ="Pedidos al proveedor")
    
    _sql_constraints = [('proveedor_cif_unique','UNIQUE (cif)','El cif debe ser único')]

