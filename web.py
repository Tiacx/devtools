import sys
from operator import methodcaller
from flask import Flask, render_template

app = Flask(__name__)

sys.path.append('app/controller')


@app.route('/ddl2<name>/')
def ddl2xxx(name):
    controller = 'DdlController'
    try:
        module = __import__(controller)
        obj = getattr(module, controller)()
        method = 'ddl2' + name
        return methodcaller(method)(obj)
    except Exception:
        return render_template('404.html')


@app.route('/')
@app.route('/<controller>')
@app.route('/<controller>/<method>')
def common(controller='Index', method='index'):
    if controller == 'favicon.ico':
        return 'favicon.ico'

    controller = controller.capitalize() + 'Controller'
    try:
        module = __import__(controller)
        obj = getattr(module, controller)()
        return methodcaller(method)(obj)
    except Exception:
        return render_template('404.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9002, debug=True)
