from odoo import models, fields, api


class Exam(models.Model):
    _name = 'exam.college.erp'
    _rec_name = 'exam_name'
    _sql_constraints = [
        ('promotion_exam', 'unique(promotion_exam)', 'Already promoted using this exam!')
    ]
    exam_type = fields.Selection(string="Type of exam", selection=[('internal', 'Internal'),
                                                                   ('semester', 'Semester'),
                                                                   ('unit test', 'Unit test')], required=True)

    exam_class = fields.Many2one("class.college.erp", string="Class", required=True)
    exam_semester_id = fields.Many2one("semester.college.erp", string="Semester",
                                       related="exam_class.semester_for_class_id")
    exam_course = fields.Many2one("course.college.erp", string="Course",
                                  related="exam_class.course_of_class_id")
    exam_start_date = fields.Date("Start date", required=True)
    exam_end_date = fields.Date("End date", required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('completed', 'Completed')],
                             compute="stage_change", default='draft')
    exam_name = fields.Char("Exam", compute='compute_display_name')
    exam_subject_ids = fields.Many2many("syllabus.college.erp", widget="section_and_note_one2many",
                                        string="exam subject")
    count_valuation = fields.Integer(compute="count_of_exam")

    @api.depends('exam_type', 'exam_semester_id', 'exam_course')
    def compute_display_name(self):
        for record in self:
            if record.exam_type and record.exam_semester_id and record.exam_course:
                record.exam_name = str(record.exam_type) + " " + str(record.exam_semester_id.sem_name)
            elif record.exam_type and record.exam_semester_id:
                record.exam_name = str(record.exam_type) + " " + str(record.exam_semester_id.sem_name)
            else:
                record.exam_name = str(record.exam_type)

    @api.onchange('exam_type', 'exam_class')
    def _onchange_exam_subject_ids(self):
        if self.exam_type == 'semester':
            self.exam_subject_ids = self.exam_semester_id.sem_syllabus_ids

    @api.depends('exam_end_date')
    def stage_change(self):
        if self.exam_end_date < fields.Date.today():
            self.write({'state': 'completed'})
        else:
            self.write({'state': 'draft'})

    @api.depends('student_list_ids')
    def compute_corresponding_students(self):
        data = self.env['student.college.erp']
        for rec in self:
            stud_ids = data.search([('semester_id.id', '=', rec.semester_for_class_id.id),
                                    ('academic_year_id.id', '=', rec.academic_year_for_class_id.id)]).ids
            rec.student_list_ids = [(6, 0, stud_ids)]

    def smart_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Validation',
            'view_mode': 'tree',
            'res_model': 'student.college.erp',
            'domain': [('semester_id.id', '=', self.exam_semester_id.id), ('exam_flag', '=', 'True')],
            'context': {'create': False}
        }

    @api.depends('exam_class')
    def count_of_exam(self):
        for rec in self:
            rec.count_valuation = self.env['student.college.erp'].search_count([
                ('student_class_id.id', '=', rec.exam_class.id), ('exam_flag', '=', True)])

    def generate_mark_sheet(self):
        if self.exam_name:
            element = self.env['mark.sheet.college.erp'].create({
                'ms_exam_id': self.id,
                'marksheet_subject_ids': [(0, 0, {
                    'marksheet_subject_name_id': i.id, }) for i in self.exam_subject_ids]
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'mark.sheet.college.erp',
                'view_mode': 'form',
                'target': 'current',
                'res_id': element.id,
            }
