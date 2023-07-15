#!.\venv\Scripts\python.exe
from __future__ import annotations

__version__ = '0.1'
__author__ = 'Bartlomiej Jargut'

from pydactle.articles import WikiArticleParser
from pydactle.titles import ALL_TITLES
from flask import Flask, Response, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import random

app = Flask(__name__) 
bootstrap = Bootstrap(app)
moment = Moment(app)

parser = WikiArticleParser()
article_title: str = random.choice(ALL_TITLES)
article_text = parser.get_article_text(article_title, print_content=True)


@app.route('/')
def index() -> str:
    return render_template('index.html', title=article_title, content=article_text)


@app.route('/', methods=['POST'])
def get_guess() -> str:
    text = request.form['text']
    return text

@app.route('/user/<name>')
def user(name: str) -> str:
    return render_template('user.html', name=name, content=f'{article_title}\n{article_text}')

@app.route('/settings')
def settings() -> str:
    return '<h1>Settings page<h1>'

@app.route('/redirect')
def zen_of_python():
    return redirect('https://peps.python.org/pep-0020/#the-zen-of-python')

@app.errorhandler(404)
def page_not_found(e: Exception) -> tuple[str, int]:
    """Handler for Error 404.
    """    
    return render_template('404.html'), 400

@app.errorhandler(500)
def internal_server_error(e: Exception) -> tuple[str, int]:
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
