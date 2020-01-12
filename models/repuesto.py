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
    
    linea_taller_ids = fields.One2many("upocar.linea_taller", "repuesto_id", string="Taller")
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
        for linea_taller in self.linea_taller_ids:
            linea_taller.unlink()
        
    @api.onchange('linea_taller_ids')
    def _check_repetitions_linea_reparacion(self):
        for linea_taller in self.linea_taller_ids:
            count = 0
            for linea_taller2 in self.linea_taller_ids:
                if linea_taller.taller_id.__eq__(linea_taller2.taller_id):
                    count += 1
            if count > 1:
                raise models.ValidationError("Repuesto \"" + linea_taller.repuesto_id.nombre_repuesto + "\" repetido en el taller. Aumenta la cantidad")
                break
            
            