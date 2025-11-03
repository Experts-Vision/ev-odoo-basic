from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'


    property_ids = fields.One2many("estate.property", "salesperson_id") 

    property_count = fields.Integer(default=0, compute="_compute_property_count")


    @api.depends("property_ids")
    def _compute_property_count(self): 
        for rec in self:
            rec.property_count = len(rec.property_ids)
