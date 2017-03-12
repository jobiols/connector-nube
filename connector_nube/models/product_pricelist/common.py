# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    tienda_nube_groups_bind_ids = fields.One2many(
            comodel_name='tienda_nube.groups.pricelist',
            inverse_name='odoo_id',
            string='TiendaNube user groups',
    )


class TiendaNubeGroupsPricelist(models.Model):
    _name = 'tienda_nube.groups.pricelist'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'product.pricelist': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.pricelist',
            required=True,
            ondelete='cascade',
            string='Odoo Pricelist',
            oldname='openerp_id',
    )


@tienda_nube
class PricelistAdapter(GenericAdapter):
    _model_name = 'tienda_nube.groups.pricelist'
    _tienda_nube_model = 'groups'
