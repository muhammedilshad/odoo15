from odoo import models, fields, api, _


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    credit_limit = fields.Boolean("Active credit limit")
    warning_amount = fields.Float("Warning amount")
    blocking_amount = fields.Float("Blocking amount")


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    due_amount = fields.Float("Amount due", readonly=True, default=False)
    hide_button = fields.Boolean(string="test", default=False)

    @api.onchange('partner_id')
    def calculate_due_amount(self):
        self.write({'due_amount': 0})
        data = self.env['account.move'].search(
            [('partner_id', "=", self.partner_id.id), ('payment_state', "=", 'not_paid')])
        amount = 0
        for rec in data:
            amount = rec.amount_total + amount
            self.due_amount = amount

    @api.onchange('partner_id')
    def warning_amount_checking(self):
        self.hide_button = False
        warng_amount = self.partner_id.warning_amount
        blocking_amt = self.partner_id.blocking_amount
        if warng_amount <= self.due_amount < blocking_amt:
            msg = {'warning': {
                'title': _('Warning'),
                'message': _('My warning message.')}}
            return msg

        elif self.due_amount:
            if self.due_amount >= blocking_amt:
                self.hide_button = True
                self.update({'partner_id': True})
                return {'warning': {
                    'title': _('Warning'),
                    'message': _('Cant continue with this customer.')}}
