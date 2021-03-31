# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class AspelSystem(models.Model):
    _name = 'aspel.system'

    name = fields.Char('Nombre')
