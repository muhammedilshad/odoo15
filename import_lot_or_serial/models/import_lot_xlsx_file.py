from odoo import models, fields, _


class LotOrSerialImport(models.Model):
    _inherit = 'stock.production.lot'

    name = fields.Char("test")

    def import_btn(self):
        return {
            'name': _('Test Wizard'),
            'type': 'ir.actions.act_window',
            'res_model': 'lot.serial.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }
