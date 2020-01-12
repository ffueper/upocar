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
    stock = fields.Integer("Stock", size=3)
    
    taller_ids = fields.Many2many("upocar.taller", string="Taller")
    modelo_id = fields.Many2one('upocar.modelo', "Modelo", required=True)
    linea_reparacion_ids = fields.One2many("upocar.linea_reparacion", "repuesto_id", string="Líneas reparacion")
    linea_pedido_ids = fields.One2many("upocar.linea_pedido", "repuesto_id", string="Línea pedidos")
    
    #@api.constrains('taller_ids')
    #def _check_taller_ids(self):
    #    if len(self.taller_ids) < 1:
    #        raise models.ValidationError("Es necesario seleccionar un taller al menos")
    
    def delete_repuesto(self):
        for linea_pedido in self.linea_pedido_ids:
            linea_pedido.unlink()
        for linea_reparacion in self.linea_reparacion_ids:
            linea_reparacion.unlink()
        self.write({'taller_ids':[ (5,) ]})