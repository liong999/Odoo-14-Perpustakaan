from odoo import models, fields, api, _
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning

class NmPeminjaman(models.Model):
    _name = 'nm.peminjaman'
    _description = 'nm.peminjaman'
    _order = 'id desc'

    # 7: defaults methods
    def _get_default_user(self):
        return self.env.uid

    def _get_default_date(self):
        return date.today()

    def _get_default_end_date(self):
        return date.today() + relativedelta(days = 7)
        
    name = fields.Char(string='Name')
    state = fields.Selection(string='Status', selection=[('Draft','Draft'),('Request Peminjaman','Request Peminjaman'), ('Batal','Batal'), ('Ditolak', 'Ditolak'), ('Dipinjam', 'Dipinjam'),('Request Perpanjangan','Request Perpanjangan'), ('Konfirmasi Pengembalian', 'Konfirmasi Pengembalian'), ('Selesai', 'Selesai'),],default='Draft')
    date = fields.Date(string='Tanggal Peminjaman',default=_get_default_date)
    end_date = fields.Date(string='Tgl Pengembalian',default=_get_default_end_date)
    actual_end_date = fields.Date(string='Tgl Pengembalian Aktual')
    keterlambatan = fields.Integer(string='Keterlambatan',compute='_compute_keterlambatan')
    no_hp = fields.Char(string='No HP',compute='_compute_no_hp')
    
    
    user_id = fields.Many2one(comodel_name='res.users', string='Peminjam',default=_get_default_user)
    product_id = fields.Many2one(comodel_name='product.product', string='Buku')

    def _compute_no_hp(self):
        for record in self:
            if record.user_id:
                record.no_hp = record.user_id.mobile

    def _compute_keterlambatan(self):
        pass
        # today = date.today()
        # for record in self:
        #     if record.end_date:
        #         end_date = datetime.strptime(record.end_date, '%Y-%m-%d').date()
        #         if record.state == 'Dipinjam' and today > end_date:
        #             record.keterlambatan = today - end_date
    
    @api.model_create_multi
    def create(self, vals_list):
        self._check_workday()
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].sudo().get_sequence('PERPUS','PJM')
        sp = super(NmPeminjaman, self).create(vals_list)
        return sp

    def write(self, vals):
        self._check_workday()
        return super(NmPeminjaman, self).write(vals)
        
    def action_request(self):
        self.write({
            'state':'Request Peminjaman',
        })

    def action_confirm(self):
        if self.product_id.qty_avail == 0:
            raise Warning('Tidak bisa konfirmasi peminjaman! Buku ini sudah dipinjam semua.')
        qty_unavail = self.product_id.qty_unavail + 1
        self.state = 'Dipinjam'
        self.product_id.qty_unavail = qty_unavail

    def action_reject(self):
        self.write({
            'state':'Ditolak',
        })

    def action_extend(self):
        self.write({
            'end_date':self._get_default_end_date(),
            'state':'Dipinjam',
        })

    def action_request_perpanjangan(self):
        self.write({
            'state':'Request Perpanjangan',
        })

    def action_pengembalian(self):
        self.state = 'Konfirmasi Pengembalian'

    def action_cancel(self):
        self.state = 'Batal'

    def action_done(self):
        qty_unavail = self.product_id.qty_unavail - 1
        self.write({
            'state':'Selesai',
            'actual_end_date':self._get_default_date()           
        })
        self.product_id.qty_unavail = qty_unavail

    def _check_workday(self):
        if date.today().weekday() in (5,6):
            raise Warning("Gagal ! Hanya bisa dilakukan pada hari Senin - Jumat.")
