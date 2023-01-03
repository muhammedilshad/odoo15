from odoo import http
from odoo.http import request


class StageChange(http.Controller):
    @http.route(['/purchase/change_state'], type='json', auth='public')
    def tree_view_button(self, **kw):
        purchase_id = kw['data'][0]
        x = request.env['purchase.order'].browse(purchase_id)
        print(x)
