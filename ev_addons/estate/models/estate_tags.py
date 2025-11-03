from  odoo import models, fields


class EstateTags(models.Model):
    _name = "estate.tags"
    _description = "Estate Tags"

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.'),
    ]

    name = fields.Char(string="Tag Name")
    color = fields.Integer(string="Color")