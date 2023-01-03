from odoo import models, fields, api


class Promotion(models.Model):
    _name = 'promotion.college.erp'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'promotion_exam'
    _sql_constraints = [
        ('promotion_exam', 'unique(promotion_exam)', 'Already promoted using this exam!')
    ]

    promotion_exam = fields.Many2one('exam.college.erp', string="Exam")
    promotion_Class = fields.Many2one('class.college.erp', related="promotion_exam.exam_class", string="Class")
    promotion_Semester = fields.Many2one('semester.college.erp', related="promotion_exam.exam_semester_id",
                                         string="Semester")
    promoted_student_ids = fields.Many2many('student.college.erp', string="Promoted students")
    promotion_state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('completed', 'Completed')],
                                       default='draft', tracking=True)

    @api.depends('stud_ids')
    def getStudentDetails(self):
        data = self.env['student.college.erp'].search([])
        print('ertyu')
        for record in data:
            promoted_students = record.search([('student_class_id.id', "=", self.promotion_Class.id),
                                               ('exam_flag', '=', True)]).ids
            self.promoted_student_ids = [(6, 0, promoted_students)]
        if self.promoted_student_ids:
            self.promotion_state = 'pending'

    def promote_students(self):
        marksheet_object = self.env['mark.sheet.college.erp']
        for stud_id in self.promoted_student_ids:
            promote_id = marksheet_object.search(
                [('ms_Student_id.id', '=', stud_id.id), ('Pass_or_Fail', '=', True)]).ids
            print(promote_id)

            if promote_id:
                if self.promotion_Class.promotion_class.id:
                    stud_id.student_class_id = self.promotion_Class.promotion_class.id
                self.promotion_state = 'completed'
