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
    fecha_inicio = fields.Datetime('Inicio  de la reparación', required=True, autodate=True)
    fecha_fin = fields.Datetime('Fin de la reparación', autodate=True)
    numero_mecanicos = fields.Integer("Número de mecánicos", compute="_compute_numero_mecanicos", readonly=True, size=8, store=True)
    numero_dias = fields.Integer("Número de días en la reparación", compute="_compute_numero_dias", size=8, readonly=True, store=True)
    horas_trabajadas = fields.Float("Horas de mano de obra del/los mecanico/s", (4, 2))
    precio_hora = fields.Selection([(20, "20€"),
                                    (25, "25€"),
                                    (30, "30€"),
                                    (35, "35€")], "Precio Hora", default=20)
    descuento = fields.Float("Descuento aplicado", (3, 2), required=True)
    iva = fields.Selection([("0.1", '10%'),
                          ("0.15", '15%'),
                          ("0.21", '21%'), ],
                          string='IVA', default='0.21', required=True)
    importe_total = fields.Float("Importe total", (4, 2), compute="_get_importe_total", readonly=True, store=True)
    state = fields.Selection([('en_proceso', 'En proceso'),
                              ('terminada', 'Terminada'),
                              ('facturada', 'Facturada'), ], 'Estado', default='en_proceso')
    
    vehiculo_id = fields.Many2one("upocar.vehiculo", string="Vehículo reparado", required=True)
    linea_reparacion_ids = fields.One2many("upocar.linea_reparacion", "reparacion_id", string="Repuestos utilizados")
    mecanico_ids = fields.Many2many("upocar.mecanico", string="Mecánicos")
    taller_id = fields.Many2one("upocar.taller", string="Taller", required=True)
    
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
    
    @api.depends('descuento', 'iva', 'linea_reparacion_ids', 'precio_hora', 'mecanico_ids')
    def _get_importe_total(self):
        for record in self:
            if record.horas_trabajadas > 0 and record.numero_mecanicos > 0 and record.precio_hora != False:
                record.importe_total = record.horas_trabajadas * record.numero_mecanicos * record.precio_hora
            if len(record.linea_reparacion_ids) > 0:
                for linea_reparacion in record.linea_reparacion_ids:
                    record.importe_total = record.importe_total + linea_reparacion.repuesto_id.precio * linea_reparacion.cantidad
            record.importe_total += record.importe_total * float(record.iva)
            record.importe_total -= record.importe_total * record.descuento / 100
    
    @api.onchange('fecha_fin', 'fecha_inicio')
    def _check_date(self):
        date_format = "%Y-%m-%d %H:%M:%S"
        if self.fecha_inicio and self.fecha_fin:
            dt1 = datetime.strptime(self.fecha_inicio, date_format)
            dt2 = datetime.strptime(self.fecha_fin, date_format)
            if dt2.__le__(dt1):
                raise models.ValidationError("Error, la fecha fin debe ser posterior a la fecha inicio")
                
    @api.onchange('linea_reparacion_ids', 'taller_id')
    def _check_repetitions_linea_reparacion(self):
        for linea_reparacion in self.linea_reparacion_ids:
            count = 0
            for linea_reparacion2 in self.linea_reparacion_ids:
                if linea_reparacion.repuesto_id.__eq__(linea_reparacion2.repuesto_id):
                    count += 1
            if count > 1:
                raise models.ValidationError("Repuesto \"" + linea_reparacion.repuesto_id.nombre_repuesto + "\" repetido. Aumenta la cantidad")
                break
    
    @api.onchange('mecanico_ids', 'taller_id')
    def _check_mecanico_in_taller(self):
        for mecanico in self.mecanico_ids:
            if not mecanico.taller_id.__eq__(self.taller_id):
                raise models.ValidationError("Error, el mecánico \"" + mecanico.nombre_apellidos + "\" no está en el taller en el que se realiza la reparación.")
            
    @api.onchange('linea_reparacion_ids', 'taller_id')
    def _check_repuesto_in_taller(self):
        enc = False
        for linea_reparacion in self.linea_reparacion_ids:
            for linea_taller in linea_reparacion.repuesto_id.linea_taller_ids:
                if self.taller_id == linea_taller.taller_id:
                    enc = True
                    break
            if not enc:
                raise models.ValidationError("Error, el repuesto \"" + linea_reparacion.repuesto_id.nombre_repuesto + "\" seleccionado no está en el taller en el que se realiza la reparación.")

    @api.one
    def btn_submit_to_terminada(self):
        error = ""
        repuesto = ""
        if self.precio_hora == False:
            error += "Precio por hora incorrecto.\n"
        if self.fecha_fin == False:
            error += "Fecha fin no introducida.\n"
        if self.horas_trabajadas <= 0:
            error += "Horas de mano de obra debe ser mayor de 0.\n"
        if len(self.mecanico_ids) < 1:
            error += "Ningún mecánico seleccionado.\n"
        if len(self.linea_reparacion_ids) > 0:
            for linea_reparacion in self.linea_reparacion_ids:
                for linea_taller in linea_reparacion.repuesto_id.linea_taller_ids:
                    if linea_taller.taller_id == self.taller_id:
                        if linea_taller.stock < linea_reparacion.cantidad:
                            repuesto = linea_reparacion.repuesto_id.nombre_repuesto
                            break
            if len(repuesto) > 0:
                error += "Stock insuficiente para el repuesto \"" + repuesto + "\", puede que se haya utilizado en otra reparación."
        if len(error) > 0:
            raise models.ValidationError("Error al terminar la reparación:\n" + error)
        else:
            for linea_reparacion in self.linea_reparacion_ids:
                for linea_taller in linea_reparacion.repuesto_id.linea_taller_ids:
                    if linea_taller.taller_id == self.taller_id:
                        linea_taller.stock -= linea_reparacion.cantidad
            self.write({"state":"terminada"})
        
    @api.one
    def btn_submit_to_facturada(self):
        self.write({"state":"facturada"})
