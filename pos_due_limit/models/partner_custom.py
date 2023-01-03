from odoo import models, fields


class CustomResPartner(models.Model):
    _inherit = "res.partner"

    due_limit = fields.Char("Purchase Limit")
