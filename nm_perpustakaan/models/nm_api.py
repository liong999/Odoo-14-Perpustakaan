#!/usr/bin/python
#-*- coding: utf-8 -*-

# 1: imports of python lib
import functools
import werkzeug.wrappers
try:
    import simplejson as json
except ImportError:
    import json
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta,datetime as dt,date
from dateutil.relativedelta import relativedelta
# 2: import of known third party lib

# 3:  imports of odoo
import odoo
from odoo import models, fields, api, _
from odoo import http

# 4:  imports from odoo modules
from odoo.http import request
from odoo.http import Response
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

# 5: local imports

# 6: Import of unknown third party lib


_logger = logging.getLogger(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

def invalid_token(method):
    _logger.error("Token is expired or invalid!")    
    return invalid_response(401, 'invalid_token', "Token is expired or invalid!",method)

def check_valid_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get('access_token')
        method = request.httprequest.method
        if not access_token:
            info = "Missing access token in request header!"
            error = 'access_token_not_found'
            _logger.error(info)
            return invalid_response(400, error, info,method)

        access_token_data = request.env['oauth.access_token'].sudo().search(
            [('token', '=', access_token)], order='id DESC', limit=1)

        if access_token_data._get_access_token(user_id=access_token_data.user_id.id) != access_token:
            return invalid_token(method)

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)

    return wrap

def valid_response(status, data):
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        response=json.dumps(data, cls=JSONEncoder),
    )

def invalid_response(status, error, info, method):
    if method == 'POST':
        return {
            'error': error,
            'error_descrip': info,
            'message': info,
            'status': status,
        }
    
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        response=json.dumps({
            'error': error,
            'error_descrip': info,
        }),
    )


class ControllerREST(http.Controller):
    @http.route('/api/perpustakaan/get_books', methods=['GET'], type='http', auth='none', csrf=False)
    @check_valid_token
    def get_books(self,**post):
        limit = 10
        offset = 0
        ORDER = "ORDER BY sp.date DESC"
        string = False
        url = str(request.httprequest.url).split('/api/')[0]
        
        WHERE = ""
        
        if 'string' in post:
            WHERE += " AND (product.name ilike '%%%s%%' OR product.penulis ilike '%%%s%%')" %(string)

        query = """
            SELECT
                product.name
                ,product.penulis
                ,product.pengarang
                ,product.qty
                ,product.qty - product.qty_unavail as qty_avail
                , '%s' || '/web/content/product.product/' || product.id || '/image_128' as url_image
            FROM product_product as product
            WHERE 1=1
            AND product.active IS TRUE
            %s
            %s
            LIMIT %d
            OFFSET %d
        """ %(url,WHERE,ORDER,limit,offset)
        request._cr.execute (query)
        ress =  request._cr.dictfetchall()
        result = {
            'message':'ok',
            'data':ress,
        }
        return valid_response(200,result)

    @http.route('/api/perpustakaan/post_request_peminjaman', methods=['POST'], type='json', auth='none', csrf=False)
    @check_valid_token
    def post_request_peminjaman(self,**post):
        uid = request.session.uid
        product_id = post.get('product_id',False)
        if not product_id:
            return invalid_response(401,'data_not_found','Peminjaman - product_id is required','POST')
        
        product_obj = request.env['product.product'].sudo().browse(int(product_id))
        
        if not product_obj:
            return invalid_response(401,'data_not_found','Peminjaman - product not found','POST')

        try:
            peminjaman = request.env['nm.peminjaman'].sudi().create({
                'product_id':product_id,
                'user_id':uid,
            })
            peminjaman.action_request()
        except Exception as e:
            return invalid_response(401,'request_failed', e, 'POST')
    
    @http.route('/api/perpustakaan/post_request_perpanjangan', methods=['POST'], type='json', auth='none', csrf=False)
    @check_valid_token
    def post_request_perpanjangan(self,**post):
        uid = request.session.uid
        peminjaman_id = post.get('id',False)
        if not peminjaman_id:
            return invalid_response(401,'data_not_found','Peminjaman - peminjaman_id is required','POST')
        
        peminjaman_obj = request.env['nm.peminjaman'].sudo().browse(int(peminjaman_id))
        
        if not peminjaman_obj:
            return invalid_response(401,'data_not_found','Peminjaman - peminjaman not found','POST')

        try:
            peminjaman_obj.action_request_perpanjangan()
        except Exception as e:
            return invalid_response(401,'request_failed', e, 'POST')
    
    
    @http.route('/api/perpustakaan/post_pengembalian', methods=['POST'], type='json', auth='none', csrf=False)
    @check_valid_token
    def post_pengembalian(self,**post):
        uid = request.session.uid
        peminjaman_id = post.get('id',False)
        if not peminjaman_id:
            return invalid_response(401,'data_not_found','Peminjaman - peminjaman_id is required','POST')
        
        peminjaman_obj = request.env['nm.peminjaman'].sudo().browse(int(peminjaman_id))
        
        if not peminjaman_obj:
            return invalid_response(401,'data_not_found','Peminjaman - peminjaman not found','POST')

        try:
            peminjaman_obj.action_pengembalian()
        except Exception as e:
            return invalid_response(401,'request_failed', e, 'POST')
    