from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    serial_number = fields.Many2one('stock.lot', string='Product Serial Number')
    serial_number_domain = fields.Char(compute='_compute_serial_number_domain', store=False)
    
    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     """Auto-select first serial number when product_id changes"""
    #     if self.product_id:
    #         # Find the first available serial number for this product
    #         first_serial = self.env['stock.lot'].search([
    #             ('product_id', '=', self.product_id.id)
    #         ], limit=1)
    #         if first_serial:
    #             self.serial_number = first_serial
    #         else:
    #             self.serial_number = False
    
    # @api.onchange('product_template_id')
    # def _onchange_product_template_id(self):
    #     """Auto-select first serial number when product_template_id changes"""
    #     if self.product_template_id:
    #         # Find the first available serial number for any variant of this template
    #         first_serial = self.env['stock.lot'].search([
    #             ('product_id.product_tmpl_id', '=', self.product_template_id.id)
    #         ], limit=1)
    #         if first_serial:
    #             self.serial_number = first_serial
    #             # Also set the product_id to match the serial number's product
    #             self.product_id = first_serial.product_id
    #         else:
    #             self.serial_number = False
    
    @api.depends('product_id')
    def _compute_serial_number_domain(self):
        """Compute domain for serial_number field"""
        for record in self:
            if record.product_id:
                record.serial_number_domain = [('product_id', '=', record.product_id.id)]
            else:
                record.serial_number_domain = [('product_id', '!=', False)]
    
    
    @api.onchange('serial_number')
    def _onchange_serial_number(self):
        """Set product fields when serial_number changes"""
        if self.serial_number:
            # Get the product template from the serial number's product
            if self.serial_number.product_id:
                self.product_template_id = self.serial_number.product_id.product_tmpl_id
                # Also set the product_id for consistency
                self.product_id = self.serial_number.product_id
                # Set UOM from the product
                self.product_uom = self.serial_number.product_id.uom_id
            else:
                # Clear fields if no product is associated with the serial number
                self.product_template_id = False
                self.product_id = False
                self.product_uom = False
        else:
            # Only clear product fields if user explicitly cleared serial number
            # (not when auto-selected by product change)
            if not self.product_id and not self.product_template_id:
                self.product_template_id = False
                self.product_id = False
                self.product_uom = False
    