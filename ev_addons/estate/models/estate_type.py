from odoo import models, fields, api

class EstateType(models.Model):
    _name = 'estate.type'
    _description = 'Estate Type'

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    property_ids = fields.One2many("estate.property", 'type_id')

    offer_ids = fields.One2many("estate.offer", "property_type_id")

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids) if rec.offer_ids else 0