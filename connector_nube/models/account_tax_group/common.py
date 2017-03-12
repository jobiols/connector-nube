# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter


class TiendaNubeAccountTaxGroup(models.Model):
    _name = 'tienda_nube.account.tax.group'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'account.tax.group': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='account.tax.group',
            string='Tax Group',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.account.tax.group',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
            readonly=True
    )
    company_id = fields.Many2one(
            comodel_name='res.company',
            index=True,
            required=True,
            string='Company',
    )


@tienda_nube
class TaxGroupAdapter(GenericAdapter):
    _model_name = 'tienda_nube.account.tax.group'
    _tienda_nube_model = 'tax_rule_groups'
