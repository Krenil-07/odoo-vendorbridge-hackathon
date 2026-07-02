import json
import requests
from odoo import models, fields, api
from odoo.exceptions import UserError

class VendorRFQ(models.Model):
    _name = 'vendor.rfq'
    _description = 'Request for Quotation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='RFQ Reference', required=True, default='New')
    product_name = fields.Char(string='Product Required', required=True, tracking=True)
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    expected_date = fields.Date(string='Expected Delivery Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent to Vendors'),
        ('done', 'Completed')
    ], string='Status', default='draft', tracking=True)
    
    quotation_ids = fields.One2many('vendor.quotation', 'rfq_id', string='Received Quotations')

    def action_analyze_quotations_ai(self):
        """Compiles bids, calls the Gemini API, and marks the recommended winner."""
        self.ensure_one()
        if not self.quotation_ids:
            raise UserError("No vendor bids found to analyze.")

        bids_data = []
        for q in self.quotation_ids:
            bids_data.append({
                'id': q.id,
                'vendor': q.vendor_id.name,
                'price': q.price,
                'delivery_time_days': q.delivery_time,
                'rating': q.vendor_id.rating
            })

        prompt = f"""
        You are an expert procurement ERP system. Analyze these vendor bids for the product '{self.product_name}' (Quantity: {self.quantity}).
        Select the absolute best option based on a balance of lowest price, fastest delivery, and high rating.
        Bids list: {json.dumps(bids_data)}
        Respond ONLY with a valid JSON object containing a single key 'recommended_bid_id' containing the ID integer of the winner.
        """

        # NOTE: Replace with your actual key before recording your demo video!
        api_key = "YOUR_GEMINI_API_KEY_HERE" 
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result_json = response.json()
                text_response = result_json['candidates'][0]['content']['parts'][0]['text']
                data = json.loads(text_response.strip())
                winner_id = data.get('recommended_bid_id')
                
                if winner_id:
                    self.quotation_ids.write({'ai_recommendation': False})
                    winning_bid = self.quotation_ids.browse(winner_id)
                    winning_bid.write({'ai_recommendation': True})
                    self.message_post(body=f"<b>AI Analysis Complete:</b> System recommends accepting the bid from {winning_bid.vendor_id.name}.")
            else:
                raise UserError(f"Gemini API returned an error status: {response.status_code}")
        except Exception as e:
            raise UserError(f"Failed to communicate with AI Engine: {str(e)}")