# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_default_partner_sequence(self):
        sequence = self.env['ir.sequence'].search(
            [('code','=','sequence.res.partner')]
            )
        next = sequence.get_next_char(sequence.number_next_actual)

        return next

    partner_sequence = fields.Char(
        string="identificador",
        size=24,
        default=get_default_partner_sequence,
        readonly=True
    )
    purchase_licenses = fields.Boolean('Compra de licencias')
    system_implementation = fields.Boolean('Implementación de sistemas')
    system_customization = fields.Boolean('Personalización de sistemas')
    training = fields.Boolean('Capacitación')
    hardware_software = fields.Boolean('Hardware o Software')
    have_systems_area = fields.Boolean('Cuentan con area de sistemas')
    computers_in_network = fields.Integer('Cuantos equipo hay en su red')
    description = fields.Text('Descripción')
    renewals_count = fields.Integer(compute='_compute_renewals_count', string=u"Número de Renovaciones")
    has_renewal = fields.Boolean(compute='_compute_renewals_count', store=True)

    def _compute_renewals_count(self):
        renewals = self.env['res.renewal']
        for record in self:
            record.has_renewal = False
            record.renewals_count = renewals.search_count([('partner_id', '=', record.id)])
            if record.renewals_count > 0:
                record.has_renewal = True

    @api.model
    def create(self, vals):
        rec = super(ResPartner, self).create(vals)
        current_sequence = self.get_default_partner_sequence()
        if(rec.partner_sequence == current_sequence):
            vals['partner_sequence'] = \
            self.env['ir.sequence'].next_by_code('sequence.res.partner')

        return rec

    def renewals_tree_view(self):
        return {
            "name": "Renovaciones",
            'type': 'ir.actions.act_window',
            'res_model': 'res.renewal',
            'view_mode': 'tree',
            'views': [(False, 'tree')],
            'context': {'default_partner_id': self.id},
            'domain': [('partner_id', '=', self.id)]
        }
