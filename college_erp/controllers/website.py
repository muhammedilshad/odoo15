import base64
from urllib import request
from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/create'], type="http", auth="user", website=True)
    def college_admission(self):
        return request.render("college_erp.template_website_form")

    @http.route(['/admission'], type="http", auth="user", website=True)
    def college_admission_tree(self, **kw):
        admission = request.env['admission.college.erp'].sudo().search([])
        admission_tree = []
        for rec in admission:
            data = {
                'admission_no': rec.admission_no,
                'f_name': rec.first_name,
                'father_name': rec.father,
                'email': rec.email,
                'phone': rec.phone
            }
            admission_tree.append(data)
        list_1 = {
            'data': admission_tree
        }
        return request.render("college_erp.admission_tree_view", list_1)

    @http.route(['/admission/submit/'], type="http", auth="user", website=True)
    def college_admission_submit(self, **post):
        data = post.get('file')
        if data:
            data_file = data.read()
            decrypt_file = base64.encodebytes(data_file)
        else:
            decrypt_file = ''
        rec = request.env['admission.college.erp'].sudo().create({

            'first_name': post.get('first_name'),
            'father': post.get('father'),
            'email': post.get('email'),
            'communication_address': post.get('address'),
            'transfer_certificate': decrypt_file
        })
        vals = {
            'op_model': rec,
        }
        return request.render("college_erp.tmp_customer_form_success", vals)
