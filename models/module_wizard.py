# simple_module/models/module_wizard.py
from odoo import api, fields, models, _

class SimpleModelListWizard(models.TransientModel):
    _name = 'simple.model.list.wizard'
    _description = 'Wizard that shows names of selected simple.model records'

    record_names = fields.Text(string="Selected Simple-Model Names", readonly=True)

class SimpleModel(models.Model):
    _inherit = 'simple.model'

    def action_show_selected_models(self):
        names = "\n".join(self.mapped("name")) or _("No records selected.")
        wiz = self.env['simple.model.list.wizard'].create({'record_names': names})
        view = self.env.ref('simple_module.view_simple_model_list_wizard_form')
        return {
            'name': _('Selected Simple-Model Names'),
            'type': 'ir.actions.act_window',
            'res_model': 'simple.model.list.wizard',
            'res_id': wiz.id,
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'target': 'new',
        }
