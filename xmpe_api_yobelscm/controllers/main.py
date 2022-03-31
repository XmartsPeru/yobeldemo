import logging
import json

from odoo import http, fields
from odoo.http import JsonRequest, Response

from odoo.tools import date_utils

_logger = logging.getLogger(__name__)


class XmpeApiYobelscm(http.Controller):

    def is_authenticated(self, data):
        ICPSudo = http.request.env['ir.config_parameter'].sudo()
        company = ICPSudo.get_param('xmpe_api_yobelscm.company')
        username = ICPSudo.get_param('xmpe_api_yobelscm.username')
        passwd = ICPSudo.get_param('xmpe_api_yobelscm.passwd')
        if data['Seguridad']['compania'] != company or data['Seguridad'][
            'usuario'] != username or data['Seguridad']['password'] != passwd:
            return False
        return True

    @http.route('/web/ConfEmbarque', auth='none', type="json",
                methods=['POST'],
                csrf=False, cors='*', lover='chun')
    def conf_shipment(self, **kw):
        data = json.loads(http.request.httprequest.data)
        picking_model = http.request.env['stock.picking'].sudo().search(
            [('picking_type_code', '!=', 'outgoing')])
        details = []
        for detail in data['Mensaje']['Body']['ConfEmbarque']['Detalles']:
            details.append({
                'correlative': detail['CEMLIN'],
                'product_code': detail['CEMCPR'],
                'qty': detail['CEMQTY'],
                'uom': detail['CEMUMC'],
                'lot': detail['CEMLOT'],
                'lot_creation_date': detail['CEMFFA'],
                'lot_expiration_date': detail['CEMFVE'],
                'homologous_customer': detail['CEMALX'],
                'additional_1': detail['CEMA01'],
                'numeric_1': detail['CEMN01'],
            })
        _logger.info(details)
        if not self.is_authenticated(data) or not details:
            for pick in picking_model.filtered(
                    lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfEmbarque'][
                    'CEMEMB']:
                    pick.yobel_state = 'lost'
            res = {
                'RetornoInsertResult': {
                    'resultado': '0',
                    'mensaje': 'ERROR'
                }
            }
        else:
            for pick in picking_model.filtered(
                    lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfEmbarque'][
                    'CEMEMB']:
                    pick.yobel_state = 'confirmed'
            res = {
                'RetornoInsertResult': {
                    'resultado': '1',
                    'mensaje': 'OK'
                }
            }
        return res

    @http.route('/web/ConfPedido', auth='none', type="json",
                methods=['POST'],
                csrf=False, cors='*', lover='chun')
    def conf_order(self, **kw):
        data = json.loads(http.request.httprequest.data)
        _logger.info(data)
        picking_model = http.request.env['stock.picking'].sudo().search(
            [('picking_type_code', '=', 'outgoing')])
        details = []
        for detail in data['Mensaje']['Body']['ConfPedido']['Detalles']:
            details.append((0, 0, {
                'correlative': detail['CPINUL'],
                'product_code': detail['CPICPR'],
                'lot': detail['CPILOT'],
                'qty_picking': detail['CPICTP'],
                'qty': detail['CPICTD'],
                'origin_warehouse': detail['CPIALM'],
                'additional_1': detail['CPIA01'],
                'numeric_1': detail['CPIN01'],
            }))
        if not self.is_authenticated(data) or not details:
            for pick in picking_model.filtered(
                    lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfPedido']['CPINRO']:
                    pick.yobel_state = 'lost'
            res = {
                'RetornoInsertResult': {
                    'resultado': '0',
                    'mensaje': 'ERROR'
                }
            }
        else:
            for pick in picking_model.filtered(
                    lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfPedido']['CPINRO']:
                    pick.yobel_state = 'confirmed'
            res = {
                'RetornoInsertResult': {
                    'resultado': '1',
                    'mensaje': 'OK'
                }
            }
        return res

    @http.route('/web/RetornoError', auth='none', type="json",
                methods=['POST'],
                csrf=False, cors='*', lover='chun')
    def error_messages(self, **kw):
        model_stock_picking = None
        datas = json.loads(http.request.httprequest.data)
        _logger.info(datas)
        domain = [('id_mensaje', '=', datas['Mensaje']['Head']['id_mensaje'])]
        model_product_template = http.request.env[
            'product.template'].sudo().search(domain)
        model_stock_picking = http.request.env['stock.picking'].sudo() \
            .search(['|', ('id_mensaje_in', '=', datas['Mensaje']['Head'][
            'id_mensaje']), ('id_mensaje_out', '=',
                             datas['Mensaje']['Head']['id_mensaje'])])
        model_partner = http.request.env['res.partner'].sudo().search(domain)
        error_message = http.request.env['xmpe.error.msg'].sudo() \
            .search([('code', '=', datas['Mensaje']['Body']['codigo'])],
                    limit=1)

        if model_product_template.ids != 0:
            model_product_template.notify_message = error_message.description

        if model_stock_picking.ids != 0:
            model_stock_picking.notify_message = error_message.description

        if model_partner.ids != 0:
            model_partner.notify_message = error_message.description

        res = {
            'RetornoInsertResult': {
                'resultado': '0',
                'mensaje': 'ERROR'
            }
        }

        if not (
                model_product_template.ids == [] and model_stock_picking.ids == [] and model_partner.ids == []):
            res = {
                'RetornoInsertResult': {
                    'resultado': '1',
                    'mensaje': 'OK'
                }
            }

        return res

    @http.route('/web/RetornoInsert', auth='none', type="json",
                methods=['POST'],
                csrf=False, cors='*', lover='chun')
    def insert_messages(self, **kw):
        datas = json.loads(http.request.httprequest.data)
        _logger.info(datas)
        domain = [('id_mensaje', '=', datas['Mensaje']['Head']['id_mensaje'])]
        model_product_template = http.request.env[
            'product.template'].sudo().search(domain)
        model_stock_picking = http.request.env['stock.picking'].sudo() \
            .search(['|', ('id_mensaje_in', '=', datas['Mensaje']['Head'][
            'id_mensaje']), ('id_mensaje_out', '=',
                             datas['Mensaje']['Head']['id_mensaje'])])
        model_partner = http.request.env['res.partner'].sudo().search(domain)

        res = {
            'RetornoInsertResult': {
                'resultado': '0',
                'mensaje': 'ERROR'
            }
        }

        if not (
                model_product_template.ids == [] and model_stock_picking.ids == [] and model_partner.ids == []):
            res = {
                'RetornoInsertResult': {
                    'resultado': '1',
                    'mensaje': 'OK'
                }
            }

        return res
