# simple_module/models/simple_model.py
from odoo import models, fields

class SimpleModel(models.Model):
    _name = 'simple.model'
    _description = 'Simple Model'

    name = fields.Char(required=True, string='Name')
    description = fields.Text(string='Description')
