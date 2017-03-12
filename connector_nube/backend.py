# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.addons.connector.backend as backend

tienda_nube = backend.Backend('tienda_nube')
# version < 1.6.0.9
tienda_nube1500 = backend.Backend(parent=tienda_nube, version='1.5')
# version 1.6.0.9 - 1.6.0.10
tienda_nube1609 = backend.Backend(parent=tienda_nube, version='1.6.0.9')
# version >= 1.6.0.11
tienda_nube16011 = backend.Backend(parent=tienda_nube, version='1.6.0.11')
tienda_nube1612 = backend.Backend(parent=tienda_nube, version='1.6.1.2')
