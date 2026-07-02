from odoo import models, fields

class VendorQuotation(models.Model):
    _name = 'vendor.quotation'
    _description = 'Vendor Quotation Bid'

    rfq_id = fields.Many2one('vendor.rfq', string='RFQ Reference', required=True, ondelete='cascade')
    vendor_id = fields.Many2one('vendor.profile', string='Vendor', required=True)
    price = fields.Float(string='Quoted Price', required=True)
    delivery_time = fields.Integer(string='Delivery Time (Days)')
    state = fields.Selection([
        ('pending', 'Pending Evaluation'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Bid Status', default='pending')
    ai_recommendation = fields.Boolean(string='Recommended by AI', default=False)