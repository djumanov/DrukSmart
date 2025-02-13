from odoo import models, fields, api
from odoo.exceptions import UserError


class CustomDashboard(models.Model):
    _name = 'custom.dashboard'
    _description = 'Custom Dashboard'

    sales_order_count = fields.Integer("Sales Order", compute="_compute_dashboard_data")
    sales = fields.Float("Sales", compute="_compute_dashboard_data")
    sales_target = fields.Float("Sales Target", compute="_compute_sales_target")
    target_achievement = fields.Float("Target Achievement (%)", compute="_compute_dashboard_data")
    revenue_income = fields.Float("Revenue Income", compute="_compute_dashboard_data")
    cost_of_revenue = fields.Float("Cost of Revenue", compute="_compute_dashboard_data")
    gross_profit = fields.Float("Gross Profit", compute="_compute_dashboard_data")
    gross_profit_margin = fields.Float("Gross Profit Margin (%)", compute="_compute_dashboard_data")
    expenses = fields.Float("Expenses", compute="_compute_dashboard_data")
    net_profit = fields.Float("Net Profit", compute="_compute_dashboard_data")
    net_profit_margin = fields.Float("Net Profit Margin (%)", compute="_compute_dashboard_data")
    account_receivable = fields.Float("Account Receivable", compute="_compute_dashboard_data")
    account_payable = fields.Float("Account Payable", compute="_compute_dashboard_data")
    total_employee = fields.Integer("Total Employee", compute="_compute_dashboard_data")

    @api.depends('sales_target')
    def _compute_sales_target(self):
        """Compute the sales target from the configuration settings."""
        config = self.env['res.config.settings'].sudo().get_values()
        for record in self:
            record.sales_target = config.get('sales_target', 250000000)

    @api.depends('sales_order_count', 'sales', 'sales_target')
    def _compute_dashboard_data(self):
        """Compute all the dashboard metrics."""
        for record in self:
            try:
                # Sales Order Count
                record.sales_order_count = self._compute_sales_order_count()

                # Total Sales
                record.sales = self._compute_total_sales()

                # Target Achievement
                record.target_achievement = self._compute_target_achievement(record.sales, record.sales_target)

                # Revenue Income
                record.revenue_income = record.sales

                # Cost of Revenue
                record.cost_of_revenue = self._compute_cost_of_revenue(record.revenue_income)

                # Gross Profit
                record.gross_profit = self._compute_gross_profit(record.revenue_income, record.cost_of_revenue)

                # Gross Profit Margin
                record.gross_profit_margin = self._compute_gross_profit_margin(record.gross_profit, record.revenue_income)

                # Expenses
                record.expenses = self._compute_expenses()

                # Net Profit
                record.net_profit = self._compute_net_profit(record.gross_profit, record.expenses)

                # Net Profit Margin
                record.net_profit_margin = self._compute_net_profit_margin(record.net_profit, record.revenue_income)

                # Account Receivable
                record.account_receivable = self._compute_account_receivable()

                # Account Payable
                record.account_payable = self._compute_account_payable()

                # Total Employee
                record.total_employee = self._compute_total_employee()

            except Exception as e:
                raise UserError(f"Error computing dashboard data: {e}")

    def _compute_sales_order_count(self):
        """Compute the total number of sales orders."""
        return self.env['sale.order'].sudo().search_count([])

    def _compute_total_sales(self):
        """Compute the total sales amount."""
        sale_orders = self.env['sale.order'].sudo().search([])
        return sum(order.amount_total for order in sale_orders)

    def _compute_target_achievement(self, sales, sales_target):
        """Compute the target achievement percentage."""
        return (sales / sales_target) * 100 if sales_target else 0

    def _compute_cost_of_revenue(self, revenue_income):
        """Compute the cost of revenue."""
        return revenue_income * 0.6

    def _compute_gross_profit(self, revenue_income, cost_of_revenue):
        """Compute the gross profit."""
        return revenue_income - cost_of_revenue

    def _compute_gross_profit_margin(self, gross_profit, revenue_income):
        """Compute the gross profit margin percentage."""
        return (gross_profit / revenue_income) * 100 if revenue_income else 0

    def _compute_expenses(self):
        """Compute the total expenses."""
        expense_accounts = self.env['account.move.line'].sudo().search([('account_id.user_type_id.type', '=', 'expense')])
        return sum(expense_accounts.mapped('balance'))

    def _compute_net_profit(self, gross_profit, expenses):
        """Compute the net profit."""
        return gross_profit - expenses

    def _compute_net_profit_margin(self, net_profit, revenue_income):
        """Compute the net profit margin percentage."""
        return (net_profit / revenue_income) * 100 if revenue_income else 0

    def _compute_account_receivable(self):
        """Compute the total account receivable."""
        receivable_accounts = self.env['account.move.line'].sudo().search([('account_id.user_type_id.type', '=', 'receivable')])
        return sum(receivable_accounts.mapped('balance'))

    def _compute_account_payable(self):
        """Compute the total account payable."""
        payable_accounts = self.env['account.move.line'].sudo().search([('account_id.user_type_id.type', '=', 'payable')])
        return sum(payable_accounts.mapped('balance'))

    def _compute_total_employee(self):
        """Compute the total number of employees."""
        return self.env['hr.employee'].sudo().search_count([])

