from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lodinpay_client_id = fields.Char(
        string="LodinPay Client ID",
        config_parameter='rtp_invoice_link.lodinpay_client_id'
    )
    
    lodinpay_client_secret = fields.Char(
        string="LodinPay Client Secret",
        config_parameter='rtp_invoice_link.lodinpay_client_secret'
    )
    
    lodinpay_device_static_id = fields.Char(
        string="LodinPay Device Static ID",
        config_parameter='rtp_invoice_link.lodinpay_device_static_id'
    )