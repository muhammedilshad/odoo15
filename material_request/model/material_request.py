from odoo import models, fields, api, _


class MaterialRequest(models.Model):
    _name = 'material.request'
    _inherit = 'mail.thread'
    _rec_name = 'sequence_no'

    sequence_no = fields.Char(default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('approval', 'Approval'), ('approved', 'Approved'),
                              ('submitted', 'Submitted'), ('rejected', 'Rejected')], default='draft')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    order_line_ids = fields.One2many('material.order.line', 'order_line_id', string="order_line", required=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code(
                'material.request') or _('New')
        result = super(MaterialRequest, self).create(vals)
        return result

    def confirm_btn(self):
        self.write({'state': 'approval'})
        # order_ids = self.env['sale.order'].search([])
        # order_names = order_ids.order_line.mapped('product_id')
        # print("order names", order_names)

    def approve_btn(self):
        self.write({'state': 'approved'})

    def reject_by_head(self):
        self.write({'state': 'rejected'})

    def approve_by_head(self):
        self.write({'state': 'submitted'})

        # a = self.env['sale.oder'].browse('partner_id')
        # print(a)
        for record in self.order_line_ids:
            if record.type == 'purchase order':
                # partner_id = self.mapped('partner_id')
                # print(partner_id)
                for i in record.product_id.seller_ids:
                    # vendors = self.env['']
                    self.env['purchase.order'].create([{
                        'partner_id': i.name.id,
                        'order_line': [
                            (0, 0, {
                                'name': record.product_id.name,
                                'product_id': record.product_id.id,
                                'product_qty': record.qty,
                            })]
                    }])
            if record.type == 'internal transfer':
                rec = self.env['stock.picking.type'].search([
                    ('code', '=', 'internal')

                ])
                # print(rec.id)
                self.env['stock.picking'].create({
                    'picking_type_id': record.id,
                    'location_id': record.source_location_id.id,
                    'location_dest_id': record.destination_location_id.id,
                    'move_lines': [(0, 0, {
                        'name': 'operation type',
                        'product_id': record.product_id.id,
                        'location_id': record.source_location_id.id,
                        'location_dest_id': record.destination_location_id.id,
                        'product_uom_qty': record.qty,
                        'product_uom': record.product_id.uom_id.id
                    })]

                })

    def smart_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfer',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('picking_type_id.id', '=', self.id)],
            'context': {'create': False}
        }


class MaterialOrderLine(models.Model):
    _name = 'material.order.line'

    order_line_id = fields.Many2one('material.request')
    product_id = fields.Many2one('product.product', string="Product")
    type = fields.Selection(string="type", selection=[('purchase order', 'Purchase order'),
                                                      ('internal transfer', 'Internal transfer')])
    qty = fields.Integer("Quantity")
    source_location_id = fields.Many2one("stock.location", domain="[('usage', '=', 'internal')]")
    destination_location_id = fields.Many2one("stock.location", domain="[('usage', '=', 'internal')]")
