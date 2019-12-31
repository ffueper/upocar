'''
Created on 27 nov. 2019

@author: usuario
'''
from odoo import api, fields, models


class factura(models.Model):
    _name = "upocar.factura"
    
    _rec_name = "numero_factura"
    numero_factura = fields.Integer("Número de factura", required=True, size=20)
    fecha_facturacion = fields.Datetime("Fecha de la factura", autodate=True, required=True)
    descuento = fields.Float("Descuento aplicado", (3, 2), required=True)
    importe_total = fields.Float("Importe total", (4, 2), compute="_get_importe_total", readonly=True, store=True)
    iva = fields.Selection([("0.1", '10%'),
                          ("0.15", '15%'),
                          ("0.21", '21%')],
                          string='IVA', required=True)
    
    reparacion_id = fields.Many2one("upocar.reparacion", string="Reparación", required=True)
    
    @api.depends('reparacion_id', 'descuento', 'iva')
    def _get_importe_total(self):
        for record in self:
            if record.reparacion_id:
                record.importe_total = record.reparacion_id.horas_trabajadas * record.reparacion_id.numero_mecanicos * record.reparacion_id.precio_hora
            #if len(record.reparacion_id.repuesto_ids) > 0:
            #    for repuesto in record.reparacion_id.repuesto_ids:
            #        record.importe_total = record.importe_total + repuesto.precio * repuesto.cantidad
            record.importe_total = record.importe_total - (record.importe_total * record.descuento / 100)
            record.importe_total = record.importe_total + (record.importe_total * float(record.iva))
