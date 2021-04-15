# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
import logging

_logger = logging.getLogger(__name__)


class ResRenewal(models.Model):
    _name = 'res.renewal'
    _description = 'Renovaciones'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    def _compute_name(self):
        sequence = self.env['ir.sequence'].next_by_code('sequence.res.renewal')
        return sequence

    name = fields.Char(string=u'Número', default=_compute_name, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date_start = fields.Date(string='Fecha Inicio', required=True)
    date_end = fields.Date(string='Fecha Fin')
    to_expire = fields.Boolean(string=u'Próxima a expirar', default=False, readonly=False)
    state = fields.Selection(selection=[
        ('draft', 'Borrador'),
        ('process', 'Vigente'),
        ('expired', 'Vencido'),
        ('cancel', 'Cancelado')], string='Estado', required=True, readonly=True, default='draft')

    type = fields.Selection(related='partner_id.type')
    is_company = fields.Boolean(related='partner_id.is_company')
    street = fields.Char(related='partner_id.street')
    street2 = fields.Char(related='partner_id.street2')
    city = fields.Char(string='Ciudad', related='partner_id.city')
    state_id = fields.Many2one(string='Estado', related='partner_id.state_id')
    zip = fields.Char(string='C.P.', related='partner_id.zip')
    country_id = fields.Many2one(string=u'País', related='partner_id.country_id')
    vat = fields.Char(string='RFC', related='partner_id.vat')
    parent_id = fields.Many2one(string=u'Compañía', related='partner_id.parent_id')
    company_name = fields.Char(string=u'Nombre Compañía', related='partner_id.company_name')

    function = fields.Char(string='Puesto de trabajo', related='partner_id.function')
    phone = fields.Char(string=u'Teléfono', related='partner_id.phone')
    mobile = fields.Char(string='Celular', related='partner_id.mobile')
    email = fields.Char(string='Email', related='partner_id.email')
    website = fields.Char(string='Sitio Web', related='partner_id.website')
    title = fields.Many2one(string=u'Título', related='partner_id.title')
    category_id = fields.Many2many(string=u'Categorías', related='partner_id.category_id')
    # ------------------------------------------------------
    purchase_licenses = fields.Boolean('Compra de licencias')
    system_implementation = fields.Boolean('Implementación de sistemas')
    system_customization = fields.Boolean('Personalización de sistemas')
    training = fields.Boolean('Capacitación')
    hardware_software = fields.Boolean('Hardware o Software')
    have_systems_area = fields.Boolean('Cuentan con area de sistemas')
    computers_in_network = fields.Integer('Cuantos equipo hay en su red')
    description_aesa = fields.Text('Descripción')
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
        [('0', 'Sin servidor'), ('1', 'Servidor propio')],
        'Cuentan con servidor'
    )
    server_type = fields.Selection(
        [('local', 'Servidor local'), ('cloud', 'Propio cloud')],
        'Tipo de servidor'
    )
    recurring_customer = fields.Selection(
        [('0', 'No'), ('1', 'Si')], 'Cliente recurrente de timbres'
    )
    number_rings = fields.Selection(
        [('50', '50'),
         ('200', '200'),
         ('400', '400'),
         ('1000', '1000'),
         ('2000', '2000'),
         ('5000', '5000'),
         ('10000', '10000'),
         ('20000', '20000'),
         ('50000', '50000'),
         ('70000', '70000'),
         ('100000', '100000')],
        'Número de timbres'
    )
    last_sale = fields.Date('Fecha de última venta')
    aspel_systems = fields.One2many(
        'aspel.system',
        'partner_id'
    )

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_process(self):
        self.write({'state': 'process'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_expired(self):
        self.write({'state': 'expired'})

    def action_to_expire(self):
        self.write({'to_expire': True})

    def action_renovations_to_expire(self):
        # ren_conf = self.env['res.renewal.config'].search()
        ren_conf = {'days_to_expire': 1}
        if ren_conf and ren_conf['days_to_expire']:
            _logger.info("::::: Planificador de Renovaciones a vencer ejecutado! :::::")
            # days = int(ren_conf.days_to_expire)
            days = int(ren_conf['days_to_expire'])
            date_exp = (datetime.now() + timedelta(days=days)).date()
            domain = [('date_end', '<=', date_exp),
                      ('state', '=', 'process')
                      ]
            ren_ids = self.search(domain)
            for ren in ren_ids:
                ren.action_to_expire()
        else:
            _logger.info(u"::::: No está establecida la opción de 'Días antes de vencimiento' en la configuración "
                         u"de Renovaciones! :::::")
        # raise Warning('Dias antes vencer: %s' % date_exp)

    def schedule_renovations(self):
        _logger.info("::::: Starting Renovations schedule :::::")
        dominio = [('date_end', '<=', date.today()),
                   ('state', '=', 'process'),
                   ]
        renov_ids = self.search(dominio)
        self.action_renovations_to_expire()
        for ren in renov_ids:
            ren.action_expired()
        _logger.info("::::: Finished Renovations schedule :::::")
