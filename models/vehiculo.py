'''
Created on 27 nov. 2019

@author: Pedro
'''
from odoo import api, models, fields


class vehiculo(models.Model):
    _name = "upocar.vehiculo"
    
    _rec_name = "matricula"
    matricula = fields.Char("Matrícula", required=True, size=8)
    numero_bastidor = fields.Char("Número de bastidor", required=True, size=17)
    kilometros = fields.Integer("Kilómetros", required=True)
    numero_reparaciones = fields.Integer("Número de reparaciones", compute="_compute_numero_reparaciones", readonly=True, store=True)
    marca = fields.Char("Marca", compute="_compute_marca_from_modelo")
    
    reparacion_ids = fields.One2many("upocar.reparacion", "vehiculo_id", string="Reparaciones")
    cliente_id = fields.Many2one("upocar.cliente", string="Dueño del vehiculo")
    modelo_id = fields.Many2one("upocar.modelo", string="Modelo del vehiculo")
    
    @api.depends('reparacion_ids')
    def _compute_numero_reparaciones(self):
        for record in self:
            if record.reparacion_ids:
                record.numero_reparaciones = len(record.reparacion_ids)
            else:
                record.numero_reparaciones = 0

    @api.depends('modelo_id')
    def _compute_marca_from_modelo(self):
        for record in self:
            if record.modelo_id:
                record.marca = record.modelo_id.marca_id.nombre_marca
