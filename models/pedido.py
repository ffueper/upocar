'''
Created on 11 jan. 2020

@author: usuario
'''

from odoo import models, fields, api


class pedido(models.Model):
    _name = 'upocar.pedido'
    
    _rec_name = "identificador"
    
    identificador = fields.Char('Identificador', size=64, required=True)
    
    taller_id = fields.Many2one("upocar.taller", "Taller", required=True)
    proveedor_id = fields.Many2one('upocar.proveedor', "Proveedor", required=True)
    linea_pedido_ids = fields.One2many("upocar.linea_pedido","pedido_id", string="Líneas reparacion")
    state = fields.Selection([('pendiente', 'Pendiente de aprobación'),
                              ('pagado', 'Pagado'),
                              ('entregado', 'Entregado'), ], 'Estado', default='pendiente')
    
    _sql_constraints = [('pedido_identificador_unique', 'UNIQUE (identificador)', 'El identificador debe ser único')]

    
    @api.one
    def btn_submit_to_pagado(self):
        if len(self.linea_pedido_ids)<1:
            raise models.ValidationError('Debe de crear al menos 1 linea de pedidos')
        else:
            self.write({"state":"pagado"})
    
    @api.one
    def btn_submit_to_entregado(self):
        for linea in self.linea_pedido_ids:
            linea.repuesto_id.cantidad+=linea.cantidad
        self.write({"state":"entregado"})