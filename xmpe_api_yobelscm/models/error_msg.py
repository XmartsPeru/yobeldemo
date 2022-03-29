from odoo import fields, models, api, _


class ErrorMessage(models.Model):
    _name = 'xmpe.error.msg'
    _description = 'Error Message'

    code = fields.Char(string=_('Code'), required=True)
    description = fields.Char(string=_('Description'), required=True)
