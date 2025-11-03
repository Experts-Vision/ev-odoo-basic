from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo.tools import float_utils 

class EstateProperty(models.Model):
    # meta fields data for the model
    _name = 'estate.property' # this is a mandatory field
    _description = 'Estate Property'

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Property expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Property selling price must be positive.'),
    ]

    # fields data for the model
    name = fields.Char(string='Name', related='type_id.name')
    type_id = fields.Many2one(string='Type', comodel_name='estate.type')
    # description = fields.Text(string='Description', required=True)
    tags_ids = fields.Many2many(string="Tags", comodel_name="estate.tags")
    offer_ids = fields.One2many("estate.offer", "property_id", string="Offers") 
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=(fields.Date.add(fields.Date.today(), days=30)))
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        string='Garden Orientation'
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        string='State', default='new', copy=False
    )
    salesperson_id = fields.Many2one(string='Salesperson', comodel_name='res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one(string='Buyer', comodel_name='res.partner')



    # total area
    total_area = fields.Float(string='Total Area', compute='_compute_total_area')


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self: 
            rec.total_area = rec.living_area + rec.garden_area

    # best offer 
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')

    
    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for rec in self: 
            price_list = rec.offer_ids.mapped("price")
            if not len(price_list):
                rec.best_offer = 0
            else:
                rec.best_offer = max(rec.offer_ids.mapped("price"))
            
    

    @api.onchange("garden")
    def _onchage_garden(self): 
        for rec in  self:
            if rec.garden: 
                rec.garden_area = 10
                rec.garden_orientation = "North"
                return {'warning': {
                        'title': _("Warning"),
                        'message': ('This option is not supported for Authorize.net')}}
            else: 
                rec.garden_area = 0
                rec.garden_orientation = None

    
            
            
    def sell_property(self):
        for rec in self: 
            if rec.state != 'canceled': 
                rec.state = "sold" 
            else: 
                raise UserError("The Canceled Property can't be sold")

    def cancel_property(self):
        for rec in self: 
            if rec.state != 'sold': 
                rec.state = "canceled" 
            else: 
                raise UserError("The Sold Property can't be Canceled")
            

    @api.constrains("selling_price")
    def _check_selling_price(self): 
        for rec in self: 
            accepted_line = rec.expected_price * .9 # 90% from the expected price
            if rec.selling_price < accepted_line:
                raise UserError("The Selling Price must be at least 90% of the Expected Price")


    # def unlink(self): # this overide could cause some issue while uninstalling the module
    #     print(self)
    #     for rec in self: 
    #         if rec.state != 'new' and rec.state != 'canceled':
    #             raise UserError(f"Can't delete {rec.state} record !") 
    #     return super().unlink()

    @api.ondelete(at_uninstall=False)
    def _prevent_delete_active_property(self):
        for rec in self: 
            if rec.state != 'new' and rec.state != 'canceled':
                raise UserError(f"Can't delete {rec.state} record !") 
            