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
        default=get_default_partner_sequence
    )
    purchase_licenses = fields.Boolean('Compra de licencias')
    system_implementation = fields.Boolean('Implementación de sistemas')
    system_customization = fields.Boolean('Personalización de sistemas')
    training = fields.Boolean('Capacitación')
    hardware_software = fields.Boolean('Hardware o Software')
    have_systems_area = fields.Boolean('Cuentan con area de sistemas')
    computers_in_network = fields.Integer('Cuantos equipo hay en su red')
    description = fields.Text('Descripción')


    @api.model
    def create(self, vals):
        rec = super(ResPartner, self).create(vals)
        current_sequence = self.get_default_partner_sequence()
        if(rec.partner_sequence == current_sequence):
            vals['partner_sequence'] = \
            self.env['ir.sequence'].next_by_code('sequence.res.partner')

        return rec
