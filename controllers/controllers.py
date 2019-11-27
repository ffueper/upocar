# -*- coding: utf-8 -*-
from odoo import http

# class Upocar(http.Controller):
#     @http.route('/upocar/upocar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/upocar/upocar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('upocar.listing', {
#             'root': '/upocar/upocar',
#             'objects': http.request.env['upocar.upocar'].search([]),
#         })

#     @http.route('/upocar/upocar/objects/<model("upocar.upocar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('upocar.object', {
#             'object': obj
#         })