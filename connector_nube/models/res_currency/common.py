# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from openerp import fields, models

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class TiendaNubeResCurrency(models.Model):
    _name = 'tienda_nube.res.currency'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.currency': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='res.currency',
            string='Currency',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.res.currency',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
            readonly=True
    )


@tienda_nube
class ResCurrencyAdapter(GenericAdapter):
    _model_name = 'tienda_nube.res.currency'
    _tienda_nube_model = 'currencies'
