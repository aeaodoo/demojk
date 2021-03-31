# -*- coding: utf-8 -*-

{
    'name': 'AESA',
    'version': '1.0',
    'category': 'Extras',
    'summary': 'Modifications for AESA',
    'description': """
Modifications for AESA.
========================================
    """,
    'website': 'http://www.ikom.mx',
    'depends': [
        'crm',
        'sale_subscription'
    ],
    'data': [
        'security/security.xml',
        'data/sequences.xml',
        'data/cron_data.xml',
        'views/crm_lead_view.xml',
        'views/res_partner_view.xml',
        'views/res_renewal_views.xml',

    ],
    'application': False,
}
