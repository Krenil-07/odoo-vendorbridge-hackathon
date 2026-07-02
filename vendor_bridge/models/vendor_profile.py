from odoo import models, fields

class VendorProfile(models.Model):
    _name = 'vendor.profile'
    _description = 'Vendor Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Vendor Name', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone')
    gst_number = fields.Char(string='GST Number')
    rating = fields.Float(string='AI Rating', default=0.0, help="Rating out of 5 stars")