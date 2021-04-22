# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class AspelSystem(models.Model):
    _name = 'aspel.system'
    _description = 'Aspel System'
    _rec_name = 'aspel_id'

    def get_user_numbers_selection(self):
        selection = []
        for x in range(1, 51):
            val = str(x)
            tpl = (val, val)
            selection.append(tpl)

        return selection

    aspel_id = fields.Many2one('aspel.names', string='Nombre', required=True)
    user_numbers = fields.Selection(
        get_user_numbers_selection, 'Número de usuarios'
    )
    serial_number_aesa = fields.Char('Número de serie')
    version = fields.Char('Versión')
    type_id = fields.Many2one('aspel.types', string='Tipo', required=True)
    lead_id = fields.Many2one('crm.lead', string='Oportunidad')
    partner_id = fields.Many2one('res.partner', string='Cliente')
    new_date = fields.Date('Fecha renovación')
