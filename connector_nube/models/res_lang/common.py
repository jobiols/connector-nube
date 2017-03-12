# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from openerp import models, fields

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class TiendaNubeResLang(models.Model):
    _name = 'tienda_nube.res.lang'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.lang': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='res.lang',
            required=True,
            ondelete='cascade',
            string='Language',
            oldname='openerp_id',
    )
    active = fields.Boolean(
            string='Active in TiendaNube',
            default=False,
    )


class ResLang(models.Model):
    _inherit = 'res.lang'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.res.lang',
            inverse_name='odoo_id',
            readonly=True,
            string='TiendaNube Bindings',
    )


@tienda_nube
class ResLangAdapter(GenericAdapter):
    _model_name = 'tienda_nube.res.lang'
    _tienda_nube_model = 'languages'
