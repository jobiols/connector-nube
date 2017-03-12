# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    tienda_nube_synchronized = fields.Boolean(
            string='Sync with TiendaNube',
            help='Check this option to synchronize this location with TiendaNube')

    @api.model
    def get_tienda_nube_stock_locations(self):
        tienda_nube_locations = self.search([
            ('tienda_nube_synchronized', '=', True),
            ('usage', '=', 'internal'),
        ])
        return tienda_nube_locations
