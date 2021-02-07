from odoo import models, fields, api, _

class Sequence(models.Model):
    _inherit = "ir.sequence"

    def get_sequence(self,doc_code, prefix):
        seq_name = '{0}/{1}'.format(prefix, doc_code)

        ids = self.search([('name','=',seq_name)])
        if not ids:
            prefix = '/%(y)s/%(month)s/'
            prefix = seq_name + prefix
            vals = {
                'name':seq_name,
                'implementation': 'standard',
                'prefix': prefix,
                'padding':5
            }
            ids = super(Sequence,self).create(vals)

        return self.get_id(ids.id)
