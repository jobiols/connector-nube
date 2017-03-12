# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from datetime import datetime
from openerp.addons.connector.exception import NothingToDoJob

from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.mapper import ImportMapper, mapping

from ...backend import tienda_nube
from ...unit.importer import (
    DelayedBatchImporter,
    TiendaNubeImporter,
    import_batch,
)
from ...unit.backend_adapter import TiendaNubeCRUDAdapter
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

try:
    from prestapyt import TiendaNubeWebServiceError
except ImportError:
    _logger.debug('Can not `from prestapyt import TiendaNubeWebServiceError`.')


@tienda_nube
class SupplierMapper(ImportMapper):
    _model_name = 'tienda_nube.supplier'

    direct = [
        ('name', 'name'),
        ('id', 'tienda_nube_id'),
        ('active', 'active'),
    ]

    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def supplier(self, record):
        return {
            'supplier': True,
            'is_company': True,
            'customer': False,
        }

    @mapping
    def image(self, record):
        supplier_image_adapter = self.unit_for(
                TiendaNubeCRUDAdapter, 'tienda_nube.supplier.image'
        )
        try:
            return {'image': supplier_image_adapter.read(record['id'])}
        except:
            return {}


@tienda_nube
class SupplierRecordImport(TiendaNubeImporter):
    """ Import one simple record """
    _model_name = 'tienda_nube.supplier'

    def _create(self, record):
        try:
            return super(SupplierRecordImport, self)._create(record)
        except ZeroDivisionError:
            del record['image']
            return super(SupplierRecordImport, self)._create(record)

    def _after_import(self, erp_id):
        binder = self.binder_for(self._model_name)
        ps_id = binder.to_backend(erp_id)
        import_batch(
                self.session,
                'tienda_nube.product.supplierinfo',
                self.backend_record.id,
                filters={'filter[id_supplier]': '%d' % ps_id},
                priority=10,
        )


@tienda_nube
class SupplierBatchImporter(DelayedBatchImporter):
    _model_name = 'tienda_nube.supplier'


@tienda_nube
class SupplierInfoMapper(ImportMapper):
    _model_name = 'tienda_nube.product.supplierinfo'

    direct = [
        ('product_supplier_reference', 'product_code'),
    ]

    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def name(self, record):
        binder = self.binder_for('tienda_nube.supplier')
        partner = binder.to_odoo(record['id_supplier'], unwrap=True)
        return {'name': partner.id}

    @mapping
    def product_id(self, record):
        binder = self.binder_for('tienda_nube.product.combination')
        if record['id_product_attribute'] != '0':
            return {'product_id': binder.to_odoo(
                    record['id_product_attribute'], unwrap=True).id}
        return {
            'product_id': binder.to_odoo(record['id_product'], unwrap=True).id,
        }

    @mapping
    def product_tmpl_id(self, record):
        binder = self.binder_for('tienda_nube.product.template')
        erp_id = binder.to_odoo(record['id_product'], unwrap=True)
        return {'product_tmpl_id': erp_id.id}

    @mapping
    def required(self, record):
        return {'min_qty': 0.0, 'delay': 1}


@tienda_nube
class SupplierInfoImport(TiendaNubeImporter):
    _model_name = 'tienda_nube.product.supplierinfo'

    def _import_dependencies(self):
        record = self.tienda_nube_record
        try:
            self._import_dependency(
                    record['id_supplier'], 'tienda_nube.supplier'
            )
            self._import_dependency(
                    record['id_product'], 'tienda_nube.product.template'
            )

            if record['id_product_attribute'] != '0':
                self._import_dependency(
                        record['id_product_attribute'],
                        'tienda_nube.product.combination'
                )
        except TiendaNubeWebServiceError:
            raise NothingToDoJob('Error fetching a dependency')


@tienda_nube
class SupplierInfoBatchImporter(DelayedBatchImporter):
    _model_name = 'tienda_nube.product.supplierinfo'


@job(default_channel='root.tienda_nube')
def import_suppliers(session, backend_id, since_date):
    filters = None
    if since_date:
        filters = {'date': '1', 'filter[date_upd]': '>[%s]' % (since_date)}
    now_fmt = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    import_batch(session, 'tienda_nube.supplier', backend_id, filters)
    import_batch(session, 'tienda_nube.product.supplierinfo', backend_id)
    session.env['tienda_nube.backend'].browse(backend_id).write({
        'import_suppliers_since': now_fmt
    })
