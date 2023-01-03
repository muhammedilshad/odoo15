from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    set_discount = fields.Float('E-commerce discount')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('e_commerce_discount.set_discount', self.set_discount)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            set_discount=params.get_param('e_commerce_discount.set_discount')
        )
        return res

    @api.onchange('set_discount')
    def get_discount(self):
        # print("dd")
        discount_value = self.env['ir.config_parameter'].sudo().get_param('e_commerce_discount.set_discount')
        record_id = self.env.ref('e_commerce_discount.no_code_needed_website_coupon_program')
        if self.set_discount == '0.0':
            record_id.active = False
        else:
            record_id.active = True
            record_id.discount_percentage = float(discount_value)
