# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from ...unit.mapper import backend_to_m2o
from ...unit.importer import TiendaNubeImporter, DirectBatchImporter
from ...backend import tienda_nube


@tienda_nube
class ShopImportMapper(ImportMapper):
    _model_name = 'tienda_nube.shop'

    direct = [
        ('name', 'name'),
        (backend_to_m2o('id_shop_group'), 'shop_group_id'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}

    @mapping
    def warehouse_id(self, record):
        return {'warehouse_id': self.backend_record.warehouse_id.id}

    @mapping
    def opener_id(self, record):
        return {'odoo_id': self.backend_record.warehouse_id.id}


@tienda_nube
class ShopImporter(TiendaNubeImporter):
    _model_name = 'tienda_nube.shop'


@tienda_nube
class ShopBatchImporter(DirectBatchImporter):
    _model_name = 'tienda_nube.shop'
