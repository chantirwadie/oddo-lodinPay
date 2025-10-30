from odoo import api, fields, models
import requests
import hashlib
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

LODING_GUIDE_MSG = (
    "⚠️ RTP Link unavailable.\n"
    "You must register in LodinPay:\n"
    "➡ https://merchant-preprod.lodinpay.com/auth/login\n\n"
    "Then retrieve:\n"
    "- Client ID\n"
    "- Client Secret\n"
    "- Device Static ID\n\n"
    "And configure them in:\n"
    "Settings → LodinPay Settings"
)

class AccountMove(models.Model):
    _inherit = "account.move"

    rtp_payment_link = fields.Char(
        string="RTP Payment Link",
        readonly=True,
        help="Auto-generated RTP payment link from LodinPay."
    )

    def action_post(self):
        res = super().action_post()
        ICP = self.env['ir.config_parameter'].sudo()

        lodinpay_api_url = "https://api-preprod.lodinpay.com/merchant-service/pay/order/pos"

        client_id = ICP.get_param("rtp_invoice_link.lodinpay_client_id")
        client_secret = ICP.get_param("rtp_invoice_link.lodinpay_client_secret")
        device_static_id = ICP.get_param("rtp_invoice_link.lodinpay_device_static_id")

        if not all([client_id, client_secret, device_static_id]):
            _logger.error("Missing LodinPay credentials!")
            for record in self:
                record.rtp_payment_link = LODING_GUIDE_MSG
            return res

        for record in self:
            try:
                amount = round(record.amount_total, 2)
                formatted_date = datetime.utcnow().strftime("%Y-%m-%d %H")

                security_code = hashlib.sha256(
                    f"{amount:.2f}{client_id}{device_static_id}{formatted_date}".encode()
                ).hexdigest()

                payload = {
                    "clientId": client_id,
                    "clientSecret": client_secret,
                    "deviceStaticId": device_static_id,
                    "amount": f"{amount:.2f}",
                    "securityCode": security_code,
                }

                headers = {"Content-Type": "application/json; charset=UTF-8"}
                response = requests.post(lodinpay_api_url, json=payload, headers=headers, timeout=10)

                if response.status_code == 200:
                    result = response.json()
                    record.rtp_payment_link = result.get("url") or LODING_GUIDE_MSG
                else:
                    record.rtp_payment_link = LODING_GUIDE_MSG

            except Exception as e:
                _logger.exception("Error generating RTP payment link")
                record.rtp_payment_link = LODING_GUIDE_MSG

        return res
