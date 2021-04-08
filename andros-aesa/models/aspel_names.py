# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class AspelNames(models.Model):
    _name = 'aspel.names'

    name = fields.Char('Nombre')
