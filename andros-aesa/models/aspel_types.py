# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class AspelTypes(models.Model):
    _name = 'aspel.types'

    name = fields.Char('Nombre')
    value_type = fields.Selection([
        ('meses', 'Meses'),
        ('dias', 'Días'),
        ('bimestres', 'Bimestres'),
        ('Trimestres', 'Trimestres'),
        ('year', 'Años'),
    ], 'Tipo valor')
    value = fields.Integer('Valor')
