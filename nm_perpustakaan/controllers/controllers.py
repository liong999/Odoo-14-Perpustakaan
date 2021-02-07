# -*- coding: utf-8 -*-
# from odoo import http


# class NmPerpustakaan(http.Controller):
#     @http.route('/nm_perpustakaan/nm_perpustakaan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nm_perpustakaan/nm_perpustakaan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nm_perpustakaan.listing', {
#             'root': '/nm_perpustakaan/nm_perpustakaan',
#             'objects': http.request.env['nm_perpustakaan.nm_perpustakaan'].search([]),
#         })

#     @http.route('/nm_perpustakaan/nm_perpustakaan/objects/<model("nm_perpustakaan.nm_perpustakaan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nm_perpustakaan.object', {
#             'object': obj
#         })
