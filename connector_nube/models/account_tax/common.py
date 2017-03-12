# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter


class TiendaNubeAccountTax(models.Model):
    _name = 'tienda_nube.account.tax'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'account.tax': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='account.tax',
            string='Tax',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )


class AccountTax(models.Model):
    _inherit = 'account.tax'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.account.tax',
            inverse_name='odoo_id',
            string='tienda_nube Bindings',
            readonly=True,
    )


@tienda_nube
class AccountTaxAdapter(GenericAdapter):
    _model_name = 'tienda_nube.account.tax'
    _tienda_nube_model = 'taxes'
