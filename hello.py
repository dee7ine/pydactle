import __future__

from flask import Flask, request, abort, redirect, render_template
from flask_script import Manager
import numpy as np
from flask_bootstrap import Bootstrap
from flask_moment import Moment


app = Flask(__name__) 
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index() -> str:
    # user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent
    return render_template('base.html')

@app.route('/user/<name>')
def user(name: str) -> str:
    return render_template('user.html', name=name)

@app.route('/settings')
def settings() -> str:
    return '<h1>Settings page<h1>'

@app.route('/redirect')
def zen_of_python() -> str:
    return redirect('https://peps.python.org/pep-0020/#the-zen-of-python')

@app.errorhandler(404)
def page_not_found(e) -> tuple[str, int]:
    return render_template('404.html'), 400

@app.errorhandler(500)
def internal_server_error(e) -> tuple[str, int]:
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)