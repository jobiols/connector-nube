# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp import fields, models

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.mail.message',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )


class TiendaNubeMailMessage(models.Model):
    _name = "tienda_nube.mail.message"
    _inherit = "tienda_nube.binding.odoo"
    _inherits = {'mail.message': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='mail.message',
            required=True,
            ondelete='cascade',
            string='Message',
            oldname='openerp_id',
    )


@tienda_nube
class MailMessageAdapter(GenericAdapter):
    _model_name = 'tienda_nube.mail.message'
    _tienda_nube_model = 'messages'
