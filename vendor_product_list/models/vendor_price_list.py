from odoo import models, fields, api


class VendorPriceList(models.Model):
    _inherit = 'purchase.order'

    is_vendor_product = fields.Boolean("Is Vendor Products")


class VendorPriceOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def vendor_product(self):
        # if self.order_id.is_vendor_product:
        #     print("wwwwwwww")
        #     list = []
        #     # if self.is_vendor_product:
        #     product_templ = self.env['product.product'].search([])
        #     for i in product_templ:
        #         for j in i.seller_ids:
        #             print(j.name.id)
        #             print(self.partner_id.id, "kkk")
        #             if j.name.id == self.partner_id.id:
        #                 list.append(i.id)
        #     print(list)
        #     return {'domain': {
        #         'product_id': [('id', 'in', list)]
        #     }}
        if self.order_id.is_vendor_product:
            return {'domain': {'product_id': [('seller_ids.name', '=', self.partner_id.id)]}}
