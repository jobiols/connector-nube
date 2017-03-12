# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


@tienda_nube
class OrderCarriers(GenericAdapter):
    _model_name = '__not_exit_tienda_nube.order_carrier'
    _tienda_nube_model = 'order_carriers'
    _export_node_name = 'order_carrier'
