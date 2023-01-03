import calendar
from dateutil.relativedelta import relativedelta
from odoo import models, fields
import datetime


class ProjectSchedule(models.Model):
    _name = 'project.schedule'

    project_schedule_id = fields.Many2one('project.project')
    month = fields.Char("Month")
    year = fields.Char("Year")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")


class ProjectInherit(models.Model):
    _inherit = 'project.project'

    s_date_ids = fields.One2many('project.schedule', 'project_schedule_id', string="dates", readonly=True)
    # sale_order_ref = fields.Many2one('res.partner', "partner reference")

    def get_date(self):
        month = 1
        a = datetime.date.today()
        year = a.year
        if not self.s_date_ids:
            for i in range(1, 13):
                first_day = datetime.date(year, month, 1)
                last_day = datetime.date(year, month, 1) + relativedelta(day=31)  # End-of-month
                month += 1
                data = self.env['project.schedule'].sudo().create({
                    'month': calendar.month_name[i],
                    'year': year,
                    'start_date': first_day,
                    'end_date': last_day,
                    'project_schedule_id': self.id
                })
                self.env['project.project'].update({
                    's_date_ids': [(0, 0, data.id)]
                })
