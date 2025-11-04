from odoo import fields, models, Command

class EstateProperty(models.Model): 
    _inherit = "estate.property"


    def sell_property(self):
        super().sell_property()
        # Create an empty invoice for each property
        for rec in self:
            if rec.buyer_id:
                # Get the default sales journal
                journal = self.env['account.journal'].search(
                    [('type',    '=', 'sale')], limit=1
                )
                # Calculate 6% of selling price
                commission_amount = rec.selling_price * 0.06
                
                # Create the invoice with two invoice lines
                self.env['account.move'].create({
                    'partner_id': rec.buyer_id.id,
                    'move_type': 'out_invoice',
                    'journal_id': journal.id if journal else False,
                    'invoice_line_ids': [
                        Command.create({
                            'name': f'6% of selling price for {rec.name}',
                            'quantity': 1,
                            'price_unit': commission_amount,
                        }),
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        })
                    ]
                })
        
        return True