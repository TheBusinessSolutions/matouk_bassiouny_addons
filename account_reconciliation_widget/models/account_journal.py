from odoo import models


class AccountJournal(models.Model):

    _inherit = "account.journal"

    def action_open_reconcile(self):
        if self.type in ['bank', 'cash']:
            # Open reconciliation view for bank statements belonging to this journal
            bank_stmt = self.env['account.bank.statement.line'].search([('statement_id.journal_id', 'in', self.ids), ('is_reconciled', '=', False)])
            return {
                'type': 'ir.actions.client',
                'tag': 'bank_statement_reconciliation_view',
                'context': {'statement_line_ids': bank_stmt.ids, 'company_ids': self.mapped('company_id').ids},
            }
        else:
            # Open reconciliation view for customers/suppliers
            action_context = {'show_mode_selector': False, 'company_ids': self.mapped('company_id').ids}
            if self.type == 'sale':
                action_context.update({'mode': 'customers'})
            elif self.type == 'purchase':
                action_context.update({'mode': 'suppliers'})
            return {
                'type': 'ir.actions.client',
                'tag': 'manual_reconciliation_view',
                'context': action_context,
            }

    def action_open_reconcile_to_check(self):
        self.ensure_one()
        ids = self.to_check_ids().ids
        action_context = {
            "show_mode_selector": False,
            "company_ids": self.mapped("company_id").ids,
            "suspense_moves_mode": True,
            "statement_line_ids": ids,
        }
        return {
            "type": "ir.actions.client",
            "tag": "bank_statement_reconciliation_view",
            "context": action_context,
        }
