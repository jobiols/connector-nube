# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from ...unit.importer import (
    import_record,
    DelayedBatchImporter,
    TranslatableRecordImporter
)
from ...backend import tienda_nube


@tienda_nube
class PartnerCategoryImportMapper(ImportMapper):
    _model_name = 'tienda_nube.res.partner.category'

    direct = [
        ('name', 'name'),
        ('date_add', 'date_add'),
        ('date_upd', 'date_upd'),
    ]

    @mapping
    def tienda_nube_id(self, record):
        return {'tienda_nube_id': record['id']}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}


@tienda_nube
class PartnerCategoryRecordImport(TranslatableRecordImporter):
    """ Import one translatable record """
    _model_name = [
        'tienda_nube.res.partner.category',
    ]

    _translatable_fields = {
        'tienda_nube.res.partner.category': ['name'],
    }

    def _after_import(self, erp_id):
        record = self._get_tienda_nube_data()
        if float(record['reduction']):
            import_record(
                self.session,
                    'tienda_nube.groups.pricelist',
                self.backend_record.id,
                record['id']
            )


@tienda_nube
class PartnerCategoryBatchImporter(DelayedBatchImporter):
    _model_name = 'tienda_nube.res.partner.category'
