'''
Created on 27 nov. 2019

@author: pedro
'''

from odoo import models, fields, api


class linea_reparacion(models.Model):
    _name = 'upocar.linea_reparacion'
    
    cantidad = fields.Integer("Cantidad", size=3)
    stock = fields.Integer("Stock", size=3, compute="compute_stock", readonly=True)
    
    repuesto_id = fields.Many2one("upocar.repuesto", string="Repuesto", required=True)
    reparacion_id = fields.Many2one("upocar.reparacion", string="Reparacion")
    
    @api.one
    @api.constrains("cantidad")
    def check_cantidad(self):
        if self.cantidad <= 0:
            raise models.ValidationError("Error: se debe introducir una cantidad mayor o igual a 1 en los repuestos seleccionados\n")        
    
    @api.onchange("cantidad")
    def on_change_cantidad(self):
        resultado = {}
        if self.stock < self.cantidad:
            resultado = {'value': {'cantidad' : 0 },
                         'warning': {'title': 'Cantidad incorrecta',
                                     'message': 'Error, no hay suficiente stock del repuesto seleccionado'}
                         }
        return resultado
    
    @api.onchange("repuesto_id")
    def check_taller(self):
        resultado = {}
        if self.repuesto_id and not self.repuesto_id.taller_id.__eq__(self.reparacion_id.taller_id):
            resultado = {'value': {'repuesto_id' : "" },
                         'warning': {'title': 'Repuesto incorrecto',
                                     'message': 'El repuesto no corresponde al taller en el que se está realizando la reparación'}
                         }
        return resultado

    @api.depends("repuesto_id")
    def compute_stock(self):
        if self.repuesto_id:
            self.stock = self.repuesto_id.cantidad
