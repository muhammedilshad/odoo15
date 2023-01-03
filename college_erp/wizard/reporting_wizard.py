import io
import xlsxwriter
from odoo import models, fields
import json

from odoo.exceptions import MissingError
from odoo.tools import date_utils


class ReportingWizard(models.TransientModel):
    _name = 'college.marksheet.reporting'

    report_type = fields.Selection([('student wise', 'Student Wise'), ('class wise', 'Class Wise')], 'Report',
                                   default='student wise')
    student_id = fields.Many2one('student.college.erp', "student")
    class_id = fields.Many2one('class.college.erp', "Class")
    sem_id = fields.Many2one('semester.college.erp', "semester")
    exam_type = fields.Selection(string="Type of exam", selection=[('internal', 'Internal'),
                                                                   ('semester', 'Semester'),
                                                                   ('unit test', 'Unit test')])
    stud_fname = fields.Char()
    stud_lname = fields.Char()
    s_class = fields.Char()
    type_of_exam = fields.Char()
    r_result = fields.Char()
    r_course = fields.Char()
    r_academic_yr = fields.Char()
    total_student = fields.Integer()
    pass_student = fields.Integer()
    fail_stud = fields.Integer(default=0)
    r_ratio = fields.Float()

    def print_pdf(self):
        if self.student_id:
            student = self.env['mark.sheet.college.erp'].search_count(
                [('ms_student_id', '=', self.student_id.id)])
            print(student)
            if student == 0:
                raise MissingError("No marksheets found for this student..!")

        if self.report_type == 'student wise':
            sql_query = """select st.first_name, syl.syllabus_subject, syl.syllabus_pass_mark, msp.marksheet_subject_mark, msp.marksheet_subject_pass_or_fail from mark_sheet_college_erp as ms
                           inner join student_college_erp as st on st.id = ms.ms_student_id inner join mark_sheet_subjects_college_erp as msp on msp.marksheet_sem_id = ms.id
                           inner join syllabus_college_erp as syl on msp.marksheet_subject_name_id = syl.id inner join exam_college_erp as ex on ms."ms_exam_id" = ex.id """
            if self.student_id:
                query_1 = """ where ms.ms_student_id = '%s' """ % self.student_id.id
                self.stud_fname = self.student_id.first_name
                self.stud_lname = self.student_id.last_name
                self.s_class = self.student_id.student_class_id.name_of_class
                result = self.env['mark.sheet.college.erp'].search([('ms_student_id', '=', self.student_id.id),
                                                                    ('mark_sheet_Semester_id', '=', self.sem_id.id),
                                                                    ('ms_exam_id.exam_type', '=', self.exam_type)])
                for i in result:
                    if i.Pass_or_Fail:
                        self.r_result = "Pass"
                    else:
                        self.r_result = "Fail"
                sql_query += query_1
            if self.sem_id:
                semester_q = """ AND ms."mark_sheet_Semester_id" = %s """ % self.sem_id.id
                sql_query += semester_q
            if self.exam_type:
                exam_type_q = """ AND ex.exam_type = '%s' """ % self.exam_type
                sql_query += exam_type_q
            self.env.cr.execute(sql_query)
            s_data = self.env.cr.dictfetchall()
            data = {
                'student_id': self.student_id.first_name,
                'sem_id': self.sem_id,
                'exam_type': self.exam_type,
                'query': s_data,
                'r_result': self.r_result,
                's_class': self.s_class,
            }
            return self.env.ref('college_erp.action_report_std_wise_marksheet').report_action(self, data=data)

        if self.report_type == "class wise":
            if self.class_id:
                self.s_class = self.class_id.name_of_class
                self.r_course = self.class_id.course_of_class_id.name
                self.r_academic_yr = self.class_id.academic_year_for_class_id
                self.total_student = self.env['student.college.erp'].search_count(
                    [('student_class_id', '=', self.class_id.id)])
                if self.exam_type:
                    self.pass_student = self.env['mark.sheet.college.erp'].search_count(
                        [('mark_sheet_Class_id', '=', self.class_id.id),
                         ('ms_exam_id.exam_type', '=', self.exam_type),
                         ('Pass_or_Fail', '=', True)])
                    self.fail_stud = self.env['mark.sheet.college.erp'].search_count(
                        [('mark_sheet_Class_id', '=', self.class_id.id),
                         ('ms_exam_id.exam_type', '=', self.exam_type),
                         ('Pass_or_Fail', '=', False)])
                    self.r_ratio = (self.pass_student / self.total_student) * 100
                    self.r_ratio = round(self.r_ratio, 2)
                    qry1 = """ select ms.id, std.first_name, ms.total_get_mark, ms.max_mark_total, ms."Pass_or_Fail" 
                    from mark_sheet_college_erp as ms inner join student_college_erp as std on ms.ms_student_id = std.id 
                    inner join class_college_erp as cls on ms."mark_sheet_Class_id" = cls.id and std.student_class_id = cls.id 
                    inner join exam_college_erp as exam on ms.ms_exam_id = exam.id where cls.id = '%d' """ % self.class_id.id
                    qry2 = """AND exam.exam_type = '%s' """ % self.exam_type
                    qry1 += qry2
                    qry3 = """order by ms.id"""
                    qry1 += qry3
                    self.env.cr.execute(qry1)
                    stud_data = self.env.cr.dictfetchall()
                    sub_qry = """select distinct syl.syllabus_subject from mark_sheet_college_erp as ms 
                    inner join exam_college_erp as exam on exam.id = ms.ms_exam_id inner join 
                    mark_sheet_subjects_college_erp as msub on ms.id = msub.marksheet_sem_id 
                    inner join syllabus_college_erp as syl on msub.marksheet_subject_name_id = syl.id 
                    inner join class_college_erp as cls on ms."mark_sheet_Class_id" = cls.id 
                    where exam.exam_type = '%s' """ % self.exam_type
                    sub_qry1 = """and cls.id = '%d' """ % self.class_id.id
                    sub_qry += sub_qry1
                    self.env.cr.execute(sub_qry)
                    sub_data = self.env.cr.dictfetchall()
                    m_qry = """select ms.id, msub.marksheet_subject_mark from mark_sheet_college_erp as ms 																																														inner join exam_college_erp as exam on exam.id = ms.ms_exam_id 
                    inner join mark_sheet_subjects_college_erp as msub on ms.id = msub.marksheet_sem_id 
                    inner join class_college_erp as cls on ms."mark_sheet_Class_id" = cls.id 
                    inner join syllabus_college_erp as syl on msub.marksheet_subject_name_id = syl.id
                    where exam.exam_type = '%s' """ % self.exam_type
                    m_qry1 = """and cls.id = '%d' """ % self.class_id.id
                    m_qry += m_qry1
                    m_qry2 = """order by ms.id, msub.marksheet_subject_mark DESC"""
                    m_qry += m_qry2
                    self.env.cr.execute(m_qry)
                    mark_data = self.env.cr.dictfetchall()
                    record = {
                        'r_ratio': self.r_ratio,
                        'total_student': self.total_student,
                        'exam_type': self.exam_type,
                        's_class': self.s_class,
                        'r_course': self.r_course,
                        'pass_student': self.pass_student,
                        'fail_stud': self.fail_stud,
                        'stud_data': stud_data,
                        'mark_data': mark_data,
                        'sub_data': sub_data
                    }
                    return self.env.ref('college_erp.action_report_class_wise_marksheet').report_action(self,
                                                                                                        data=record)

    def print_xlsx_report(self):
        if self.report_type == 'student wise':
            if self.student_id:
                student = self.env['mark.sheet.college.erp'].search_count(
                    [('ms_student_id', '=', self.student_id.id)])
                print(student)
                if student == 0:
                    raise MissingError("No marksheets found for this student..!")
            sql_query = """select st.first_name, syl.syllabus_subject, syl.syllabus_pass_mark, msp.marksheet_subject_mark, msp.marksheet_subject_pass_or_fail from mark_sheet_college_erp as ms
                           inner join student_college_erp as st on st.id = ms.ms_student_id inner join mark_sheet_subjects_college_erp as msp on msp.marksheet_sem_id = ms.id
                           inner join syllabus_college_erp as syl on msp.marksheet_subject_name_id = syl.id inner join exam_college_erp as ex on ms."ms_exam_id" = ex.id """
            if self.student_id:
                query_1 = """ where ms.ms_student_id = '%s' """ % self.student_id.id
                self.stud_fname = self.student_id.first_name
                self.stud_lname = self.student_id.last_name
                self.s_class = self.student_id.student_class_id.name_of_class
                result = self.env['mark.sheet.college.erp'].search([('ms_student_id', '=', self.student_id.id),
                                                                    ('mark_sheet_Semester_id', '=', self.sem_id.id),
                                                                    ('ms_exam_id.exam_type', '=', self.exam_type)])
                for i in result:
                    if i.Pass_or_Fail:
                        self.r_result = "Pass"
                    else:
                        self.r_result = "Fail"
                sql_query += query_1
            if self.sem_id:
                semester_q = """ AND ms."mark_sheet_Semester_id" = %s """ % self.sem_id.id
                sql_query += semester_q
            if self.exam_type:
                exam_type_q = """ AND ex.exam_type = '%s' """ % self.exam_type
                sql_query += exam_type_q
            self.env.cr.execute(sql_query)
            s_data = self.env.cr.dictfetchall()
            data = {
                'student_id': self.student_id.first_name,
                'sem_id': self.sem_id,
                'exam_type': self.exam_type,
                'query': s_data,
                'r_result': self.r_result,
                's_class': self.s_class
            }
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'college.marksheet.reporting',
                         'options': json.dumps(data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Student Report',
                         },
                'report_type': 'xlsx',
            }
        if self.report_type == "class wise":
            if self.class_id:
                self.s_class = self.class_id.name_of_class
                self.r_course = self.class_id.course_of_class_id.name
                self.r_academic_yr = self.class_id.academic_year_for_class_id
                self.total_student = self.env['student.college.erp'].search_count(
                    [('student_class_id', '=', self.class_id.id)])
                if self.exam_type:
                    self.pass_student = self.env['mark.sheet.college.erp'].search_count(
                        [('mark_sheet_Class_id', '=', self.class_id.id),
                         ('ms_exam_id.exam_type', '=', self.exam_type),
                         ('Pass_or_Fail', '=', True)])
                    self.fail_stud = self.env['mark.sheet.college.erp'].search_count(
                        [('mark_sheet_Class_id', '=', self.class_id.id),
                         ('ms_exam_id.exam_type', '=', self.exam_type),
                         ('Pass_or_Fail', '=', False)])
                    if self.fail_stud == 0:
                        self.fail_stud = 0
                    self.r_ratio = (self.pass_student / self.total_student) * 100
                    self.r_ratio = round(self.r_ratio, 2)
                    qry1 = """ select ms.id, std.first_name, ms.total_get_mark, ms.max_mark_total, ms."Pass_or_Fail" 
                    from mark_sheet_college_erp as ms inner join student_college_erp as std on ms.ms_student_id = std.id 
                    inner join class_college_erp as cls on ms."mark_sheet_Class_id" = cls.id and std.student_class_id = cls.id 
                    inner join exam_college_erp as exam on ms.ms_exam_id = exam.id where cls.id = '%d' """ % self.class_id.id
                    qry2 = """AND exam.exam_type = '%s' """ % self.exam_type
                    qry1 += qry2
                    qry3 = """order by ms.id"""
                    qry1 += qry3
                    self.env.cr.execute(qry1)
                    stud_data = self.env.cr.dictfetchall()
                    sub_qry = """select distinct syl.id, syl.syllabus_subject from mark_sheet_college_erp as ms 
                    inner join exam_college_erp as exam on exam.id = ms.ms_exam_id inner join 
                    mark_sheet_subjects_college_erp as msub on ms.id = msub.marksheet_sem_id 
                    inner join syllabus_college_erp as syl on msub.marksheet_subject_name_id = syl.id 
                    inner join class_college_erp as cls on ms."mark_sheet_Class_id" = cls.id 
                    where exam.exam_type = '%s' """ % self.exam_type
                    sub_qry1 = """and cls.id = '%d' """ % self.class_id.id
                    sub_qry += sub_qry1
                    sub_qry2 = """order by syl.id ASC"""
                    sub_qry += sub_qry2
                    self.env.cr.execute(sub_qry)
                    sub_data = self.env.cr.dictfetchall()
                    m_qry = """select ms.id, msub.marksheet_subject_mark from mark_sheet_college_erp as ms 																																														inner join exam_college_erp as exam on exam.id = ms.ms_exam_id 
                    inner join mark_sheet_subjects_college_erp as msub on ms.id = msub.marksheet_sem_id 
                    inner join class_college_erp as cls on ms."mark_sheet_Class_id" = cls.id 
                    inner join syllabus_college_erp as syl on msub.marksheet_subject_name_id = syl.id
                    where exam.exam_type = '%s' """ % self.exam_type
                    m_qry1 = """and cls.id = '%d' """ % self.class_id.id
                    m_qry += m_qry1
                    m_qry2 = """order by ms.id, msub.marksheet_subject_mark DESC"""
                    m_qry += m_qry2
                    self.env.cr.execute(m_qry)
                    mark_data = self.env.cr.dictfetchall()

                    data = {
                        'r_ratio': self.r_ratio,
                        'c_exam_type': self.exam_type,
                        'c_class': self.s_class,
                        'r_course': self.r_course,
                        'academic_year': self.r_academic_yr,
                        'total_student': self.total_student,
                        'pass_student': self.pass_student,
                        'fail_stud': self.fail_stud,
                        'stud_data': stud_data,
                        'mark_data': mark_data,
                        'sub_data': sub_data
                    }
                    return {
                        'type': 'ir.actions.report',
                        'data': {'model': 'college.marksheet.reporting',
                                 'options': json.dumps(data, default=date_utils.json_default),
                                 'output_format': 'xlsx',
                                 'report_name': 'Class Report',
                                 },
                        'report_type': 'xlsx',
                    }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head_table = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '10px'})
        head_name = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        head_class = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '15px'})
        side_panel = workbook.add_format({'bold': True})
        if data.get('c_class'):
            if data['c_class']:
                sheet.merge_range('B1:E2', data['c_class'], head_name)
        if data.get('s_class'):
            if data['s_class']:
                sheet.write(2, 2, data['s_class'], head_class)
        if data.get('exam_type'):
            if data['exam_type']:
                sheet.write(4, 0, 'Exam Type', side_panel)
                sheet.write(4, 1, data['exam_type'])
        if data.get('c_exam_type'):
            if data['c_exam_type']:
                sheet.write(4, 0, 'Exam Type', side_panel)
                sheet.write(4, 1, data['c_exam_type'])
        if data.get('total_student'):
            if data['total_student']:
                sheet.write(5, 0, 'Total Students:', side_panel)
                sheet.write(5, 1, data['total_student'])
        if data.get('pass_student'):
            if data['pass_student']:
                sheet.write(6, 0, 'Total Pass:', side_panel)
                sheet.write(6, 1, data['pass_student'])
        if data.get('fail_stud'):
            if data['fail_stud']:
                sheet.write(7, 0, 'Total Fail:', side_panel)
                sheet.write(7, 1, data['fail_stud'])
        if data.get('r_ratio'):
            if data['r_ratio']:
                sheet.write(8, 0, 'Pass Ratio:', side_panel)
                sheet.write(8, 1, data['r_ratio'])
        if data.get('r_result'):
            if data['r_result']:
                sheet.write(5, 0, 'Result', side_panel)
                sheet.write(5, 1, data['r_result'])
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 10)
        sheet.set_column('D:D', 13)
        sheet.set_column('E:E', 10)
        sheet.set_column('F:F', 10)
        sheet.set_column('G:G', 10)
        sheet.set_column('H:H', 10)
        sheet.set_column('I:I', 10)
        sheet.set_column('J:J', 10)
        if data.get('query'):
            s_data = data.get('query')
            if s_data:
                row = 7
                col = 0
                sheet.write(row, col, 'SL.No', head_table)
                sheet.write(row, col + 1, 'Subject', head_table)
                sheet.write(row, col + 2, 'Pass Mark', head_table)
                sheet.write(row, col + 3, 'Obtained Mark', head_table)
                sheet.write(row, col + 4, 'Pass/Fail', head_table)
                if not data.get('student_id'):
                    sheet.write(row, col + 5, 'Students', head_table)
                rows = 7
                cols = 0
                sl = 0
                for rec in s_data:
                    rows = rows + 1
                    sl = sl + 1
                    sheet.write(rows, cols, sl)
                    sheet.write(rows, cols + 1, rec.get('syllabus_subject'))
                    sheet.write(rows, cols + 2, rec.get('syllabus_pass_mark'))
                    sheet.write(rows, cols + 3, rec.get('marksheet_subject_mark'))
                    if rec.get('marksheet_subject_pass_or_fail'):
                        sheet.write(rows, cols + 4, "Pass")
                    else:
                        sheet.write(rows, cols + 4, "Fail")
                    if not data.get('student_id'):
                        sheet.write(rows, cols + 5, rec.get('first_name'))
        if data.get('sub_data'):
            subject_data = data.get('sub_data')
            if subject_data:
                row = 11
                col = 0
                sheet.write(row, col, 'SL.No', head_table)
                sheet.write(row, col + 1, 'Student', head_table)
                for sub in subject_data:
                    sheet.write(row, col + 2, sub.get('syllabus_subject'), head_table)
                    col += 1
                col += 1
                sheet.write(row, col + 1, 'Obtained Mark', head_table)
                sheet.write(row, col + 2, 'Total Mark', head_table)
                sheet.write(row, col + 3, 'Result', head_table)
                if data.get('stud_data'):
                    student_data = data.get('stud_data')
                    rows = 11
                    sl = 0
                    for rec in student_data:
                        cols = 0
                        rows = rows + 1
                        sl = sl + 1
                        sheet.write(rows, cols, sl)
                        sheet.write(rows, cols + 1, rec.get('first_name'))
                        if data.get('mark_data'):
                            mark_data = data.get('mark_data')
                            for m in mark_data:
                                if rec.get('id') == m.get('id'):
                                    sheet.write(rows, cols + 2, m.get('marksheet_subject_mark'))
                                    cols += 1
                            cols += 1
                        sheet.write(rows, cols + 1, rec.get('total_get_mark'))
                        sheet.write(rows, cols + 2, rec.get('max_mark_total'))
                        if rec.get('Pass_or_Fail'):
                            sheet.write(rows, cols + 3, "Pass")
                        else:
                            sheet.write(rows, cols + 3, "Fail")
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
