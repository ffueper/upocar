'''
Created on 17 nov. 2019

@author: Juan Carlos Ruiloba 
'''
from odoo import models,fields,api


class taller(models.Model):
    _name = 'upocar.taller'
    cif = fields.Char("CIF del taller",size=9,required=True)
    nombre = fields.Char("Nombre del taller",size=64,required=True)

    state_id = fields.Many2one("res.country.state", string='Provincia', help='Seleccionar una provincia/estado', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Pais', help='Seleccionar un pais', ondelete='restrict')
    city = fields.Char('Ciudad', help='Introducir la ciudad')
    direccion = fields.Char("Direccion del taller",size=64,required=True)
    hide = fields.Boolean(string='Hide', compute="_compute_hide")


    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}

    # Show Hide State selection based on Country
    @api.depends('country_id')
    def _compute_hide(self):
        if self.country_id:
            self.hide = False
        else:
            self.hide = True
   
    
    proveedor_ids=fields.Many2many("upocar.proveedor",string="Proveedor del taller")
    cliente_ids=fields.Many2many("upocar.cliente",string="Cliente del taller")
    #reparacion_ids=fields.One2many("upocar.reparacion", "reparacion_id", string = "Reparaciones del taller")
    #mecanico_ids=fields.One2many("upocar.mecanico","mecanico_id",string = "Mecanicos del taller")
    #repuesto_ids=fields.One2many("upocar.repuesto","repuesto_id",string = "Repuestos del taller")