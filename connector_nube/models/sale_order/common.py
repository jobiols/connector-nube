# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import openerp.addons.decimal_precision as dp

from openerp import models, fields, api

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube

_logger = logging.getLogger(__name__)

try:
    from prestapyt import TiendaNubeWebServiceDict
except ImportError:
    _logger.debug('Can not `from prestapyt import TiendaNubeWebServiceDict`.')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.sale.order',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )


class TiendaNubeSaleOrder(models.Model):
    _name = 'tienda_nube.sale.order'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'sale.order': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='sale.order',
            string='Sale Order',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    tienda_nube_order_line_ids = fields.One2many(
            comodel_name='tienda_nube.sale.order.line',
            inverse_name='tienda_nube_order_id',
            string='TiendaNube Order Lines',
    )
    tienda_nube_discount_line_ids = fields.One2many(
            comodel_name='tienda_nube.sale.order.line.discount',
            inverse_name='tienda_nube_order_id',
            string='TiendaNube Discount Lines',
    )
    tienda_nube_invoice_number = fields.Char('TiendaNube Invoice Number')
    tienda_nube_delivery_number = fields.Char('TiendaNube Delivery Number')
    total_amount = fields.Float(
            string='Total amount in TiendaNube',
            digits_compute=dp.get_precision('Account'),
            readonly=True,
    )
    total_amount_tax = fields.Float(
            string='Total tax in TiendaNube',
            digits_compute=dp.get_precision('Account'),
            readonly=True,
    )
    total_shipping_tax_included = fields.Float(
            string='Total shipping in TiendaNube',
            digits_compute=dp.get_precision('Account'),
            readonly=True,
    )
    total_shipping_tax_excluded = fields.Float(
            string='Total shipping in TiendaNube',
            digits_compute=dp.get_precision('Account'),
            readonly=True,
    )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.sale.order.line',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )
    tienda_nube_discount_bind_ids = fields.One2many(
            comodel_name='tienda_nube.sale.order.line.discount',
            inverse_name='odoo_id',
            string='TiendaNube Discount Bindings',
    )


class TiendaNubeSaleOrderLine(models.Model):
    _name = 'tienda_nube.sale.order.line'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'sale.order.line': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='sale.order.line',
            string='Sale Order line',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    tienda_nube_order_id = fields.Many2one(
            comodel_name='tienda_nube.sale.order',
            string='TiendaNube Sale Order',
            required=True,
            ondelete='cascade',
            index=True,
    )

    @api.model
    def create(self, vals):
        ps_sale_order = self.env['tienda_nube.sale.order'].search([
            ('id', '=', vals['tienda_nube_order_id'])
        ], limit=1)
        vals['order_id'] = ps_sale_order.odoo_id.id
        return super(TiendaNubeSaleOrderLine, self).create(vals)


class TiendaNubeSaleOrderLineDiscount(models.Model):
    _name = 'tienda_nube.sale.order.line.discount'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'sale.order.line': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='sale.order.line',
            string='Sale Order line',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    tienda_nube_order_id = fields.Many2one(
            comodel_name='tienda_nube.sale.order',
            string='TiendaNube Sale Order',
            required=True,
            ondelete='cascade',
            index=True,
    )

    @api.model
    def create(self, vals):
        ps_sale_order = self.env['tienda_nube.sale.order'].search([
            ('id', '=', vals['tienda_nube_order_id'])
        ], limit=1)
        vals['order_id'] = ps_sale_order.odoo_id.id
        return super(TiendaNubeSaleOrderLineDiscount, self).create(vals)


@tienda_nube
class SaleOrderAdapter(GenericAdapter):
    _model_name = 'tienda_nube.sale.order'
    _tienda_nube_model = 'orders'
    _export_node_name = 'order'

    def update_sale_state(self, tienda_nube_id, datas):
        api = self.connect()
        return api.add('order_histories', datas)

    def search(self, filters=None):
        result = super(SaleOrderAdapter, self).search(filters=filters)

        shops = self.env['tienda_nube.shop'].search([
            ('backend_id', '=', self.backend_record.id)
        ])
        for shop in shops:
            if not shop.default_url:
                continue
            api = TiendaNubeWebServiceDict(
                    '%s/api' % shop.default_url, self.tienda_nube.webservice_key
            )
            result += api.search(self._tienda_nube_model, filters)
        return result


@tienda_nube
class SaleOrderLineAdapter(GenericAdapter):
    _model_name = 'tienda_nube.sale.order.line'
    _tienda_nube_model = 'order_details'


@tienda_nube
class OrderPaymentAdapter(GenericAdapter):
    _model_name = '__not_exist_tienda_nube.payment'
    _tienda_nube_model = 'order_payments'


@tienda_nube
class OrderDiscountAdapter(GenericAdapter):
    _model_name = 'tienda_nube.sale.order.line.discount'
    _tienda_nube_model = 'order_discounts'
