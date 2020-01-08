'''
Created on 17 nov. 2019

@author: Juan Carlos Ruiloba
'''
from odoo import models, fields, api


class cliente(models.Model):
    _name = 'upocar.cliente'
    
    _rec_name = 'nombreyapellidos'
    dni = fields.Char("Dni del cliente", size=9, required=True)
    nombre = fields.Char("Nombre del cliente", size=64, required=True)
    apellidos = fields.Char("Apellidos del cliente", size=64, required=True)
    telefono = fields.Integer("Telefono del cliente", size=9, required=True)
    nombreyapellidos = fields.Char("Nombre y apellidos", compute="compute_nombre_y_apellidos")
    
    _sql_constraints = [('cliente_dni_unique','UNIQUE (dni)','El dni debe ser único')]

    
    vehiculo_id = fields.One2many("upocar.vehiculo",'cliente_id',string ="Vehiculos del cliente")
    taller_id = fields.Many2many("upocar.taller", string="Taller del cliente")
    
    @api.depends('nombre', 'apellidos')
    def compute_nombre_y_apellidos(self):
        self.nombreyapellidos = self.nombre + " " + self.apellidos
