# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, fields, models

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class StockLocation(models.Model):
    _inherit = 'stock.warehouse'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.shop',
            inverse_name='odoo_id',
            readonly=True,
            string='TiendaNube Bindings',
    )


class TiendaNubeShop(models.Model):
    _name = 'tienda_nube.shop'
    _inherit = 'tienda_nube.binding'
    _description = 'TiendaNube Shop'

    @api.multi
    @api.depends('shop_group_id', 'shop_group_id.backend_id')
    def _compute_backend_id(self):
        self.backend_id = self.shop_group_id.backend_id.id

    name = fields.Char(
            string='Name',
            help="The name of the method on the backend",
            required=True
    )
    shop_group_id = fields.Many2one(
            comodel_name='tienda_nube.shop.group',
            string='TiendaNube Shop Group',
            required=True,
            ondelete='cascade',
    )
    odoo_id = fields.Many2one(
            comodel_name='stock.warehouse',
            string='WareHouse',
            required=True,
            readonly=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    backend_id = fields.Many2one(
            compute='_compute_backend_id',
            comodel_name='tienda_nube.backend',
            string='TiendaNube Backend',
            store=True,
    )
    default_url = fields.Char('Default url')


@tienda_nube
class ShopAdapter(GenericAdapter):
    _model_name = 'tienda_nube.shop'
    _tienda_nube_model = 'shops'
