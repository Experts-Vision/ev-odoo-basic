from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateOffer(models.Model): 
    _name="estate.offer"
    _description="Estate Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("Accepted", "Accepted"),
        ("Refused", "Refused"),
    ])
    partner_id= fields.Many2one(string="Person", comodel_name="res.partner")

    # inverse Field used to create One2many relationship with the property model
    property_id = fields.Many2one(string="Property", comodel_name="estate.property")

    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.type", related="property_id.type_id")

    validity = fields.Float(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute="_compute_deadline_date",  inverse="_inverse_deadline_date")

    @api.depends("validity")
    def _compute_deadline_date(self):
        for rec in self: 
            if rec.create_date:
                # Convert datetime to date before adding days
                base_date = fields.Date.to_date(rec.create_date)
                rec.deadline = fields.Date.add(base_date, days=rec.validity)
            else:
                rec.deadline = fields.Date.add(fields.Date.today(), days=rec.validity)
    
    def _inverse_deadline_date(self): 
        for rec in self: 
            if rec.deadline: 
                # Get the base date (create_date if exists, otherwise today for new records)
                if rec.create_date: 
                    # Convert datetime to date
                    base_date = fields.Date.to_date(rec.create_date)
                else: 
                    # For new records, use today as base
                    base_date = fields.Date.today()
                
                # Calculate difference in days (deadline - base_date)
                delta = rec.deadline - base_date
                rec.validity = max(0, delta.days)  # Ensure validity is not negative
            else: 
                rec.validity = 7


    def confirm_offer(self): 
        for rec in self: 
            rec.property_id.buyer_id = rec.partner_id
            rec.property_id.selling_price = rec.price
            rec.status = "Accepted"

    
    def refuse_offer(self): 
        for rec in self: 
            rec.status = "Refused"

    @api.model
    def create(self, vals): 
        property_rec = self.env["estate.property"].browse(vals['property_id'])
        property_rec.state = "offer_received"
        lowest_price = 0
        if len(property_rec.offer_ids) > 0:
            lowest_price = min(property_rec.offer_ids.mapped("price"))
        if vals['price'] < lowest_price:
            raise UserError("The Offer Price must be higher than the lowest offer price")
        return super().create(vals)