from odoo import models, fields, api


class SaleOrderMargin(models.Model):
    _inherit = 'sale.order'

    total_margin = fields.Float("Total Margin", readonly=True)

    @api.onchange('order_line')
    def product_margin(self):
        total = 0
        for rec in self.order_line:
            cost = rec.product_id.standard_price
            sale = rec.price_unit
            if sale == 0:
                sale = rec.product_id.list_price
            if cost != 0 and sale != 0:
                rec.order_line_margin = sale - cost
            else:
                rec.order_line_margin = 0
            total += rec.order_line_margin
            self.total_margin = total


class SaleOrderLineMargin(models.Model):
    _inherit = 'sale.order.line'

    order_line_margin = fields.Float("Margin")
