import io
import xlsxwriter
from odoo import models, fields
from odoo.tools import date_utils
from odoo.tools.safe_eval import json


class ReportButtonWizard(models.TransientModel):
    _name = 'attendance.report.wizard'

    employee_ids = fields.Many2many("hr.employee", string="Employee")

    def print_pdf(self):
        today_date = fields.Datetime.today()
        data_list = []
        for i in self.employee_ids:
            for rec in self.env['hr.attendance'].search([('employee_id', '=', i.id), ('check_in', '>', today_date)]):
                employee_name = rec.employee_id.name
                check_in = rec.check_in
                check_out = rec.check_out
                work_hours = round(rec.worked_hours, 2)
                record = {
                    'name_of_employee': employee_name,
                    'get_in': check_in,
                    'get_out': check_out,
                    'worked_hours': work_hours
                }
                data_list.append(record)
        dict_data = {
            'record': data_list
        }
        return self.env.ref('daily_attendance_report.attendance_pdf_action_report').report_action(self, data=dict_data)

    def print_excel_report(self):
        today_date = fields.Datetime.today()
        data_list = []
        for i in self.employee_ids:
            for rec in self.env['hr.attendance'].search([('employee_id', '=', i.id), ('check_in', '>', today_date)]):
                employee_name = rec.employee_id.name
                check_in = rec.check_in
                check_out = rec.check_out
                work_hours = round(rec.worked_hours, 2)
                record = {
                    'name_of_employee': employee_name,
                    'get_in': check_in,
                    'get_out': check_out,
                    'worked_hours': work_hours
                }
                data_list.append(record)
        dict_data = {
            'record': data_list
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'attendance.report.wizard',
                     'options': json.dumps(dict_data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Daily Attendance Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, dict_data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        table_head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '10px'})
        heading = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        sheet.merge_range('B2:F3', "Daily Attendance Report", heading)
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        row = 3
        col = 1
        sheet.write(row, col, 'Sl No', table_head)
        sheet.write(row, col + 1, 'Employee Name', table_head)
        sheet.write(row, col + 2, 'Check In Time', table_head)
        sheet.write(row, col + 3, 'Check Out Time', table_head)
        sheet.write(row, col + 4, 'Worked Hours', table_head)
        if dict_data.get('record'):
            if dict_data['record']:
                row = 3
                col = 1
                sl = 0

                for rec in dict_data.get('record'):
                    row = row + 1
                    sl = sl + 1
                    sheet.write(row, col, sl)
                    sheet.write(row, col + 1, rec.get('name_of_employee'))
                    sheet.write(row, col + 2, rec.get('get_in'))
                    sheet.write(row, col + 3, rec.get('get_out'))
                    sheet.write(row, col + 4, rec.get('worked_hours'))
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
