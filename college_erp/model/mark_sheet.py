from odoo import models, fields, api


class Mark_sheet(models.Model):
    _name = 'mark.sheet.college.erp'
    _rec_name = "mark_sheet_Semester_id"

    ms_student_id = fields.Many2one('student.college.erp', string="Student", domain=[('exam_flag', '=', True)],
                                    store=True)
    ms_exam_id = fields.Many2one("exam.college.erp", string="Exam", store=True)
    mark_sheet_Class_id = fields.Many2one("class.college.erp", string="Class", related="ms_exam_id.exam_class",
                                          store=True)
    mark_sheet_Course_id = fields.Many2one("course.college.erp", string="Course",
                                           related="mark_sheet_Class_id.course_of_class_id", store=True)
    mark_sheet_Semester_id = fields.Many2one("semester.college.erp", string="Semester",
                                             related="mark_sheet_Class_id.semester_for_class_id", store=True)
    Pass_or_Fail = fields.Boolean("Pass or Fail", default=False)
    rank = fields.Char("Rank")
    total_get_mark = fields.Float(store=True)
    max_mark_total = fields.Float(store=True)
    marksheet_subject_ids = fields.One2many('mark.sheet.subjects.college.erp', 'marksheet_sem_id', store=True)

    @api.onchange('marksheet_subject_ids')
    def _compute_obtained(self):
        self.total_get_mark = 0
        self.max_mark_total = 0
        for rec in self.marksheet_subject_ids:
            self.total_get_mark = self.total_get_mark + rec.marksheet_subject_mark
            self.max_mark_total = self.max_mark_total + rec.marksheet_subject_maximum_mark
        # print(self.total_get_mark)
        # print(self.max_mark_total)


class marksheet_subjects(models.Model):
    _name = 'mark.sheet.subjects.college.erp'

    marksheet_subject_name_id = fields.Many2one('syllabus.college.erp', string="Subject")
    marksheet_subject_maximum_mark = fields.Integer(string="Maximum mark",
                                                    related="marksheet_subject_name_id.syllabus_maximum_mark")
    marksheet_subject_pass_mark = fields.Integer(string="Pass mark", related="marksheet_subject_name_id"
                                                                             ".syllabus_pass_mark")
    marksheet_subject_mark = fields.Integer("Mark")
    marksheet_sem_id = fields.Many2one('mark.sheet.college.erp', string="Semester")
    marksheet_subject_pass_or_fail = fields.Boolean("Pass or Fail", default=False, compute="mark_greater_pass_mark",
                                                    store=True)

    @api.depends('marksheet_subject_mark', 'marksheet_subject_pass_mark')
    def mark_greater_pass_mark(self):
        for record in self:
            if record.marksheet_subject_mark >= record.marksheet_subject_pass_mark:
                record.marksheet_subject_pass_or_fail = True
            else:
                record.marksheet_subject_pass_or_fail = False
