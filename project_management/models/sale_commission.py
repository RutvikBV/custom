from odoo import models, fields, api


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = 'this have all commission details'
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        store=True
    )

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    sale_order_ids = fields.One2many('sale.order', 'commission_id', string='Sale Orders' , compute='calculate_orders')
    total_order=fields.Integer()
    total_commission=fields.Integer()

    # @api.depends('user_id','start_date','end_date')
    def calculate_orders(self):
        if self.user_id:
            # print(self.user_id.name)
            list_of_order=self.env['sale.order'].search([('user_id.name','=',self.user_id.name),('date_order','>=',self.start_date),('date_order','<=',self.end_date)])
            # for item in list_of_order:
            #     print(item)
            self.total_order=len(list_of_order)
            self.total_commission=round(sum(order.commission for order in list_of_order),2)
            self.sale_order_ids=[(6, 0, list_of_order.ids)]
        else:
            self.sale_order_ids= [(5, 0, 0)]



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    percent_commission = fields.Integer(string='Percentage', default=16, readonly=True)
    commission = fields.Float(string='Commission', compute="_compute_commission")
    commission_id = fields.Many2one('sale.commission', string='Commission')


    @api.depends('amount_total')
    def _compute_commission(self):
        for rec in self:
            rec.commission = rec.amount_total * (rec.percent_commission / 100)
class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_ids = fields.One2many('sale.order', 'commission_id', string='Sale Orders',compute='calculate_orders')

    def calculate_orders(self):
        if self.name:
            print(self.name)
            list_of_order = self.env['sale.order'].search([('user_id.name', '=', self.name)])
            for item in list_of_order:
                print(item)
            self.sale_order_ids = [(6, 0, list_of_order.ids)]
        else:
            self.sale_order_ids = [(5, 0, 0)]