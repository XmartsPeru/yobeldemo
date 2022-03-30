# -*- coding: utf-8 -*-
import json
import logging

from odoo.tools import date_utils
from . import controllers
from . import models

from odoo.http import JsonRequest, Response


class JsonRequestPatch(JsonRequest):

    def _json_response(self, result=None, error=None):
        response = {}
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


JsonRequest._json_response = JsonRequestPatch._json_response
