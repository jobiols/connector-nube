# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from openerp import fields, models

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class TiendaNubeResCountry(models.Model):
    _name = 'tienda_nube.res.country'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.country': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='res.country',
            required=True,
            ondelete='cascade',
            string='Country',
            oldname='openerp_id',
    )


class ResCountry(models.Model):
    _inherit = 'res.country'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.res.country',
            inverse_name='odoo_id',
            readonly=True,
            string='tienda_nube Bindings',
    )


@tienda_nube
class ResCountryAdapter(GenericAdapter):
    _model_name = 'tienda_nube.res.country'
    _tienda_nube_model = 'countries'
