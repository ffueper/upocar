'''
Created on 27 nov. 2019

@author: usuario
'''
from odoo import api, fields, models

class factura(models.Model):
    _name="upocar.factura"
    
    numero_factura = fields.Integer("Número de factura", required = True, size=20)
    fecha_facturacion = fields.Datetime("Fecha de la factura", autodate=True, required = True)
    descuento = fields.Float("Descuento aplicado", (3,2))
    importe_total = fields.Float("Importe total", (4,2), compute = "_get_importe_total", readonly = True, store = True)
    reparacion_id = fields.Many2one("upocar.reparacion", string="Reparacion")
    
    #@api.depends('reparacion.horas_trabajadas')
    #@api.onchange('reparacion_id')
    #def _onchange_reparacion_id(self):
        #self.importe_total = 10
        #for record in self:
        #    if record.reparacion.horas_trabajadas:
        #        self.importe_total = 10 * record.reparacion.horas_trabajadas;
    
    @api.depends('reparacion_id.horas_trabajadas','reparacion_id.precio_hora','reparacion_id.numero_mecanicos','descuento')
    def _get_importe_total(self):
        for record in self:
            if record.reparacion_id:
                importe_parcial = record.reparacion_id.horas_trabajadas * record.reparacion_id.numero_mecanicos * record.reparacion_id.precio_hora
                record.importe_total = importe_parcial - (importe_parcial * record.descuento/100)