import json
import logging

import requests
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, _

_logger = logging.getLogger(__name__)

headers = {'Content-type': 'application/json'}

url_test = 'http://yscmserver-test.yobelscm.biz:1973/TI_Logistics/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearCliente'
url = 'http://yscmserver-04.yobelscm.biz:1973/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearCliente'
data_test = {
    "Seguridad": {
        "compania": "PLT",
        "usuario": "PEPLTUSR01",
        "password": "Y0b3lPrb01"
    },
    "Mensaje": {
        "Head": {
            "id_mensaje": "PRB20190328001",
            "sistema_origen": "SAP",
            "fecha_origen": "2018-12-08T16:03:00",
            "tipo": "RECCLIEN"
        },
        "Body": {
            "Clientes": [
                {
                    "CLICIA": "IRX",
                    "CLIFPR": "2018-12-08",
                    "CLICCL": "PRBIRXCLI1001",
                    "CLINBR": "CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA",
                    "CLIDIR": "DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA",
                    "CLIUBG": "0123456789",
                    "CLINBRF": "RAZON SOCIAL FISCAL-RAZON SOCIAL FISCAL-RAZON SOCIAL FISCAL-",
                    "CLIDIRF": "DIRECCION FISCAL-DIRECCION FISCAL-DIRECCION FISCAL",
                    "CLIUBF": "0123456789",
                    "CLIRUC": "123456789012345",
                    "CLIREF": "REFERENCIA DIRECCION ENTREGA-REFERENCIA DIRECCION ENTREGA-REFERENCIA DIRECCION ENTREGA-REFERENCIA DI",
                    "CLIDNI": "DNI456789012345",
                    "CLITLF": "12345678901234567890",
                    "CLICEL": "ksilva1@yobelscm.biz",
                    "CLIDIS": "BARRANCA",
                    "CLIPRV": "BARRANCA",
                    "CLIDEP": "LIMA",
                    "CLILAT": "0.345678901234567890123456789012345678901234567890",
                    "CLILON": "0.55599901234567890123456789012345678901234567890"
                },
                {
                    "CLICIA": "IRX",
                    "CLIFPR": "2018-12-08",
                    "CLICCL": "PRBIRXCLI002",
                    "CLINBR": "CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA CLIENTE PRUEBA",
                    "CLIDIR": "DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA DIRECCCION ENTREGA DE MERCADERÍA",
                    "CLIUBG": "0123456789",
                    "CLINBRF": "RAZON SOCIAL FISCAL-RAZON SOCIAL FISCAL-RAZON SOCIAL FISCAL-",
                    "CLIDIRF": "DIRECCION FISCAL-DIRECCION FISCAL-DIRECCION FISCAL",
                    "CLIUBF": "0123456789",
                    "CLIRUC": "123456789012345",
                    "CLIREF": "REFERENCIA DIRECCION ENTREGA-REFERENCIA DIRECCION ENTREGA-REFERENCIA DIRECCION ENTREGA-REFERENCIA DI",
                    "CLIDNI": "DNI456789012345",
                    "CLITLF": "12345678901234567890",
                    "CLICEL": "ksilva1@yobelscm.biz",
                    "CLIDIS": "BARRANCA",
                    "CLIPRV": "BARRANCA",
                    "CLIDEP": "LIMA",
                    "CLILAT": "0.345678901234567890123456789012345678901234567890",
                    "CLILON": "0.55599901234567890123456789012345678901234567890"
                }
            ]
        }
    }
}


class Partner(models.Model):
    _inherit = 'res.partner'

    yobel_sync = fields.Boolean(string=_('Yobel Synchronization'),
                                default=False)

    sync = fields.Boolean(string=_('Synchronization'), default=False)

    delivery_address_reference = fields.Char(
        string=_('Merchandise delivery address reference'),
        related='street', )

    notify_message = fields.Char(string=_('Notify Message'), )

    origin_date = fields.Datetime(string=_('Origin Date'),
                                  default=fields.Datetime.now)

    id_mensaje = fields.Char(string=_('Mensaje ID'), copy=False, readonly=True,
                            index=True, default=lambda self: _('New'))

    def fill_security(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        return {
            "compania": ICPSudo.get_param('xmpe_api_yobelscm.company'),
            "usuario": ICPSudo.get_param('xmpe_api_yobelscm.username'),
            "password": ICPSudo.get_param('xmpe_api_yobelscm.passwd')
        }

    def fill_message(self):
        shipment_list = []

        for rec in self:
            shipment_list.append({
                "CLICIA": rec.company_id.yobel_identifier or rec.env.company.yobel_identifier,
                "CLIFPR": self.origin_date.date().strftime(DEFAULT_SERVER_DATE_FORMAT),
                "CLICCL": rec.vat,
                "CLINBR": rec.name,
                "CLIDIR": f'{rec.street}, {rec.city}',
                "CLIUBG": int('0123456789'),
                "CLINBRF": rec.name,
                "CLIDIRF": f'{rec.street}, {rec.city}',
                "CLIUBF": rec.street,
                "CLIRUC": rec.vat,
                "CLIREF": rec.delivery_address_reference,
                "CLIDNI": rec.vat,
                "CLITLF": rec.phone,
                "CLICEL": rec.email,
                "CLIDIS": rec.l10n_pe_district.name,
                "CLIPRV": rec.city,
                "CLIDEP": rec.state_id.name,
                "CLILAT": rec.partner_latitude,
                "CLILON": rec.partner_longitude,
            })
            # detail_list.clear()
        return {
            "Head": {
                "id_mensaje": "PRB20190328001",
                "sistema_origen": "SAP",
                "fecha_origen": self.origin_date.date().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                "tipo": "RECCLIEN"
            },
            "Body": {
                "Clientes": shipment_list
            }
        }


    def send_yobel_data(self, url, data):
        try:
            data_json = json.dumps(data)
            req = requests.post(url, data=data_json, headers=headers)
            content = req.json()
        except IOError:
            _logger.error("Error in sending data to Yobel SCM")
            error_msg = "Something went wrong during data submission"
            return UserError(error_msg)
        _logger.info(content)
        return content

    def send_yobel_customer_data(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        data = {
            "Seguridad": self.fill_security(),
            "Mensaje": self.fill_message()
        }
        is_api_test = ICPSudo.get_param('xmpe_api_yobelscm.is_api_test')
        if is_api_test:
            _logger.info("Yobel Customer Data Test: %s", data_test)
            req = self.send_yobel_data(url_test, data_test)
        else:
            _logger.info("Yobel Customer Data: %s", data)
            req = self.send_yobel_data(url_test, data)
            # self.write({'state': 'sent'})
        if req['CrearClienteResult']['resultado'] == 'OK':
            self.write({'yobel_sync': False})
            self.notify_message = 'Cliente enviado a Yobel SCM exitosamente'
        else:
            message = []
            for error in req['CrearClienteResult']['errores']:
                message.append(error['descripcion'])
            self.notify_message = "\n ".join(message)
