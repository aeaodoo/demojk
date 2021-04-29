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
        string="Identificador",
        size=24,
        readonly=True
    )
    renewals_count = fields.Integer(compute='_compute_renewals_count', string=u"Número de Renovaciones")
    has_renewal = fields.Boolean(compute='_compute_renewals_count', store=True)
    purchase_licenses = fields.Boolean('Compra de licencias')
    system_implementation = fields.Boolean(u'Implementación de sistemas')
    system_customization = fields.Boolean(u'Personalización de sistemas')
    training = fields.Boolean(u'Capacitación')
    hardware_software = fields.Boolean('Hardware o Software')
    have_systems_area = fields.Boolean('Cuentan con area de sistemas')
    computers_in_network = fields.Integer('Cuantos equipo hay en su red')
    description_aesa = fields.Text('Descripción')
    description_crm = fields.Text('Notas internas')
    personality = fields.Selection(
        [
            ('amarillo', 'Amarillo'),
            ('verde', 'Verde'),
            ('azul', 'Azul'),
            ('Rojo', 'Rojo'),
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

    has_server = fields.Selection(
        [('0', 'Sin servidor'),('1', 'Servidor propio')],
        'Cuentan con servidor'
    )
    server_type = fields.Selection(
        [
            ('local', 'Servidor local'),
            ('cloud', 'Propio cloud'),
        ],
        'Tipo de servidor'
    )
    own_server = fields.Selection(
        [
            ('cloud_aesa', 'Cloud AESA'),
            ('cloud_basico', 'Cloud básico'),
            ('cloud_estandar', 'Cloud Server estándar'),
            ('cloud_premium', 'Cloud Server premium'),
            ('cloud_flex', 'Cloud Server flex'),
            ('cloud_l', 'Cloud Server L'),
            ('cloud_xl', 'Cloud Server XL'),
            ('cloud_xxl', 'Cloud Server XXL'),
            ('cloud_xxxl', 'Cloud Server XXXL'),
            ('cloud_dedicado', 'Cloud Server dedicado'),
        ],
        'Servidor propio'
    )
    cut_date = fields.Date('Fecha de corte')
    ip_server = fields.Char(u'Dirección IP')
    url_server = fields.Char('OP Activa (URL)')
    recurring_customer = fields.Selection(
        [('0', 'No'),('1', 'Si')], 'Cliente recurrente de timbres'
    )
    number_rings = fields.Selection(
        [('50','50'),
        ('200','200'),
        ('400','400'),
        ('1000','1000'),
        ('2000','2000'),
        ('5000','5000'),
        ('10000','10000'),
        ('20000','20000'),
        ('50000','50000'),
        ('70000','70000'),
        ('100000','100000')],
        'Número de timbres'
    )
    last_sale = fields.Date(u'Fecha de última venta')
    aspel_systems = fields.One2many(
        'aspel.system',
        'partner_id'
    )

    def _compute_renewals_count(self):
        renewals = self.env['res.renewal']
        for record in self:
            record.has_renewal = False
            record.renewals_count = renewals.search_count([('partner_id', '=', record.id)])
            if record.renewals_count > 0:
                record.has_renewal = True

    @api.model
    def create(self, vals):
        vals['partner_sequence'] = self.env['ir.sequence'].next_by_code('sequence.res.partner')
        rec = super(ResPartner, self).create(vals)
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
