'''
Created on 27 nov. 2019

@author: Pedro
'''
from odoo import api, fields, models
from datetime import datetime

class reparacion(models.Model):
    _name="upocar.reparacion"
    
    descripcion = fields.Char("Descripción de la reparacion", required = True, size = 256)
    fecha_inicio = fields.Datetime('Inicio de la reparación',required=True, autodate = True)
    fecha_fin = fields.Datetime('Fin de la reparación', autodate = True)
    numero_mecanicos = fields.Integer("Número de mecánicos", compute="_compute_numero_mecanicos", readonly = True, size=8, store = True)
    numero_dias = fields.Integer("Número de días en la reparación", compute="_compute_numero_dias", size=8, readonly = True, store = True)
    horas_trabajadas = fields.Float("Horas de mano de obra del/los mecanico/s",(4,2), required = True)
    precio_hora = fields.Selection([(20,"20€"),
                                    (25,"25€"),
                                    (30,"30€"),
                                    (35,"35€")],"Precio Hora")
    
    vehiculo_id = fields.Many2one("upocar.vehiculo", string="Vehículo reparado")
    factura_id = fields.Many2one("upocar.factura", string="Factura")
    #repuesto_ids = fields.One2many("upocar.repuesto", "repuesto_ids", string="Repuestos utilizados")
    mecanico_ids = fields.Many2many("upocar.mecanico", string="Mecánico")
    taller_id = fields.Many2one("upocar.taller", string="Taller")
    
    @api.depends('fecha_inicio','fecha_fin')
    def _compute_numero_dias(self):
        date_format = "%Y-%m-%d %H:%M:%S"
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                dt1 = datetime.strptime(record.fecha_inicio, date_format)
                dt2 = datetime.strptime(record.fecha_fin, date_format)
                diff = dt2-dt1
                record.numero_dias = diff.days
    
    @api.depends('mecanico_ids')
    def _compute_numero_mecanicos(self):
        for record in self:
            if record.mecanico_ids:
                record.numero_mecanicos = len(record.mecanico_ids)
                