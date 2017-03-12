# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter

_logger = logging.getLogger(__name__)


class TiendaNubeDeliveryCarrier(models.Model):
    _name = 'tienda_nube.delivery.carrier'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'delivery.carrier': 'odoo_id'}
    _description = 'TiendaNube Carrier'

    odoo_id = fields.Many2one(
            comodel_name='delivery.carrier',
            string='Delivery carrier',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    id_reference = fields.Integer(
            string='Reference ID',
            help="In TiendaNube, carriers can be copied with the same 'Reference "
                 "ID' (only the last copied carrier will be synchronized with the "
                 "ERP)"
    )
    name_ext = fields.Char(
            string='Name in TiendaNube',
    )
    active_ext = fields.Boolean(
            string='Active in TiendaNube',
    )
    export_tracking = fields.Boolean(
            string='Export tracking numbers to TiendaNube',
    )


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.delivery.carrier',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )
    company_id = fields.Many2one(
            comodel_name='res.company',
            string='Company',
            index=True,
    )


@tienda_nube
class DeliveryCarrierAdapter(GenericAdapter):
    _model_name = 'tienda_nube.delivery.carrier'
    _tienda_nube_model = 'carriers'

    def search(self, filters=None):
        if filters is None:
            filters = {}
        filters['filter[deleted]'] = 0

        return super(DeliveryCarrierAdapter, self).search(filters)
