#!/usr/bin/python
#-*- coding: utf-8 -*-

# 1: imports of python lib

# 2: import of known third party lib

# 3:  imports of odoo
from odoo import models, fields, api, _

# 4:  imports from odoo modules
from odoo.exceptions import UserError, ValidationError

# 5: local imports

# 6: Import of unknown third party lib


class ProductProductPerpustakaan(models.Model):
    _inherit = "product.product"

    qty = fields.Integer(string='Qty')
    qty_avail = fields.Integer(string='Qty Available',compute='_compute_qty_avail')
    qty_unavail = fields.Integer(string='Qty Unvailable')
    penulis = fields.Char(string='Penulis')
    penerbit = fields.Char(string='Penerbit')

    
    def _compute_qty_avail(self):
        for record in self:
            record.qty_avail = record.qty - record.qty_unavail
    