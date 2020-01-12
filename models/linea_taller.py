'''
Created on 12 ene. 2020

@author: pedro
'''
from odoo import api, fields, models


class linea_taller(models.Model):
    _name='upocar.linea_taller'
    
    _rec_name="repuesto_id"
    stock = fields.Integer(string="Stock", required=True)
    
    taller_id = fields.Many2one("upocar.taller", string="Taller")
    repuesto_id = fields.Many2one("upocar.repuesto", string="Repuesto")
