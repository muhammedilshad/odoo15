from odoo import models, api


class LastPurchasePrice(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        print("bnmmmmmmmmmmmm")
        fn_overwrite = super(LastPurchasePrice, self).button_confirm()
        # line = self.env['purchase.order.line'].search([('order_id', '=', self.id)])
        for i in self.order_line:
            i.product_id.standard_price = i.price_unit
        return fn_overwrite
