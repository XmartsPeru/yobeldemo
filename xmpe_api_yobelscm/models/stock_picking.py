import json
import logging
from datetime import datetime

import requests
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, _

_logger = logging.getLogger(__name__)

headers = {'Content-type': 'application/json'}

url_yobel = {
    'order_test': 'http://yscmserver-test.yobelscm.biz:1973/TI_Logistics'
                  '/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearPedido',
    'order_prod': 'http://yscmserver-04.yobelscm.biz:1973/WSYOB_RECEP_LOG'
                  '/WSYOB_RECEP/CrearPedido',
    'shipment_test': 'http://yscmserver-test.yobelscm.biz:1973/TI_Logistics'
                     '/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearEmbarque',
    'shipment_prod': 'http://yscmserver-04.yobelscm.biz:1973/WSYOB_RECEP_LOG/WSYOB_RECEP/CrearEmbarque'
}
order_test = {
    "Seguridad": {
        "compania": "LIB",
        "usuario": "PELIBUSR01",
        "password": "Y0bLibPrb01"
    },
    "Mensaje": {
        "Head": {
            "id_mensaje": "PRB20181214002",
            "sistema_origen": "SAP",
            "fecha_origen": "2018-12-14T18:00:00",
            "tipo": "RECPED"
        },
        "Body": {
            "Pedidos": [
                {
                    "PEDCIA": "IRX",
                    "PEDFPR": "2018-12-14",
                    "PEDCTR": "P1",
                    "PEDNRO": "PEDIRX101",
                    "PEDCCL": "CLIIRX01",
                    "PEDFCH": "2018-12-14",
                    "PEDTIT": "2",
                    "PEDTUN": "30",
                    "PEDFEI": "",
                    "PEDHOI": "",
                    "PEDFEF": "",
                    "PEDHOF": "",
                    "PEDNOC": "",
                    "PEDTDA": "",
                    "PEDA01": "",
                    "PEDN01": "",
                    "PEDF01": "",
                    "Detalles": [
                        {
                            "PEDAUX": "1",
                            "PEDCPR": "PRODIRX01",
                            "PEDLOT": "",
                            "PEDCTD": "10",
                            "PEDALM": "",
                            "PEDSKU": "",
                            "PEDUXE": "",
                            "PEDA02": "",
                            "PEDN02": "",
                            "PEDF02": ""
                        },
                        {
                            "PEDAUX": "2",
                            "PEDCPR": "PRODIRX02",
                            "PEDLOT": "",
                            "PEDCTD": "20",
                            "PEDALM": "",
                            "PEDSKU": "",
                            "PEDUXE": "",
                            "PEDA02": "",
                            "PEDN02": "",
                            "PEDF02": ""
                        }
                    ]
                },
                {
                    "PEDCIA": "IRX",
                    "PEDFPR": "2018-12-14",
                    "PEDCTR": "P1",
                    "PEDNRO": "PEDIRX102",
                    "PEDCCL": "CLIIRX02",
                    "PEDFCH": "2018-12-14",
                    "PEDTIT": "1",
                    "PEDTUN": "20",
                    "PEDFEI": "",
                    "PEDHOI": "",
                    "PEDFEF": "",
                    "PEDHOF": "",
                    "PEDNOC": "",
                    "PEDTDA": "",
                    "PEDA01": "",
                    "PEDN01": "",
                    "PEDF01": "",
                    "Detalles": [
                        {
                            "PEDAUX": "1",
                            "PEDCPR": "PRODIRX03",
                            "PEDLOT": "",
                            "PEDCTD": "20",
                            "PEDALM": "",
                            "PEDSKU": "",
                            "PEDUXE": "",
                            "PEDA02": "",
                            "PEDN02": "",
                            "PEDF02": ""
                        },
                    ]
                }
            ]
        }
    }
}

data_test = {
    "Seguridad": {
        "compania": "PLT",
        "usuario": "PEPLTUSR01",
        "password": "Y0b3lPrb01"
    },
    "Mensaje": {
        "Head": {
            "id_mensaje": "EMB-PRB-001",
            "sistema_origen": "SAP",
            "fecha_origen": "2018-12-14T14:00:00",
            "tipo": "RECEMB"
        },
        "Body": {
            "Embarques": [
                {
                    "EMBCIA": "IRX",
                    "EMBNRO": "IRXEMBPRB001",
                    "EMBFA1": "2018-12-14",
                    "EMBOCP": "OC0001",
                    "EMBPRV1": "PRV0001",
                    "EMBPOR": "CR",
                    "EMBNCT": "0001",
                    "EMBA01": "",
                    "EMBN01": "",
                    "Detalles": [
                        {
                            "EMBLIN": "1",
                            "EMBPRO": "PRD001",
                            "EMBQTY": "1",
                            "EMBUMC": "UN",
                            "EMBLOT": "",
                            "EMBFVE": "20201231",
                            "EMBALX": "",
                            "EMBA02": "",
                            "EMBN02": ""
                        },
                        {
                            "EMBLIN": "2",
                            "EMBPRO": "PRD002",
                            "EMBQTY": "1",
                            "EMBUMC": "UN",
                            "EMBLOT": "",
                            "EMBFVE": "",
                            "EMBALX": "",
                            "EMBA02": "",
                            "EMBN02": ""
                        }
                    ]
                },
                {
                    "EMBCIA": "IRX",
                    "EMBNRO": "IRXEMBPRB002",
                    "EMBFA1": "2018-12-14",
                    "EMBOCP": "OC0002",
                    "EMBPRV1": "PRV0002",
                    "EMBPOR": "CR",
                    "EMBNCT": "0002",
                    "EMBA01": "",
                    "EMBN01": "",
                    "Detalles": [
                        {
                            "EMBLIN": "1",
                            "EMBPRO": "PRD001",
                            "EMBQTY": "1",
                            "EMBUMC": "UN",
                            "EMBLOT": "",
                            "EMBFVE": "20201231",
                            "EMBALX": "",
                            "EMBA02": "",
                            "EMBN02": ""
                        },
                        {
                            "EMBLIN": "2",
                            "EMBPRO": "PRD002",
                            "EMBQTY": "1",
                            "EMBUMC": "UN",
                            "EMBLOT": "",
                            "EMBFVE": "",
                            "EMBALX": "",
                            "EMBA02": "",
                            "EMBN02": ""
                        }
                    ]
                }
            ]
        }
    }
}

YOBEL_STATE = [
    ('sent', _('Sent')),
    ('rejected', _('Rejected')),
    ('accepted', _('Accepted')),
    ('confirmed', _('Confirmed')),
    ('lost', _('Lost')),
]


class Picking(models.Model):
    _inherit = 'stock.picking'

    yobel_sync = fields.Boolean(string=_('Yobel Synchronization'),
                                default=False)
    sync = fields.Boolean(string=_('Synchronization'), default=False)
    notify_message = fields.Char(string=_('Notify Message'), )
    container_number = fields.Char(string=_('Container number'),
                                   required=False, )
    store = fields.Char(string=_('Store'), )
    flag_1 = fields.Char(string=_('Flag 1'), )
    additional_1 = fields.Char(string=_('Additional 1'), )
    numeric_1 = fields.Integer(string=_('Numeric 1'), )
    origin_date = fields.Datetime(string=_('Origin Date'),
                                  default=fields.Datetime.now, )
    yobel_state = fields.Selection(string=_('Yobel State'),
                                   selection=YOBEL_STATE, default='',
                                   readonly=True)

    id_mensaje_out = fields.Char(string=_('Mensaje ID'), copy=False,
                               readonly=True,
                             index=True, default=lambda self: _('New'))

    id_mensaje_in = fields.Char(string=_('Mensaje ID'), copy=False,
                                 readonly=True,
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
            detail_list = []
            for detail in rec.move_ids_without_package:
                detail_list.append({
                    "EMBLIN": detail.id,
                    "EMBPRO": detail.product_id.default_code,
                    "EMBQTY": int(detail.product_uom_qty),
                    "EMBUMC": detail.product_uom.name,
                    "EMBLOT": detail.product_id.name,
                    "EMBFVE": detail.date.strftime('%Y%m%d'),
                    "EMBALX": "",
                    "EMBA02": "",
                    "EMBN02": ""
                })
            shipment_list.append({
                "EMBCIA": self.env.company.yobel_identifier,
                "EMBNRO": rec.name,
                "EMBFA1": rec.scheduled_date.strftime(DEFAULT_SERVER_DATE_FORMAT),
                "EMBOCP": rec.name[:6],
                "EMBPRV1": rec.company_id.name,
                "EMBPOR": rec.company_id.state_id.code,
                "EMBNCT": "0001",
                "EMBA01": "",
                "EMBN01": "",
                "Detalles": detail_list,
            })
            # detail_list.clear()
        return {
            "Head": {
                "id_mensaje": self.id_mensaje_in,
                "sistema_origen": "SAP",
                "fecha_origen": fields.Datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT),
                "tipo": "RECEMB"
            },
            "Body": {
                "Embarques": shipment_list
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

    def send_yobel_shipment_data(self):
        if self.picking_type_code != 'outgoing':
            ICPSudo = self.env['ir.config_parameter'].sudo()
            data = {
                "Seguridad": self.fill_security(),
                "Mensaje": self.fill_message()
            }
            is_api_test = ICPSudo.get_param('xmpe_api_yobelscm.is_api_test')
            if is_api_test:
                _logger.info("Yobel Shipment Data Test: %s", data_test)
                req = self.send_yobel_data(url_yobel['shipment_test'],
                                           data_test)
            else:
                _logger.info("Yobel Shipment Data: %s", data)
                req = self.send_yobel_data(url_yobel['shipment_test'], data)
                # self.write({'state': 'sent'})
            if req['CrearEmbarqueResult']['resultado'] == 'OK':
                self.write({
                    'yobel_sync': False,
                    'yobel_state': 'sent',
                    'id_mensaje_in': self.env['ir.sequence'].next_by_code(
                        'yobel_master_emb')
                })
                self.notify_message = 'Embarque enviado a Yobel SCM exitosamente'
            else:
                message = []
                for error in req['CrearEmbarqueResult']['errores']:
                    message.append(error['descripcion'])
                self.notify_message = "\n ".join(message)
                self.write({'yobel_state': 'rejected'})

    def fill_order_message(self):
        order_list = []
        for rec in self:
            detail_list = []
            for detail in rec.move_ids_without_package:
                detail_list.append({
                    "PEDAUX": detail.id,
                    "PEDCPR": detail.product_id.default_code,
                    "PEDLOT": 'lote',
                    "PEDCTD": int(detail.quantity_done),
                    "PEDALM": detail.product_id.warehouse_id.name or '',
                    "PEDSKU": detail.product_id.supplier_sku_code,
                    "PEDUXE": detail.max_unit_per_package_picking or '',
                    "PEDA02": detail.additional_2 or '',
                    "PEDN02": detail.numeric_2,
                    "PEDF02": detail.flag_2 or '',
                })
            order_list.append({
                "PEDCIA": self.env.company.yobel_identifier,
                "PEDFPR": rec.scheduled_date.strftime(DEFAULT_SERVER_DATE_FORMAT),
                "PEDCTR": 'P1',
                "PEDNRO": rec.name,
                "PEDCCL": rec.name,
                "PEDFCH": rec.origin_date.strftime(DEFAULT_SERVER_DATE_FORMAT),
                "PEDTIT": len(detail_list),
                "PEDTUN": sum([d['PEDCTD'] for d in detail_list]),
                "PEDFEI": rec.scheduled_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)[:10],
                "PEDHOI": rec.scheduled_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)[11:],
                "PEDFEF": rec.scheduled_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)[:10],
                "PEDHOF": rec.scheduled_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)[11:],
                "PEDNOC": '',
                "PEDTDA": rec.store or '',
                "PEDA01": rec.additional_1 or '',
                "PEDN01": rec.numeric_1,
                "PEDF01": rec.flag_1 or '',
                "Detalles": detail_list,
            })
            # detail_list.clear()
        return {
            "Head": {
                "id_mensaje": self.id_mensaje_out,
                "sistema_origen": "SAP",
                "fecha_origen": self.origin_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT),
                "tipo": "RECEMB"
            },
            "Body": {
                "Pedidos": order_list
            }
        }

    def send_yobel_order_data(self):
        if self.picking_type_code == 'outgoing':
            ICPSudo = self.env['ir.config_parameter'].sudo()
            data = {
                "Seguridad": self.fill_security(),
                "Mensaje": self.fill_order_message()
            }
            is_api_test = ICPSudo.get_param('xmpe_api_yobelscm.is_api_test')
            if is_api_test:
                _logger.info("Yobel Order Data Test: %s", order_test)
                req = self.send_yobel_data(url_yobel['order_test'], order_test)
            else:
                _logger.info("Yobel Order Data: %s", data)
                req = self.send_yobel_data(url_yobel['order_test'], data)
                # self.write({'state': 'sent'})
            if req['CrearPedidoResult']['resultado'] == 'OK':
                self.write({
                    'yobel_sync': False,
                    'yobel_state': 'sent',
                    'id_mensaje_out': self.env['ir.sequence'].next_by_code(
                        'yobel_master_prb')
                })
                self.notify_message = 'Embarque enviado a Yobel SCM exitosamente'
            else:
                message = []
                for error in req['CrearPedidoResult']['errores']:
                    message.append(error['descripcion'])
                self.notify_message = "\n ".join(message)
                self.write({'yobel_state': 'rejected'})


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Only IN
    yobel_customer_warehouse = fields.Char(
        string=_('yobel Customer Warehouse'), )
    # ALL
    additional_2 = fields.Char(string=_('Additional 2'), )
    numeric_2 = fields.Integer(string=_('Numeric 2'), )
    # Only OUT
    flag_2 = fields.Integer(string=_('Flag 2'), )
    max_unit_per_package_picking = fields.Integer(
        string=_('Maximum units per package for Picking'), )
