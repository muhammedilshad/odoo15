from odoo import models, fields, exceptions, _
from odoo.exceptions import UserError
# from odoo.osv.osv import osv
import xlrd
import base64


class TestModelWizard(models.TransientModel):
    _name = 'lot.serial.wizard'

    xlsx_file = fields.Binary(string="Import Lot/Serial")

    def action_done(self):
        if not self.xlsx_file:
            raise exceptions.MissingError('Please upload spreadsheet file')
        try:
            book = xlrd.open_workbook(file_contents=(base64.decodebytes(self.xlsx_file)))
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheet in book.sheets():
            for row in range(sheet.nrows):
                if row > 0:
                    row_values = sheet.row_values(row)
            self.env['stock.production.lot'].sudo().create({
                'name': int(row_values[0]),
                'ref': row_values[1],
                'product_id': int(row_values[2]),
                'create_date': row_values[3],
                'company_id': int(row_values[4])
            })
        self.success_msg()

    def success_msg(self):
        active_id = self.env.context.get('active_id')
        self.env['stock.production.lot'].browse(active_id).message_post(body="Successfully Imported")