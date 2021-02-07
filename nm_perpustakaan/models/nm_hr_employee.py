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


class HrEmployeePerpustakaan(models.Model):
    _inherit = "hr.employee"

    is_member = fields.Boolean(string='Member?')
    
    
    @api.model
    def create(self,vals):
        create =  super(HrEmployeePerpustakaan,self).create(vals)
        create_user = self.create_user(vals['name'],vals['work_email'],create.id)
        create.user_id = create_user
        return create
    
    
    # 14: private methods
    def create_user(self,name,work_email,employee_id):
        users = self.env['res.users'].suspend_security().search([
            ('login','=',work_email),
            '|',
            ('active','=',False),('active','=',True)
        ])        
        if users:
            raise Warning('Perhatian ! \n Username sudah digunakan, silahkan buat username yang uniq.')

        user_create = self.env['res.users'].suspend_security().create([{
           'name':name,
           'login': work_email,
           'password':work_email,
           'email':work_email,
           'oauth_uid':work_email,
           'oauth_provider_id':3,
           'employee_id':employee_id,
        },],)

        return user_create.id