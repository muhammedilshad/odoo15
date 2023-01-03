from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/confirm'], type="http", auth="user", website=True)
    def confirm_quotation(self):
        value = request.env['sale.order'].search([])
        print(value)
        return request.render("website_quotation_confirmation.add_website_button")
