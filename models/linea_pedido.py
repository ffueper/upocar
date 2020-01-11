'''
Created on 11 ene. 2020

@author: usuario
'''

from odoo import models, fields, api


class linea_pedido(models.Model):
    _name = 'upocar.linea_pedido'
    
    cantidad = fields.Integer("Cantidad", size=3)
    
    repuesto_id = fields.Many2one("upocar.repuesto", string="Repuesto", required=True,ondelete="restrict")
    pedido_id = fields.Many2one("upocar.pedido", string="Pedido")
    precio_unidad=fields.Float("Precio por unidad",(4,2),required=True)
    
    @api.one
    @api.constrains("cantidad")
    def _check_cantidad(self):
        if self.cantidad <= 0:
            raise models.ValidationError("Error: se debe introducir una cantidad mayor o igual a 1 en los repuestos seleccionados\n")
    
    @api.constrains("precio_unidad")
    def _check_precio(self):
        if self.precio_unidad <= 0:
            raise models.ValidationError("Error: se debe introducir un precio mayor a 0\n")

    @api.constrains("repuesto_id")
    def _check_repuesto_in_taller(self):
        encontrado=False

        for taller in self.repuesto_id.taller_ids:
            if taller == self.pedido_id.taller_id:
                encontrado=True
                break
        if not encontrado:
            raise models.ValidationError("Error: se debe introducir el repuesto: "+self.repuesto_id.nombre_repuesto+" al  taller: "+self.pedido_id.taller_id.nombre)
