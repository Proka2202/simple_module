# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SimpleModelListWizard(models.TransientModel):
    _name = 'simple.model.list.wizard'
    _description = 'Selected simple.model names'

    record_names = fields.Text(readonly=True)

    simple_models = fields.Many2many('simple.model')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ids = self.env.context.get('active_ids', [])
        names = self.env['simple.model'].browse(ids).mapped('name')
        res['record_names'] = '\n'.join(names) if names else _('No records selected.')
        return res


class SimpleModel(models.Model):
    _inherit = 'simple.model'

    def action_show_selected_models(self):
        view = self.env.ref('simple_module.view_simple_model_list_wizard_form')
        return {
            'name': _('Selected Simple-Model Names'),
            'type': 'ir.actions.act_window',
            'res_model': 'simple.model.list.wizard',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'target': 'new',
            'context': {'active_ids': self.ids},
        }
