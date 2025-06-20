# -*- coding: utf-8 -*-
# simple_module/models/simple_model.py

from odoo import models, fields, api
from psycopg2 import sql


# ────────────────────────────────────────────────
#  Simple Model
# ────────────────────────────────────────────────
class SimpleModel(models.Model):
    _name = 'simple.model'
    _description = 'Simple Model'

    name        = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    # reverse side of the relation
    group_ids = fields.Many2many(
        'simple.group',
        'simple_group_model_rel',   # relation-table name (shared)
        'model_id',                 # column on this model
        'group_id',                 # column on comodel
        string='Groups',
        help='Groups that include this model',
    )

    def add_raw_record(self):
        """
        Insert one new row per record via raw SQL,
        using the current record’s name and description.
        """
        for rec in self:
            query = sql.SQL("""
                INSERT INTO {table} (name, description)
                VALUES (%s, %s)
            """).format(table=sql.Identifier(rec._table))
            rec.env.cr.execute(query, (rec.name, rec.description))
        # Odoo will commit at the end of the request
        return True

    @api.model
    def fetch_all(self):
        """
        Fetch all rows from simple_model via raw SQL.
        """
        self.env.cr.execute(f"SELECT id, name, description FROM {self._table}")
        cols = [d[0] for d in self.env.cr.description]
        return [dict(zip(cols, row)) for row in self.env.cr.fetchall()]


# ────────────────────────────────────────────────
#  Simple Group
# ────────────────────────────────────────────────
class SimpleGroup(models.Model):
    _name = 'simple.group'
    _description = 'Simple Group'

    name = fields.Char(string='Group Name', required=True)

    # forward side of the relation
    model_ids = fields.Many2many(
        'simple.model',
        'simple_group_model_rel',   # same relation-table
        'group_id',                 # column on this model
        'model_id',                 # column on comodel
        string='Models',
        help='Simple models that belong to this group',
    )

    def action_show_models(self):
        """Return a window-action listing every simple.model linked to *any*
        of the groups in `self`."""
        return {
            "type": "ir.actions.act_window",
            "name": "Models in Selected Group",
            "res_model": "simple.model",
            "view_mode": "list,form",
            "domain": [("group_ids", "in", self.ids)],
        }
