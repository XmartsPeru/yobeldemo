from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    yobel_identifier = fields.Char(string=_('Yobel Identifier'),)
