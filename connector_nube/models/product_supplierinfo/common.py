# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import (
    TiendaNubeCRUDAdapter,
    TiendaNubeWebServiceImage,
    GenericAdapter
)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tienda_nube_supplier_bind_ids = fields.One2many(
            comodel_name='tienda_nube.supplier',
            inverse_name='odoo_id',
            string="TiendaNube supplier bindings",
    )


class TiendaNubeSupplier(models.Model):
    _name = 'tienda_nube.supplier'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.partner': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='res.partner',
            string='Partner',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.supplierinfo',
            inverse_name='odoo_id',
            string="TiendaNube bindings",
    )


class TiendaNubeProductSupplierinfo(models.Model):
    _name = 'tienda_nube.product.supplierinfo'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'product.supplierinfo': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.supplierinfo',
            string='Supplier info',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )


@tienda_nube
class SupplierImageAdapter(TiendaNubeCRUDAdapter):
    _model_name = 'tienda_nube.supplier.image'
    _tienda_nube_image_model = 'suppliers'

    def read(self, supplier_id, options=None):
        api = TiendaNubeWebServiceImage(self.tienda_nube.api_url,
                                        self.tienda_nube.webservice_key)
        res = api.get_image(
                self._tienda_nube_image_model,
                supplier_id,
                options=options
        )
        return res['content']


@tienda_nube
class SupplierAdapter(GenericAdapter):
    _model_name = 'tienda_nube.supplier'
    _tienda_nube_model = 'suppliers'


@tienda_nube
class SupplierInfoAdapter(GenericAdapter):
    _model_name = 'tienda_nube.product.supplierinfo'
    _tienda_nube_model = 'product_suppliers'
