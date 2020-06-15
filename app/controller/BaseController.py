import time
import json
from os import environ
from flask import render_template, request, abort


class BaseController():

    def render(self, template_name, **kwargs):
        template_name = '{}.html'.format(template_name)
        kwargs['app_domain'] = environ.get('DOMAIN', '/')
        kwargs['footer_year'] = time.strftime('%Y', time.localtime())
        return render_template(template_name, **kwargs)

    def asJson(self, data, error=0, message='ok'):
        return json.dumps({
            'error': error,
            'message': message,
            'data': data
        })

    def getValue(self, key, default=None):
        if key in request.args:
            return request.args[key]
        elif key in request.form:
            return request.form[key]
        else:
            return default

    def error(self, code=404):
        return abort(code)
