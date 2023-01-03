from odoo import models, fields, api, exceptions, _


class Student(models.Model):
    _name = "student.college.erp"
    _rec_name = "admission_no"

    admission_no = fields.Char("Admission no")
    admission_date = fields.Date("Admission date")
    first_name = fields.Char("First name", required=True)
    last_name = fields.Char("Last name")
    father = fields.Char("Father's name")
    mother = fields.Char("Mother's name")
    communication_address = fields.Char("Communication address", required=True)
    permanent_address = fields.Char("Permanent address")
    same_as_communication_address = fields.Boolean('Same as communication address')
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    student_course_id = fields.Many2one("course.college.erp", string="Course", related='semester_id.sem_course_id')
    academic_year_id = fields.Many2one("admission.college.erp", string="Academic year",
                                       related='student_class_id.academic_year_for_class_id')
    semester_id = fields.Many2one("semester.college.erp", string="Semester",
                                  related='student_class_id.semester_for_class_id')
    student_class_id = fields.Many2one("class.college.erp", string="Class of student", required=True)
    exam_flag = fields.Boolean("Exam attended", default=False)

    @api.depends('semester_for_class_id', 'academic_year_id')
    def compute_class_name(self):
        for record in self:
            if record.semester_for_class_id and record.academic_year_for_class_id:
                record.name_of_class = str(record.academic_year_for_class_id.academic_year) + "  " + str(
                    record.semester_for_class_id.sem_name)
            else:
                record.name_of_class = str(record.semester_for_class_id)

    @api.model
    def create(self, vals):
        if vals.get('admission_no', 'New') == 'New':
            vals['admission_no'] = self.env['ir.sequence'].next_by_code(
                'student_college_erp') or 'New'
        result = super(Student, self).create(vals)
        return result


class Admission(models.Model):
    _name = 'admission.college.erp'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'academic_year'

    admission_no = fields.Char(string="admission no", default="New")
    first_name = fields.Char("First name")
    last_name = fields.Char("Last name")
    father = fields.Char("Father's name")
    mother = fields.Char("Mother's name")
    communication_address = fields.Char("Communication address")
    permanent_address = fields.Char("Permanent address")
    same_as_communication_address = fields.Boolean('Same as communication address')
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    course_id = fields.Many2one("course.college.erp", string="Course")
    date_of_application = fields.Date("Date Of Application", default=fields.Datetime.today())
    academic_year = fields.Char(string="Academic Year")
    previous_educational_qualification = fields.Selection(
        string='Previous educational qualification',
        selection=[('higher secondary', 'HIGHER SECONDARY'),
                   ('ug', 'UG'), ('pg', 'PG')])
    educational_institute = fields.Char("Educational Institute")
    transfer_certificate = fields.Binary("Transfer Certificate")
    state = fields.Selection([('draft', 'Draft'), ('application', 'Application'), ('approved', 'Approved'),
                              ('done', 'Done'), ('rejected', 'Rejected')], default='draft')

    def confirm_button(self):
        if self.state == 'draft':
            self.write({'state': 'application'})
        elif self.state == 'application':
            self.write({'state': 'done'})
            mail_template = self.env.ref('college_erp.email_template_got_admission')
            mail_template.send_mail(self.id, force_send=True)
        return True

    def reject_button(self):
        self.write({'state': 'rejected'})
        mail_template = self.env.ref('college_erp.email_template_got_rejected')
        mail_template.send_mail(self.id, force_send=True)
        return True

    @api.constrains('transfer_certificate')
    def attach_or_not(self):
        if not self.transfer_certificate:
            raise exceptions.MissingError('Select transfer Certificate')

    @api.model
    def create(self, vals):
        if vals.get('admission_no', 'New') == 'New':
            vals['admission_no'] = self.env['ir.sequence'].next_by_code(
                'admission.college.erp') or 'New'
        result = super(Admission, self).create(vals)
        return result


class Course(models.Model):
    _name = 'course.college.erp'

    name = fields.Char("Course Name")
    category = fields.Selection(string='Category',
                                selection=[('under graduation', 'UNDER GRADUATION'),
                                           ('Post Graduation', 'POST GRADUATION'), ('diploma', 'DIPLOMA')])
    number_of_semester = fields.Char("number of semester")
    duration = fields.Char("Duration in years")
    course_sem_ids = fields.Many2many("semester.college.erp", string="Corresponding semester",
                                      compute="corresponding_sem")
    course_ids = fields.One2many('admission.college.erp', 'course_id')

    @api.depends('course_sem_ids')
    def corresponding_sem(self):
        sem = self.env['semester.college.erp']
        for record in self:
            course_sem_ids = sem.search([('sem_course_id', "=", record.name)]).ids
            record.course_sem_ids = [(6, 0, course_sem_ids)]


class Syllabus(models.Model):
    _name = 'syllabus.college.erp'
    _rec_name = "syllabus_subject"

    syllabus_subject = fields.Char("Subject")
    syllabus_maximum_mark = fields.Integer("Maximum mark")
    syllabus_pass_mark = fields.Integer("Pass mark")
    # semester_id = fields.Many2one('semester.college.erp')


class Semester(models.Model):
    _name = 'semester.college.erp'
    _rec_name = "sem_name"

    number_of_semester = fields.Char("Number of semester", default='0')
    sem_course_id = fields.Many2one('course.college.erp', string="Course")
    sem_name = fields.Char(string="Name", readonly=True, compute="joined_name")
    sem_syllabus_ids = fields.Many2many('syllabus.college.erp')

    # sem_syllabus_ids = fields.One2many('syllabus.college.erp', 'semester_id')

    @api.depends('number_of_semester', 'sem_course_id')
    def joined_name(self):
        for record in self:
            if record.sem_course_id:
                record.sem_name = str(record.number_of_semester) + " SEM " + str(record.sem_course_id.name)
            else:
                record.sem_name = str(record.number_of_semester) + " SEM"


class Class(models.Model):
    _name = 'class.college.erp'
    _rec_name = "name_of_class"

    semester_for_class_id = fields.Many2one("semester.college.erp", string="Semester")
    course_of_class_id = fields.Many2one("course.college.erp", string="Course",
                                         related="semester_for_class_id.sem_course_id")
    academic_year_for_class_id = fields.Many2one("admission.college.erp", string="Academic year")
    name_of_class = fields.Char("Name", readonly=True, compute="compute_class_name", store=True, default="/")
    student_list_ids = fields.Many2many("student.college.erp", string="Students matching",
                                        compute="compute_corresponding_students")
    promotion_class = fields.Many2one('class.college.erp', string="Promotion class")

    @api.depends('semester_for_class_id', 'academic_year_for_class_id')
    def compute_class_name(self):
        for record in self:
            if record.semester_for_class_id and record.academic_year_for_class_id:
                record.name_of_class = str(record.academic_year_for_class_id.academic_year) + "  " + str(
                    record.semester_for_class_id.sem_name)
            else:
                record.name_of_class = str(record.semester_for_class_id)

    @api.depends('student_list_ids')
    def compute_corresponding_students(self):
        data = self.env['student.college.erp']
        for rec in self:
            stud_ids = data.search([('semester_id.id', '=', rec.semester_for_class_id.id),
                                    ('academic_year_id.id', '=', rec.academic_year_for_class_id.id)]).id
            rec.student_list_ids = [(6, 0, stud_ids)]
