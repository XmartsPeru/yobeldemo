import json
import logging

import requests
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo import fields, models, api, _

headers = {'Content-type': 'application/json'}

_logger = logging.getLogger(__name__)

url_test = 'http://yscmserver-test.yobelscm.biz:1973/TI_Logistics/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearProductoHJ'
url = 'http://yscmserver-04.yobelscm.biz:1973/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearProductoHJ'
data_test = {
    "Seguridad": {
        "compania": "LIB",
        "usuario": "PELIBUSR01",
        "password": "Y0bLibPrb01"
    },
    "Mensaje": {
        "Head": {
            "id_mensaje": "PRB20190327001",
            "sistema_origen": "SAP",
            "fecha_origen": "2018-12-07T14:00:00",
            "tipo": "RECPRODU"
        },
        "Body": {
            "Productos": [
                {
                    "PRDCIA": "LIB",
                    "PRDPRO": "PRODLIB1001",
                    "PRDDES": "PRODUCTO PRB",
                    "PRDFAM": "FAMILIA",
                    "PRDSFM": "SUBFAMILIA",
                    "PRDCB1": "CODIGOBARRA1",
                    "PRDUM1": "UND",
                    "PRDUX1": "1234567",
                    "PRDLR1": "12345.55",
                    "PRDAN1": "12345.22",
                    "PRDAL1": "12345.44",
                    "PRDPE1": "1234567.33",
                    "PRDVO1": "12345.999",
                    "PRDCB2": "CODIGOBARRA2",
                    "PRDUM2": "CAJ",
                    "PRDUX2": "24",
                    "PRDLR2": "",
                    "PRDAN2": "12.00",
                    "PRDAL2": "2.00",
                    "PRDPE2": "50.00",
                    "PRDVO2": "312.000",
                    "PRDFML": "1",
                    "PRDCSX": "SKUPRODUCTO1",
                    "PRDSER": "0"
                },
                {
                    "PRDCIA": "LIB",
                    "PRDPRO": "PRODLIB1002",
                    "PRDDES": "PRODUCTO PRB-PRODUCTO PRB-PRODUCTO PRB-PRODUCTO PRB",
                    "PRDFAM": "FAMILIA",
                    "PRDSFM": "SUBFAMILIA",
                    "PRDCB1": "CODIGOBARRA1",
                    "PRDUM1": "UND",
                    "PRDUX1": "7",
                    "PRDLR1": "13.00",
                    "PRDAN1": "12.00",
                    "PRDAL1": "2.00",
                    "PRDPE1": "50.00",
                    "PRDVO1": "312.000",
                    "PRDCB2": "CODIGOBARRA2",
                    "PRDUM2": "CAJ",
                    "PRDUX2": "7",
                    "PRDLR2": "13.00",
                    "PRDAN2": "12.00",
                    "PRDAL2": "2.00",
                    "PRDPE2": "50.00",
                    "PRDVO2": "312.000",
                    "PRDFML": "1",
                    "PRDCSX": "SKUPRODUCTO2",
                    "PRDSER": "0"
                }
            ]
        }
    }
}


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    yobel_sync = fields.Boolean(string=_('Yobel Synchronization'),
                                default=False)

    sync = fields.Boolean(string=_('Synchronization'), default=False)

    origin_date = fields.Datetime(string=_('Origin Date'),
                                  default=fields.Datetime.now)

    units_per_package = fields.Integer(string=_('Units per package 1'), )

    length = fields.Float(string=_('Length'), )

    high = fields.Float(string=_('High'), )

    width = fields.Float(string=_('Width'), )

    batch_flag = fields.Integer(string=_('Batch Flag'), )

    supplier_sku_code = fields.Char(string=_('Supplier SKU Code'), )

    serial_control_flag = fields.Integer(string=_('Serial Control Flag'), )

    notify_message = fields.Char(string=_('Notify Message'), )

    id_mensaje = fields.Char(string=_('Mensaje ID'), copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))

    # Calcula el volumen del producto
    @api.depends('product_variant_ids', 'product_variant_ids.volume',
                 'length', 'high', 'width')
    def _compute_volume(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.volume = template.length * template.high * template.width
        return super(ProductTemplate, self - unique_variants)._compute_volume()

    def fill_message(self):
        product_list = []
        if self.yobel_sync:
            for rec in self:
                product_list.append({
                    "PRDCIA": self.env.company.yobel_identifier,
                    "PRDPRO": rec.default_code,
                    "PRDDES": rec.name,
                    "PRDFAM": rec.categ_id.name[:10],
                    "PRDSFM": rec.categ_id.name[:10],
                    "PRDCB1": rec.barcode,
                    "PRDUM1": rec.uom_id.name,
                    "PRDUX1": rec.units_per_package,
                    "PRDLR1": rec.length,
                    "PRDAN1": rec.width,
                    "PRDAL1": rec.high,
                    "PRDPE1": rec.weight,
                    "PRDVO1": rec.volume,
                    "PRDCB2": "CODIGOBARRA2",
                    "PRDUM2": "CAJ",
                    "PRDUX2": "24",
                    "PRDLR2": "",
                    "PRDAN2": "12.00",
                    "PRDAL2": "2.00",
                    "PRDPE2": "50.00",
                    "PRDVO2": "312.000",
                    "PRDFML": rec.batch_flag,
                    "PRDCSX": rec.supplier_sku_code,
                    "PRDSER": rec.serial_control_flag,
                })
        return {
            "Head": {
                "id_mensaje": self.id_mensaje,
                "sistema_origen": "SAP",
                "fecha_origen": self.origin_date.date().strftime(
                    DEFAULT_SERVER_DATE_FORMAT),
                "tipo": "RECPRODU"
            },
            "Body": {
                "Productos": product_list
            }
        }

    def fill_security(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        return {
            "compania": ICPSudo.get_param('xmpe_api_yobelscm.company'),
            "usuario": ICPSudo.get_param('xmpe_api_yobelscm.username'),
            "password": ICPSudo.get_param('xmpe_api_yobelscm.passwd')
        }

    def send_yobel_data(self, url_target, data):
        try:
            data_json = json.dumps(data)
            _logger.info(json.dumps(data, indent=4))
            req = requests.post(url=url_target, data=data_json, headers=headers)
            content = req.json()
        except IOError:
            _logger.error("Error in sending data to Yobel SCM")
            error_msg = "Something went wrong during data submission"
            return UserError(error_msg)
        _logger.info(content)
        return content

    def send_yobel_product_data(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        data = {
            "Seguridad": self.fill_security(),
            "Mensaje": self.fill_message()
        }
        is_api_test = ICPSudo.get_param('xmpe_api_yobelscm.is_api_test')
        _logger.info("Yobel Product Data: %s", data)
        req = self.send_yobel_data(url_test, data)
        if is_api_test:
            _logger.info("Yobel Product Data Test: %s", data_test)
            req = self.send_yobel_data(url_test, data_test)

        if req['CrearProductoHJResult']['resultado'] == 'OK':
            self.write({
                'yobel_sync': False,
                'notify_message': 'Producto enviado a Yobel SCM exitosamente',
                'id_mensaje': self.env['ir.sequence'].next_by_code(
                    'yobel_master_prb')
            })
        else:
            message = []
            for error in req['CrearProductoHJResult']['errores']:
                message.append(error['descripcion'])
            self.write({'notify_message': f'\n '.join(message)})


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def send_yobel_product_data(self):
        return self.product_tmpl_id.send_yobel_product_data()
