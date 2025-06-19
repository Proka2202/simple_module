from odoo import models, fields

class SimpleModel(models.Model):
    _name = 'simple.model'
    _description = 'Simple Model'

    name        = fields.Char(required=True, string='Name')
    description = fields.Text(string='Description')

    group_ids = fields.Many2many(
        'simple.group',
        'simple_group_model_rel',  # relation table
        'model_id',                # column on this model
        'group_id',                # column on comodel
        string='Groups',
    )


class SimpleGroup(models.Model):
    _name = 'simple.group'
    _description = 'Simple Group'

    name = fields.Char(string="Group Name", required=True)

    model_ids = fields.Many2many(
        'simple.model',
        'simple_group_model_rel',  # same relation table
        'group_id',                # column on this model
        'model_id',                # column on comodel
        string="Models",
    )
