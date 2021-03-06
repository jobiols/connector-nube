# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.refund',
            inverse_name='odoo_id',
            string='TiendaNube Bindings'
    )

    def action_move_create(self):
        so_obj = self.env['tienda_nube.sale.order']
        line_replacement = {}
        for invoice in self:
            sale_order = so_obj.search([('name', '=', invoice.origin)])
            if not sale_order:
                continue
            sale_order = sale_order[0]
            discount_product_id = sale_order.backend_id.discount_product_id.id
            for invoice_line in invoice.invoice_line:
                if invoice_line.product_id.id != discount_product_id:
                    continue
                amount = invoice_line.price_subtotal
                partner = invoice.partner_id.commercial_partner_id
                refund = self._find_refund(-1 * amount, partner)
                if refund:
                    invoice_line.unlink()
                    line_replacement[invoice] = refund
                    invoice.button_reset_taxes()
        result = super(AccountInvoice, self).action_move_create()
        # reconcile invoice with refund
        for invoice, refund in line_replacement.items():
            self._reconcile_invoice_refund(invoice, refund)
        return result

    @api.model
    def _reconcile_invoice_refund(self, invoice, refund):
        move_line_obj = self.env['account.move.line']
        move_lines = move_line_obj.search([
            ('move_id', '=', invoice.move_id.id),
            ('debit', '!=', 0.0),
        ])
        move_lines += move_line_obj.search([
            ('move_id', '=', refund.move_id.id),
            ('credit', '!=', 0.0),
        ])
        move_lines.reconcile_partial()

    @api.model
    def _find_refund(self, amount, partner):
        records = self.search([
            ('amount_untaxed', '=', amount),
            ('type', '=', 'out_refund'),
            ('state', '=', 'open'),
            ('partner_id', '=', partner.id),
        ])
        return records[:1].id


class TiendaNubeRefund(models.Model):
    _name = 'tienda_nube.refund'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'account.invoice': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='account.invoice',
            required=True,
            ondelete='cascade',
            string='Invoice',
            oldname='openerp_id',
    )


@tienda_nube
class RefundAdapter(GenericAdapter):
    _model_name = 'tienda_nube.refund'

    @property
    def _tienda_nube_model(self):
        return self.backend_record.get_version_ps_key('order_slip')
