import os
import sys
from operator import methodcaller
from flask import Flask
from dotenv import load_dotenv

dotenv_path = os.path.normpath(__file__+'./.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

sys.path.append('app/controller')


@app.route('/ddl2<name>/')
def ddl2xxx(name):
    controller = 'DdlController'
    module = __import__(controller)
    obj = getattr(module, controller)()
    method = 'ddl2' + name
    return methodcaller(method)(obj)


@app.route('/')
@app.route('/<controller>')
@app.route('/<controller>/<method>')
def common(controller='Index', method='index'):
    if controller == 'favicon.ico':
        return 'favicon.ico'

    controller = controller.capitalize() + 'Controller'
    module = __import__(controller)
    obj = getattr(module, controller)()
    return methodcaller(method)(obj)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9002, debug=True)
else:
    application = app
