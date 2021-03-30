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
