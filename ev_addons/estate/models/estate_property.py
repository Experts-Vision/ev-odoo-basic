from odoo import models, fields


class EstateProperty(models.Model):
    # meta fields data for the model
    _name = 'estate.property' # this is a mandatory field
    _description = 'Estate Property'

    # fields data for the model
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
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
        string='State', default='new'
    )