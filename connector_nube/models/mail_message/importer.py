# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from ...backend import tienda_nube
from ...unit.importer import TiendaNubeImporter, DelayedBatchImporter
from openerp.addons.connector.unit.mapper import ImportMapper, mapping

_logger = logging.getLogger(__name__)


@tienda_nube
class MailMessageMapper(ImportMapper):
    _model_name = 'tienda_nube.mail.message'

    direct = [
        ('message', 'body'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def type(self, record):
        return {'type': 'comment'}

    @mapping
    def object_ref(self, record):
        binder = self.binder_for('tienda_nube.sale.order')
        order = binder.to_odoo(record['id_order'], unwrap=True)
        return {
            'model': 'sale.order',
            'res_id': order.id,
        }

    @mapping
    def author_id(self, record):
        if record['id_customer'] != '0':
            binder = self.binder_for('tienda_nube.res.partner')
            partner = binder.to_odoo(record['id_customer'], unwrap=True)
            return {'author_id': partner.id}
        return {}


@tienda_nube
class MailMessageRecordImport(TiendaNubeImporter):
    """ Import one simple record """
    _model_name = 'tienda_nube.mail.message'

    def _import_dependencies(self):
        record = self.tienda_nube_record
        self._import_dependency(record['id_order'], 'tienda_nube.sale.order')
        if record['id_customer'] != '0':
            self._import_dependency(
                    record['id_customer'], 'tienda_nube.res.partner'
            )

    def _has_to_skip(self):
        record = self.tienda_nube_record
        binder = self.binder_for('tienda_nube.sale.order')
        ps_so_id = binder.to_odoo(record['id_order']).id
        return record['id_order'] == '0' or not ps_so_id


@tienda_nube
class MailMessageBatchImporter(DelayedBatchImporter):
    _model_name = 'tienda_nube.mail.message'
