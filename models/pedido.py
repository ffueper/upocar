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
    linea_pedido_ids = fields.One2many("upocar.linea_pedido", "pedido_id", string="Líneas reparacion")
    iva = fields.Selection([("0.1", '10%'),
                          ("0.15", '15%'),
                          ("0.21", '21%'), ],
                          string='IVA', default='0.21', required=True)
    
    descuento = fields.Float("Descuento aplicado", (3, 2), required=True)
    importe_total = fields.Float("Importe total", (4, 2), compute="_get_importe_total", readonly=True, store=True)
    state = fields.Selection([('pendiente', 'Pendiente de aprobación'),
                              ('pagado', 'Pagado'),
                              ('entregado', 'Entregado'), ], 'Estado', default='pendiente')
    
    _sql_constraints = [('pedido_identificador_unique', 'UNIQUE (identificador)', 'El identificador debe ser único')]
       
    @api.one
    def btn_submit_to_pagado(self):
        if len(self.linea_pedido_ids) < 1:
            raise models.ValidationError('Debe de crear al menos 1 linea de pedidos')
        else:
            self.write({"state":"pagado"})
    
    @api.one
    def btn_submit_to_entregado(self):
        for linea in self.linea_pedido_ids:
            linea.repuesto_id.stock += linea.cantidad
        self.write({"state":"entregado"})
    
    @api.depends('descuento', 'iva', 'linea_pedido_ids')
    def _get_importe_total(self):
        self.importe_total = 0
        for linea in self.linea_pedido_ids:
            self.importe_total += linea.precio_unidad * linea.cantidad
        self.importe_total += self.importe_total * float(self.iva)
        self.importe_total -= self.importe_total * self.descuento / 100
        
    @api.onchange('linea_pedido_ids')
    def _check_repetitions_linea_pedido(self):
        for linea_pedido in self.linea_pedido_ids:
            count = 0
            for linea_pedido2 in self.linea_pedido_ids:
                if linea_pedido.repuesto_id.__eq__(linea_pedido2.repuesto_id):
                    count += 1
            if count > 1:
                raise models.ValidationError("Repuesto \"" + linea_pedido.repuesto_id.nombre_repuesto + "\" repetido. Aumenta la cantidad")
                break
