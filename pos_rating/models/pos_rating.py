from odoo import models, fields


class ProductRating(models.Model):
    _inherit = 'product.template'

    prod_rating = fields.Selection(string="Rating", selection=([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]), default="1")
