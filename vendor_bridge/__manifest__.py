{
    'name': 'VendorBridge - Smart Procurement',
    'version': '1.0',
    'category': 'Inventory/Purchase',
    'summary': 'AI-powered Vendor Management and RFQ System',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/vendor_profile_views.xml',
        'views/vendor_rfq_views.xml',
    ],
    'installable': True,
    'application': True,
}