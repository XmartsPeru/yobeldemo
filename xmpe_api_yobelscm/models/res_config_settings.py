from odoo import fields, models, api, _


class YobelSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company = fields.Char(string=_('Company'), )
    username = fields.Char(string=_('Username'), )
    passwd = fields.Char(string=_('Password'), )
    is_api_test = fields.Boolean(string=_('API Test'), )

    def set_values(self):
        res = super(YobelSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('xmpe_api_yobelscm.company',
                                                  self.company)
        self.env['ir.config_parameter'].set_param('xmpe_api_yobelscm.username',
                                                  self.username)
        self.env['ir.config_parameter'].set_param('xmpe_api_yobelscm.passwd',
                                                  self.passwd)
        self.env['ir.config_parameter'].set_param(
            'xmpe_api_yobelscm.is_api_test', self.is_api_test)
        return res

    @api.model
    def get_values(self):
        res = super(YobelSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        company = ICPSudo.get_param('xmpe_api_yobelscm.company')
        username = ICPSudo.get_param('xmpe_api_yobelscm.username')
        passwd = ICPSudo.get_param('xmpe_api_yobelscm.passwd')
        is_api_test = ICPSudo.get_param('xmpe_api_yobelscm.is_api_test')
        res.update(
            is_api_test=is_api_test,
            company=company,
            username=username,
            passwd=passwd,
        )
        return res
