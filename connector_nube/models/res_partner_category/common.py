# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.res.partner.category',
        inverse_name='odoo_id',
            string='TiendaNube Bindings',
        readonly=True,
    )


class TiendaNubeResPartnerCategory(models.Model):
    _name = 'tienda_nube.res.partner.category'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.partner.category': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Partner Category',
        required=True,
        ondelete='cascade',
        oldname='openerp_id',
    )
    date_add = fields.Datetime(
            string='Created At (on TiendaNube)',
        readonly=True,
    )
    date_upd = fields.Datetime(
            string='Updated At (on TiendaNube)',
        readonly=True,
    )

    # TODO add tienda_nube shop when the field will be available in the api.
    # we have reported the bug for it
    # see http://forge.tienda_nube.com/browse/PSCFV-8284


@tienda_nube
class PartnerCategoryAdapter(GenericAdapter):
    _model_name = 'tienda_nube.res.partner.category'
    _tienda_nube_model = 'groups'
