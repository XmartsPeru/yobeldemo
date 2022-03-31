# -*- coding: utf-8 -*-
import json
import logging

from odoo.tools import date_utils
from . import controllers
from . import models

from odoo.http import JsonRequest, Response

def _json_response(self, result=None, error=None):
    lover = self.endpoint.routing.get('lover')
    if lover == 'chun':
        response = {}
        if error is not None:
            response['error'] = error
        if result is not None:
            response = result
    else:
        response = {
            'jsonrpc': '2.0',
            'id': self.jsonrequest.get('id')
        }
        if error is not None:
            response['error'] = error
        if result is not None:
            response['result'] = result

    mime = 'application/json'
    body = json.dumps(response, default=date_utils.json_default)

    return Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Content-Length', len(body))]
    )

setattr(JsonRequest,'_json_response',_json_response) #overwrite the method
