# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SQLQueryWizard(models.TransientModel):
    _name = 'simple.sql.query.wizard'
    _description = 'Execute Arbitrary SQL'

    query = fields.Text(
        string="SQL Query",
        required=True,
        help="Write any SELECT, UPDATE, INSERT, DELETE, etc."
    )
    results = fields.Text(
        string="Results",
        readonly=True,
        help="Output of your query (first 1000 chars)"
    )

    def action_execute(self):
        """
        Run the SQL in `query`.  If it’s a SELECT, show first 10 rows.
        Keep the wizard open by returning an act_window that re-opens itself.
        """
        self.ensure_one()
        cr = self.env.cr

        try:
            cr.execute(self.query)
        except Exception as e:
            cr.rollback()  # reset aborted transaction
            self.results = f"Error:\n{e}"
        else:
            # show result set or a success message
            if cr.description:  # it was a SELECT
                cols = [d[0] for d in cr.description]
                rows = cr.fetchmany(10)
                lines = ["\t".join(cols)] + [
                    "\t".join(str(c) for c in row) for row in rows
                ]
                self.results = "\n".join(lines)
            else:
                self.results = "Query executed successfully."

        # Re-open this same wizard record so the user sees `results`
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'simple.sql.query.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',  # keep it as a modal
        }
