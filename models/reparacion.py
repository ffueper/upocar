'''
Created on 27 nov. 2019

@author: Pedro
'''
from odoo import api, fields, models
from datetime import datetime


class reparacion(models.Model):
    _name = "upocar.reparacion"
    
    _rec_name = "descripcion"
    descripcion = fields.Char("Descripción de la reparacion", required=True, size=256)
    fecha_inicio = fields.Datetime('Inicio de la reparación', required=True, autodate=True)
    fecha_fin = fields.Datetime('Fin de la reparación', autodate=True)
    numero_mecanicos = fields.Integer("Número de mecánicos", compute="_compute_numero_mecanicos", readonly=True, size=8, store=True)
    numero_dias = fields.Integer("Número de días en la reparación", compute="_compute_numero_dias", size=8, readonly=True, store=True)
    horas_trabajadas = fields.Float("Horas de mano de obra del/los mecanico/s", (4, 2))
    precio_hora = fields.Selection([(20, "20€"),
                                    (25, "25€"),
                                    (30, "30€"),
                                    (35, "35€")], "Precio Hora")
    state = fields.Selection([('en_proceso', 'En proceso'),
                              ('terminada', 'Terminada'),
                              ('facturada', 'Facturada'), ], 'Estado', default='en_proceso')
    
    vehiculo_id = fields.Many2one("upocar.vehiculo", string="Vehículo reparado", required=True)
    factura_id = fields.Many2one("upocar.factura", string="Factura")
    linea_repuesto_ids = fields.One2many("upocar.linea_repuesto", "reparacion_id", string="Repuestos utilizados")
    mecanico_ids = fields.Many2many("upocar.mecanico", string="Mecánico")
    taller_id = fields.Many2one("upocar.taller", string="Taller")
    
    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_numero_dias(self):
        date_format = "%Y-%m-%d %H:%M:%S"
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                dt1 = datetime.strptime(record.fecha_inicio, date_format)
                dt2 = datetime.strptime(record.fecha_fin, date_format)
                diff = dt2 - dt1
                record.numero_dias = diff.days
    
    @api.depends('mecanico_ids')
    def _compute_numero_mecanicos(self):
        for record in self:
            if record.mecanico_ids:
                record.numero_mecanicos = len(record.mecanico_ids)
                
    @api.one
    def btn_submit_to_terminada(self):
        error = ""
        date_format = "%Y-%m-%d %H:%M:%S"
        if self.precio_hora == False:
            error += "Precio por hora incorrecto.\n"
        if self.fecha_fin == False:
            error += "Fecha fin no introducida.\n"
        else:
            dt1 = datetime.strptime(self.fecha_inicio, date_format)
            dt2 = datetime.strptime(self.fecha_fin, date_format)
            if dt1.__ge__(dt2):
                error += "Fecha fin anterior a la fecha de inicio.\n"
        if self.horas_trabajadas == 0:
            error += "Horas de mano de obra debe ser mayor de 0.\n"
        if len(self.mecanico_ids) < 1:
            error += "Ningún mecánico seleccionado."
        if len(error) > 0:
            raise models.ValidationError("Error al terminar la reparación:\n" + error)
        else:
            for linea_repuesto in self.linea_repuesto_ids:
                linea_repuesto.repuesto_id.cantidad -= linea_repuesto.cantidad
            self.write({"state":"terminada"})
        
    @api.one
    def btn_submit_to_facturada(self):
        if len(self.factura_id) > 0:
            raise models.ValidationError("Error al facturar la reparación: No se ha seleccionado/creado ninguna factura")
        else:
            self.write({"state":"facturada"})
