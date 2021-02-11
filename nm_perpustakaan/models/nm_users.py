from odoo import api, fields, models


class NmUsers(models.Model):
    _inherit = 'res.users'
    _description = 'User'

    mobile = fields.Char(string='Mobile',related='partner_id.mobile')
    nik = fields.Char(string='NIK')
    
    
    def action_daftar_member_wizard(self):
        form_id = self.env.ref('nm_perpustakaan.view_pendaftaran_member_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pendaftaran Member',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.users',
            'target':'new',
			'res_id': self._uid,
            'views': [(form_id, 'form')],
        }
    
    def action_register_member(self):
        pass