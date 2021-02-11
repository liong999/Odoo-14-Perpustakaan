from odoo import api, fields, models


class NmUsers(models.Model):
    _inherit = 'res.users'
    _description = 'User'

    mobile = fields.Char(string='Mobile')
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
        # Add to member
        group_member_id = self.env.ref('nm_perpustakaan.group_nm_perpustakaan_member')
        group_member_id.sudo().write({
            'users' : [(4, self.env.user.id)]
        })
        # Unlink non-member
        group_non_member_id = self.env.ref('nm_perpustakaan.group_nm_perpustakaan_non_member')
        group_non_member_id.sudo().write({
            'users' : [(3, self.env.user.id)]
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        # import ipdb;ipdb.set_trace()