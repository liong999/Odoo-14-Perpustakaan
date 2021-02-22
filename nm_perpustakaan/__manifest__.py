# -*- coding: utf-8 -*-
{
    'name': "nm_perpustakaan",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','rest_api','ow_backend_theme_v14'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/nm_peminjaman_view.xml',
        'views/nm_product_view.xml',
        'views/nm_product_admin_view.xml',
        'views/nm_pendaftaran.xml',
        'views/nm_users_view.xml',
        'views/nm_request_buku_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
