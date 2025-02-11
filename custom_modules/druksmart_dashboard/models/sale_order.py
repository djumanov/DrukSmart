from odoo import models, fields, api

class DruksmartDashboard(models.Model):
    _name = 'druksmart.dashboard'
    _description = 'DrukSmart Dashboard'

    total_sales = fields.Float(string="Total Sales", compute="_compute_total_sales")
    total_revenue = fields.Float(string="Total Revenue", compute="_compute_total_revenue")
    total_expenses = fields.Float(string="Total Expenses", compute="_compute_total_expenses")
    total_employees = fields.Integer(string="Total Employees", compute="_compute_total_employees")

    @api.depends()
    def _compute_total_sales(self):
        for record in self:
            total_sales = self.env['sale.order'].search([('state', '=', 'sale')]).mapped('amount_total')
            record.total_sales = sum(total_sales)

    @api.depends()
    def _compute_total_revenue(self):
        for record in self:
            revenue = self.env['account.move.line'].search([
                ('account_id.user_type_id.type', '=', 'income')
            ]).mapped('balance')
            record.total_revenue = sum(revenue)

    @api.depends()
    def _compute_total_expenses(self):
        for record in self:
            expenses = self.env['account.move.line'].search([
                ('account_id.user_type_id.type', '=', 'expense')
            ]).mapped('balance')
            record.total_expenses = sum(expenses)

    @api.depends()
    def _compute_total_employees(self):
        for record in self:
            total_employees = self.env['hr.employee'].search_count([])
            record.total_employees = total_employees
