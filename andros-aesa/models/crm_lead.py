# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def get_default_lead_sequence(self):
        sequence = self.env['ir.sequence'].search(
            [('code','=','sequence.lead')]
            )
        next = sequence.get_next_char(sequence.number_next_actual)

        return next

    def get_default_opportunity_sequence(self):
        sequence = self.env['ir.sequence'].search(
            [('code','=','sequence.opportunity')]
        )
        next = sequence.get_next_char(sequence.number_next_actual)

        return next

    lead_sequence = fields.Char(
        string="Iniciativa",
        size=24,
        default=get_default_lead_sequence
    )
    opportunity_sequence = fields.Char(
        string="Oportunidad",
        size=24,
        default=get_default_opportunity_sequence
    )

    purchase_licenses = fields.Boolean('Compra de licencias')
    system_implementation = fields.Boolean('Implementación de sistemas')
    system_customization = fields.Boolean('Personalización de sistemas')
    training = fields.Boolean('Capacitación')
    hardware_software = fields.Boolean('Hardware o Software')
    have_systems_area = fields.Boolean('Cuentan con area de sistemas')
    computers_in_network = fields.Integer('Cuantos equipo hay en su red')
    description = fields.Text('Descripción')
    personality = fields.Selection(
        [
            ('amarillo', 'Amarillo'),
            ('verde', 'Verde'),
            ('azul', 'Azul'),
            ('Rojo', 'rojo'),
        ],
        'Personalidad del cliente'
    )
    necessity = fields.Selection([
        ('25_1', 'Compra de licencias'),
        ('25_2', 'Suscripción'),
        ('25_3', 'Timbres'),
        ('25_4', 'Implementación de sistemas'),
        ('25_5', 'Personalización de sistemas'),
        ('25_6', 'Capacitación'),
        ('25_7', 'Software y Hardware'),
    ], 'Necesidad')
    impact = fields.Selection([
        ('5', 'Bajo'),
        ('15', 'Medio'),
        ('25', 'Alto'),
    ], 'Impacto')
    time = fields.Selection([
        ('25', 'Inmediato'),
        ('17', '1 Semana'),
        ('12', '2 Semanas'),
        ('7', 'Tiempo indefinido'),
    ], 'Tiempo')
    authority = fields.Selection([
        ('25', 'Contacto principal'),
        ('17', 'Jefe inmediato'),
        ('12', 'Director'),
        ('7', 'Consejo'),
    ], 'Autoridad')

    @api.onchange('necessity', 'impact', 'time', 'authority')
    def on_change_probability_values(self):
        sum = 0
        if(self.necessity):
            sum += int(self.necessity.split('_')[0])
        if(self.impact):
            sum += int(self.impact)
        if(self.time):
            sum += int(self.time)
        if(self.authority):
            sum += int(self.authority)

        self.probability = sum

    @api.model
    def create(self, vals):
        rec = super(CrmLead, self).create(vals)
        if(rec.type == 'opportunity'):
            current_sequence = self.get_default_opportunity_sequence()
            if(rec.opportunity_sequence == current_sequence):
                vals['opportunity_sequence'] = \
                self.env['ir.sequence'].next_by_code('sequence.opportunity')
        else:
            current_sequence = self.get_default_lead_sequence()
            if(rec.lead_sequence == current_sequence):
                vals['lead_sequence'] = \
                self.env['ir.sequence'].next_by_code('sequence.lead')

        return rec
