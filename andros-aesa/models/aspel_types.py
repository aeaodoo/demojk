# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class AspelTypes(models.Model):
    _name = 'aspel.types'
    _description = 'Aspel Type'

    name = fields.Char('Nombre', required=True)
    value_type = fields.Selection([
        ('meses', 'Meses'),
        ('dias', 'Días'),
        ('bimestres', 'Bimestres'),
        ('trimestres', 'Trimestres'),
        ('year', 'Años'),
    ], 'Tipo valor', required=True, default='meses')
    value = fields.Integer('Valor', default=1)
