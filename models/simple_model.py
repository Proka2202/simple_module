# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from psycopg2 import sql


# ────────────────────────────────────────────────
#  Simple Model
# ────────────────────────────────────────────────
class SimpleModel(models.Model):
    _name = 'simple.model'
    _description = 'Simple Model'

    # Basic fields
    name        = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    # Numeric field for pivot analysis
    value = fields.Float(string="Value", digits="Product Price", default=0.0)

    # State workflow
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('archived', 'Archived'),
        ],
        string="Status",
        default='draft',
        tracking=True,
    )

    # Reverse side of the many2many relation with SimpleGroup
    group_ids = fields.Many2many(
        'simple.group',
        'simple_group_model_rel',
        'model_id',
        'group_id',
        string='Groups',
        help='Groups that include this model',
    )

    # ──────────────────────────────────────────
    #  Workflow button actions
    # ──────────────────────────────────────────
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'
        return True

    def action_archive(self):
        for rec in self:
            rec.state = 'archived'
        return True

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'
        return True

    # ──────────────────────────────────────────
    #  Raw-SQL helpers (educational)
    # ──────────────────────────────────────────
    def add_raw_record(self):
        """
        Insert one new row per record via raw SQL,
        using the record’s current values.
        """
        for rec in self:
            query = sql.SQL("""
                INSERT INTO {table} (name, description, value, state)
                VALUES (%s, %s, %s, %s)
            """).format(table=sql.Identifier(rec._table))
            rec.env.cr.execute(query, (rec.name, rec.description, rec.value, rec.state))
        return True

    @api.model
    def fetch_all(self):
        """
        Fetch all rows from simple_model via raw SQL.
        """
        self.env.cr.execute(f"""
            SELECT id, name, description, value, state
            FROM {self._table}
        """)
        cols = [d[0] for d in self.env.cr.description]
        return [dict(zip(cols, row)) for row in self.env.cr.fetchall()]

    # ──────────────────────────────────────────
    #  Deletion rule: block if archived
    # ──────────────────────────────────────────
    def unlink(self):
        for rec in self:
            if rec.state == 'archived':
                raise UserError("You cannot delete an archived record.")
        return super().unlink()


# ────────────────────────────────────────────────
#  Simple Group
# ────────────────────────────────────────────────
class SimpleGroup(models.Model):
    _name = 'simple.group'
    _description = 'Simple Group'

    name = fields.Char(string='Group Name', required=True)

    # Forward side of the many2many relation
    model_ids = fields.Many2many(
        'simple.model',
        'simple_group_model_rel',
        'group_id',
        'model_id',
        string='Models',
        help='Simple models that belong to this group',
    )

    def action_show_models(self):
        """
        Return a window action listing every simple.model
        linked to any of the selected groups.
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Models in Selected Group",
            "res_model": "simple.model",
            "view_mode": "list,form,pivot",
            "domain": [("group_ids", "in", self.ids)],
        }
