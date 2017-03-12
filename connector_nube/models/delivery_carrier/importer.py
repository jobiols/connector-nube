# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openerp.addons.connector.queue.job import job

from ...backend import tienda_nube
from ...unit.importer import (
    TiendaNubeImporter,
    DelayedBatchImporter,
    import_batch,
)
from openerp.addons.connector.unit.mapper import ImportMapper, mapping

_logger = logging.getLogger(__name__)


@tienda_nube
class DeliveryCarrierImport(TiendaNubeImporter):
    _model_name = ['tienda_nube.delivery.carrier']


@tienda_nube
class CarrierImportMapper(ImportMapper):
    _model_name = 'tienda_nube.delivery.carrier'
    direct = [
        ('name', 'name_ext'),
        ('name', 'name'),
        ('id_reference', 'id_reference'),
    ]

    @mapping
    def active(self, record):
        return {'active_ext': record['active'] == '1'}

    @mapping
    def product_id(self, record):
        if self.backend_record.shipping_product_id:
            return {'product_id': self.backend_record.shipping_product_id.id}
        prod_mod = self.session.pool['product.product']
        default_ship_product = prod_mod.search(
                self.session.cr,
                self.session.uid,
                [('default_code', '=', 'SHIP'),
                 ('company_id', '=', self.backend_record.company_id.id)],
        )
        if default_ship_product:
            return {'product_id': default_ship_product[0]}
        return {}

    @mapping
    def partner_id(self, record):
        partner_pool = self.session.pool['res.partner']
        default_partner = partner_pool.search(
                self.session.cr,
                self.session.uid,
                [],
        )[0]
        return {'partner_id': default_partner}

    @mapping
    def tienda_nube_id(self, record):
        return {'tienda_nube_id': record['id']}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}


@tienda_nube
class DeliveryCarrierBatchImport(DelayedBatchImporter):
    """ Import the TiendaNube Carriers.
    """
    _model_name = ['tienda_nube.delivery.carrier']

    def run(self, filters=None, **kwargs):
        """ Run the synchronization """
        record_ids = self.backend_adapter.search()
        _logger.info('search for tienda_nube carriers %s returned %s',
                     filters, record_ids)
        for record_id in record_ids:
            self._import_record(record_id, **kwargs)


@job(default_channel='root.tienda_nube')
def import_carriers(session, backend_id):
    import_batch(
            session, 'tienda_nube.delivery.carrier', backend_id, priority=5
    )
