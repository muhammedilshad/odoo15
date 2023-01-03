import base64
from odoo import models


class StockReport(models.Model):
    _inherit = ['stock.quant']

    def automated_action(self):
        q_data = """select sq.id,pt.name,sq.quantity from stock_quant as sq
                   inner join product_product as pp on pp.id = sq.product_id
				   inner join product_template as pt on pt.id = pp.product_tmpl_id
                   order by sq.id"""
        self.env.cr.execute(q_data)
        s_data = self.env.cr.dictfetchall()
        data = {
            'query': s_data,
        }
        report_template = self.env.ref('stock_report.action_stock_pdf_report')._render_qweb_pdf(self.id, data=data)
        data_record = base64.b64encode(report_template[0])
        manager_email = self.env['res.users'].search([]).filtered(lambda ml: ml.has_group('stock.group_stock_manager'))
        print("manager email", manager_email)
        ir_values = {
            'name': "Stock Report",
            'type': 'binary',
            'datas': data_record,
            'mimetype': 'application/x-pdf',
        }
        data_id = self.env['ir.attachment'].create(ir_values)

        email_values = {
            'email_to': manager_email.email,
            'attachment_ids': data_id}
        template_id = self.env.ref('stock_report.stock_report_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True, email_values=email_values)
