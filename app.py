import __future__

from flask import Flask, Response, redirect, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from typing import NewType

from wiki.articles import WikiArticleParser


HTML_TEMPLATE = NewType('HTML_TEMPLATE', 'str')
ERROR_CODE = NewType('ERROR_CODE', 'int')

app = Flask(__name__) 
bootstrap = Bootstrap(app)
moment = Moment(app)

parser = WikiArticleParser()
article_title, article_text = parser.get_content()

@app.route('/')
def index() -> HTML_TEMPLATE:
    return render_template('index_test.html', title=article_title, content=article_text)

@app.route('/user/<name>')
def user(name: str) -> HTML_TEMPLATE:
    return render_template('user.html', name=name, content=f'{article_title}\n{article_text}')

@app.route('/settings')
def settings() -> HTML_TEMPLATE:
    return '<h1>Settings page<h1>'

@app.route('/redirect')
def zen_of_python() -> "Response":
    return redirect('https://peps.python.org/pep-0020/#the-zen-of-python')

@app.errorhandler(404)
def page_not_found(e: Exception) -> tuple[HTML_TEMPLATE, ERROR_CODE]:
    """Handler for Error 404.
    
    
    """    
    
    return render_template('404.html'), 400

@app.errorhandler(500)
def internal_server_error(e: Exception) -> tuple[HTML_TEMPLATE, ERROR_CODE]:
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)