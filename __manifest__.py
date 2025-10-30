{
    "name": "Lodin Pay",
    "version": "17.0.1.0.1",
    "category": "Accounting",
    "summary": "Generates a RTP payment link using lodinPay when invoice is posted.",
    "author": "Effyis Groupe",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        "views/account_move_view.xml",
        "views/res_config_settings_view.xml",
        # "views/report_invoice_rtp.xml",  # ✅ NEW LINE

    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "auto_install": False
}
