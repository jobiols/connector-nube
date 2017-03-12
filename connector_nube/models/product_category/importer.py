# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from ...backend import tienda_nube
from ...unit.importer import (
    DelayedBatchImporter,
    TranslatableRecordImporter,
)
from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from ...unit.mapper import backend_to_m2o

_logger = logging.getLogger(__name__)

try:
    from prestapyt import TiendaNubeWebServiceError
except ImportError:
    _logger.debug('Can not `from prestapyt import TiendaNubeWebServiceError`.')


@tienda_nube
class ProductCategoryMapper(ImportMapper):
    _model_name = 'tienda_nube.product.category'

    direct = [
        ('position', 'sequence'),
        ('description', 'description'),
        ('link_rewrite', 'link_rewrite'),
        ('meta_description', 'meta_description'),
        ('meta_keywords', 'meta_keywords'),
        ('meta_title', 'meta_title'),
        (backend_to_m2o('id_shop_default'), 'default_shop_id'),
        ('active', 'active'),
        ('position', 'position')
    ]

    @mapping
    def name(self, record):
        if record['name'] is None:
            return {'name': ''}
        return {'name': record['name']}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def parent_id(self, record):
        if record['id_parent'] == '0':
            return {}
        return {
            'parent_id':
                self.binder_for('tienda_nube.product.category').to_odoo(
                        record['id_parent'], unwrap=True).id}

    @mapping
    def data_add(self, record):
        if record['date_add'] == '0000-00-00 00:00:00':
            return {'date_add': datetime.now()}
        return {'date_add': record['date_add']}

    @mapping
    def data_upd(self, record):
        if record['date_upd'] == '0000-00-00 00:00:00':
            return {'date_upd': datetime.now()}
        return {'date_upd': record['date_upd']}


@tienda_nube
class ProductCategoryImport(TranslatableRecordImporter):
    _model_name = [
        'tienda_nube.product.category',
    ]

    _translatable_fields = {
        'tienda_nube.product.category': [
            'name',
            'description',
            'link_rewrite',
            'meta_description',
            'meta_keywords',
            'meta_title'
        ],
    }

    def _import_dependencies(self):
        record = self.tienda_nube_record
        if record['id_parent'] != '0':
            try:
                self._import_dependency(
                        record['id_parent'], 'tienda_nube.product.category')
            except TiendaNubeWebServiceError:
                pass


@tienda_nube
class ProductCategoryBatchImporter(DelayedBatchImporter):
    _model_name = 'tienda_nube.product.category'
