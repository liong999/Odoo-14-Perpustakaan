from odoo import models, fields, api, _
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning

class NmRequestBuku(models.Model):
    _name = 'nm.request.buku'
    _description = 'nm.request.buku'
    _order = 'id desc'

    # 7: defaults methods
    def _get_default_user(self):
        return self.env.uid

    def _get_default_date(self):
        return date.today()

    def _get_default_end_date(self):
        return date.today() + relativedelta(days = 7)
        
    name = fields.Char(string='Name')
    judul = fields.Char(string='Judul')
    penulis = fields.Char(string='Penulis')
    penerbit = fields.Char(string='Penerbit')
    state = fields.Selection(string='Status', selection=[('Di Request','Di Request'),('Selesai','Selesai')],default='requested')
    date = fields.Date(string='Tanggal Pengajuan Buku',default=_get_default_date)
    no_hp = fields.Char(string='No HP',compute='_compute_no_hp')
        
    user_id = fields.Many2one(comodel_name='res.users', string='Peminjam',default=_get_default_user)
    
    def _compute_no_hp(self):
        for record in self:
            if record.user_id:
                record.no_hp = record.user_id.mobile

    def action_request_buku_wizard(self):
        form_id = self.env.ref('nm_perpustakaan.view_konfirmasi_request_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pengajuan Buku',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'nm.request.buku',
            'target':'new',
            'views': [(form_id, 'form')],
        }
    
    
    @api.model_create_multi
    def create(self, vals_list):
        self._check_workday()
        for vals in vals_list:
            requested = self.env['nm.request.buku'].sudo().search([
                ('judul','=',vals.get('judul')),
                ('penulis','=',vals.get('penulis')),
                ('penerbit','=',vals.get('penerbit')),
                ('state','=','Di Request'),
            ])
            if requested:
                raise Warning('Buku ini sudah di request :) Mohon tunggu sampai bukunya tersedia ya')
            vals['name'] = self.env['ir.sequence'].sudo().get_sequence('PERPUS','REQ')
        sp = super(NmRequestBuku, self).create(vals_list)
        return sp

    def write(self, vals):
        self._check_workday()
        return super(NmRequestBuku, self).write(vals)

    def action_done(self):
        self.write({
            'state':'Selesai',
        })
        
    def _check_workday(self):
        if date.today().weekday() in (5,6):
            raise Warning("Gagal ! Hanya bisa dilakukan pada hari Senin - Jumat.")
