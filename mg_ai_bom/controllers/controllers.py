# -*- coding: utf-8 -*-
# from odoo import http


# class MgAiBom(http.Controller):
#     @http.route('/mg_ai_bom/mg_ai_bom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mg_ai_bom/mg_ai_bom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mg_ai_bom.listing', {
#             'root': '/mg_ai_bom/mg_ai_bom',
#             'objects': http.request.env['mg_ai_bom.mg_ai_bom'].search([]),
#         })

#     @http.route('/mg_ai_bom/mg_ai_bom/objects/<model("mg_ai_bom.mg_ai_bom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mg_ai_bom.object', {
#             'object': obj
#         })

