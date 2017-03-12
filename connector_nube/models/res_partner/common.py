# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.res.partner',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )
    tienda_nube_address_bind_ids = fields.One2many(
            comodel_name='tienda_nube.address',
            inverse_name='odoo_id',
            string='TiendaNube Address Bindings',
    )


class TiendaNubeResRartner(models.Model):
    _name = 'tienda_nube.res.partner'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.partner': 'odoo_id'}

    _rec_name = 'shop_group_id'

    odoo_id = fields.Many2one(
            comodel_name='res.partner',
            string='Partner',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    backend_id = fields.Many2one(
            related='shop_group_id.backend_id',
            comodel_name='tienda_nube.backend',
            string='TiendaNube Backend',
            store=True,
            readonly=True,
    )
    shop_group_id = fields.Many2one(
            comodel_name='tienda_nube.shop.group',
            string='TiendaNube Shop Group',
            required=True,
            ondelete='restrict',
    )
    shop_id = fields.Many2one(
            comodel_name='tienda_nube.shop',
            string='TiendaNube Shop',
    )
    group_ids = fields.Many2many(
            comodel_name='tienda_nube.res.partner.category',
            relation='tienda_nube_category_partner',
            column1='partner_id',
            column2='category_id',
            string='TiendaNube Groups',
    )
    date_add = fields.Datetime(
            string='Created At (on TiendaNube)',
            readonly=True,
    )
    date_upd = fields.Datetime(
            string='Updated At (on TiendaNube)',
            readonly=True,
    )
    newsletter = fields.Boolean(string='Newsletter')
    default_category_id = fields.Many2one(
            comodel_name='tienda_nube.res.partner.category',
            string='TiendaNube default category',
            help="This field is synchronized with the field "
                 "'Default customer group' in TiendaNube."
    )
    birthday = fields.Date(string='Birthday')
    company = fields.Char(string='Company')
    tienda_nube_address_bind_ids = fields.One2many(
            comodel_name='tienda_nube.address',
            inverse_name='odoo_id',
            string='TiendaNube Address Bindings',
    )


class TiendaNubeAddress(models.Model):
    _name = 'tienda_nube.address'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.partner': 'odoo_id'}

    _rec_name = 'backend_id'

    @api.multi
    @api.depends(
            'tienda_nube_partner_id',
            'tienda_nube_partner_id.backend_id',
            'tienda_nube_partner_id.shop_group_id',
    )
    def _compute_backend_id(self):
        for address in self:
            address.backend_id = address.tienda_nube_partner_id.backend_id.id

    @api.multi
    @api.depends('tienda_nube_partner_id',
                 'tienda_nube_partner_id.shop_group_id')
    def _compute_shop_group_id(self):
        for address in self:
            address.shop_group_id = (
                address.tienda_nube_partner_id.shop_group_id.id)

    odoo_id = fields.Many2one(
            comodel_name='res.partner',
            string='Partner',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    date_add = fields.Datetime(
            string='Created At (on TiendaNube)',
            readonly=True,
    )
    date_upd = fields.Datetime(
            string='Updated At (on TiendaNube)',
            readonly=True,
    )
    tienda_nube_partner_id = fields.Many2one(
            comodel_name='tienda_nube.res.partner',
            string='TiendaNube Partner',
            required=True,
            ondelete='cascade',
    )
    backend_id = fields.Many2one(
            compute='_compute_backend_id',
            comodel_name='tienda_nube.backend',
            string='TiendaNube Backend',
            store=True,
    )
    shop_group_id = fields.Many2one(
            compute='_compute_shop_group_id',
            comodel_name='tienda_nube.shop.group',
            string='TiendaNube Shop Group',
            store=True,
    )
    vat_number = fields.Char('TiendaNube VAT')


@tienda_nube
class PartnerAdapter(GenericAdapter):
    _model_name = 'tienda_nube.res.partner'
    _tienda_nube_model = 'customers'


@tienda_nube
class PartnerAddressAdapter(GenericAdapter):
    _model_name = 'tienda_nube.address'
    _tienda_nube_model = 'addresses'
