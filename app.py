import __future__

__version__ = '0.1'
__author__ = 'Bartlomiej Jargut'

from flask import Flask, Response, redirect, render_template, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import random
from typing import NewType

from wiki.articles import WikiArticleParser
from wiki.titles import Titles


HTML_TEMPLATE = NewType('HTML_TEMPLATE', 'str')
ERROR_CODE = NewType('ERROR_CODE', 'int')

app = Flask(__name__) 
bootstrap = Bootstrap(app)
moment = Moment(app)

parser = WikiArticleParser()
titles_list = Titles.all_titles
article_title = random.choice(titles_list)
article_text = parser.get_article_text(article_title, print_content=True)


@app.route('/')
def index() -> HTML_TEMPLATE:
    return render_template('index.html', title=article_title, content=article_text)

@app.route('/', methods=['POST'])
def get_guess() -> str:
    text = request.form['text']
    return text

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