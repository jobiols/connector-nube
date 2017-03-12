# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.category',
            inverse_name='odoo_id',
            string="TiendaNube Bindings",
    )


class TiendaNubeProductCategory(models.Model):
    _name = 'tienda_nube.product.category'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'product.category': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.category',
            required=True,
            ondelete='cascade',
            string='Product Category',
            oldname='openerp_id',
    )
    default_shop_id = fields.Many2one(comodel_name='tienda_nube.shop')
    date_add = fields.Datetime(
            string='Created At (on TiendaNube)',
            readonly=True
    )
    date_upd = fields.Datetime(
            string='Updated At (on TiendaNube)',
            readonly=True
    )
    description = fields.Html(
            string='Description', translate=True,
            help='HTML description from TiendaNube')
    link_rewrite = fields.Char(string='Friendly URL', translate=True)
    meta_description = fields.Char('Meta description', translate=True)
    meta_keywords = fields.Char(string='Meta keywords', translate=True)
    meta_title = fields.Char(string='Meta title', translate=True)
    active = fields.Boolean(string='Active', default=True)
    position = fields.Integer(string='Position')


@tienda_nube
class ProductCategoryAdapter2(GenericAdapter):
    _model_name = 'tienda_nube.product.category'
    _tienda_nube_model = 'categories'
    _export_node_name = 'category'
