# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class ResRenewal(models.Model):
    _name = 'res.renewal'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    def _compute_name(self):
        sequence = self.env['ir.sequence'].next_by_code('sequence.res.renewal')
        return sequence

    name = fields.Char(string=u'Número', default=_compute_name, readonly=True)
    state = fields.Selection(selection=[
        ('draft', 'Borrador'),
        ('confirm', 'Confirmado'),
        ('expired', 'Vencido'),
        ('cancel', 'Cancelado')], string='Estado', required=True, readonly=True, default='draft')

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
