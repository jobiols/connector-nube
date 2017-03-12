# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube

_logger = logging.getLogger(__name__)

try:
    from prestapyt import TiendaNubeWebServiceDict
except ImportError:
    _logger.debug('Can not `from prestapyt import TiendaNubeWebServiceDict.')


@tienda_nube
class PaymentMethodAdapter(GenericAdapter):
    _model_name = 'payment.method'
    _tienda_nube_model = 'orders'
    _export_node_name = 'order'

    def search(self, filters=None):
        api = TiendaNubeWebServiceDict(
                self.tienda_nube.api_url, self.tienda_nube.webservice_key)
        res = api.get(self._tienda_nube_model, options=filters)
        methods = res[self._tienda_nube_model][self._export_node_name]
        if isinstance(methods, dict):
            return [methods]
        return methods
