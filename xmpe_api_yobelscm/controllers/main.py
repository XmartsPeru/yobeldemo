import logging
import json

from odoo import http, fields
_logger = logging.getLogger(__name__)


class XmpeApiYobelscm(http.Controller):
    @http.route('/web/conf_shipment', auth='none', type="json",
                methods=['POST'],
                csrf=False, cors='*')
    def conf_shipment(self, **kw):
        data = json.loads(http.request.httprequest.data)
        ICPSudo = http.request.env['ir.config_parameter'].sudo()
        company = ICPSudo.get_param('xmpe_api_yobelscm.company')
        username = ICPSudo.get_param('xmpe_api_yobelscm.username')
        passwd = ICPSudo.get_param('xmpe_api_yobelscm.passwd')
        picking_model = http.request.env['stock.picking'].sudo().search([('picking_type_code', '!=', 'outgoing')])
        details = []
        for d in data['Mensaje']['Body']['ConfEmbarque']['Detalles']:
            details.append({
                'correlative': d['CEMLIN'],
                'product_code': d['CEMCPR'],
                'qty': d['CEMQTY'],
                'uom': d['CEMUMC'],
                'lot': d['CEMLOT'],
                'lot_creation_date': d['CEMFFA'],
                'lot_expiration_date': d['CEMFVE'],
                'homologous_customer': d['CEMALX'],
                'additional_1': d['CEMA01'],
                'numeric_1': d['CEMN01'],
            })
        _logger.info(details)
        if data['Seguridad']['compania'] != company or data['Seguridad'][
            'usuario'] != username or data['Seguridad']['password'] != passwd \
                or data['Mensaje']['Head']['tipo'] != 'CONFEMB' or not details:
            for pick in picking_model.filtered(lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfEmbarque']['CEMEMB']:
                    pick.yobel_state = 'lost'
            res = data.get('result', 'ERROR')
        else:
            for pick in picking_model.filtered(lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfEmbarque']['CEMEMB']:
                    pick.yobel_state = 'confirmed'
            res = data.get('result', 'OK')
        return res

    @http.route('/web/conf_order', auth='none', type="json",
                methods=['POST'],
                csrf=False, cors='*')
    def conf_order(self, **kw):
        data = json.loads(http.request.httprequest.data)
        ICPSudo = http.request.env['ir.config_parameter'].sudo()
        company = ICPSudo.get_param('xmpe_api_yobelscm.company')
        username = ICPSudo.get_param('xmpe_api_yobelscm.username')
        passwd = ICPSudo.get_param('xmpe_api_yobelscm.passwd')
        picking_model = http.request.env['stock.picking'].sudo().search([('picking_type_code', '=', 'outgoing')])
        details = []
        for d in data['Mensaje']['Body']['ConfPedido']['Detalles']:
            details.append((0, 0, {
                'correlative': d['CPINUL'],
                'product_code': d['CPICPR'],
                'lot': d['CPILOT'],
                'qty_picking': d['CPICTP'],
                'qty': d['CPICTD'],
                'origin_warehouse': d['CPIALM'],
                'additional_1': d['CPIA01'],
                'numeric_1': d['CPIN01'],
            }))
        if data['Seguridad']['compania'] != company or data['Seguridad'][
            'usuario'] != username or data['Seguridad']['password'] != passwd \
                or data['Mensaje']['Head']['tipo'] != 'CONFPED' or not details:
            for pick in picking_model.filtered(lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfPedido']['CPINRO']:
                    pick.yobel_state = 'lost'
            res = data.get('result', 'ERROR')
        else:
            for pick in picking_model.filtered(lambda p: p.yobel_state == 'sent'):
                if pick.name == data['Mensaje']['Body']['ConfPedido']['CPINRO']:
                    pick.yobel_state = 'confirmed'
            res = data.get('result', 'OK')
        return res
