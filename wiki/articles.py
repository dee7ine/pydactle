from __future__ import annotations

__version__ = '0.1'
__author__ = 'Bartlomiej Jargut'

import requests
import wikipedia
from wikipedia.exceptions import (DisambiguationError,
                                  HTTPTimeoutError,
                                  PageError,
                                  RedirectError)
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from functools import wraps
from typing import (TypeVar,
                    Callable,
                    ParamSpec,
                    Concatenate,
                    Any)

from wiki.titles import Titles


article_body = TypeVar('article_body', bound=str)
Param = ParamSpec('Param')
RetType = TypeVar('RetType')
OriginalFunc = Callable[Param, RetType]
DecoratedFunc = Callable[Concatenate[str, Param], RetType]

API_URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnlimit": "5"
}

PROJECT_NAME = 'pydactle'
CURRENT_DIR = Path(__file__)
SOURCE_ROOT = [p for p in CURRENT_DIR.parents if p.parts[-1] == PROJECT_NAME][0]

class Parameters:
    
    COMMON_WORDS: list[str] = ['the', 'at', 'there', 'some', 'my',
                    'of', 'be', 'use', 'her', 'than',
                    'and', 'this','an'	,'would','first',
                    'a'	,'have'	,'each'	,'make'	,'were',
                    'to','from'	,'which','like'	,'been',
                    'in','or', 'do', 'into', 'who', 'how',		
                    'that', 'by', 'if', 'but', 'will', 'not',
                    'up', 'other', 'what', 'more', 'for', 'on',
                    'all', 'about', 'go', 'out', 'as', 'with',
                    'then', 'no', 'may', 'so', 'such', 'despite', 
                    'beneath', 'now', 'during', 'after', 'was', 
                    'because', 'unlike', 'unless', 'through',
                    'onto', 'when', 'unto', 'beyond', 'off',
                    'since', 'along', 'against']
    
    COMMON_WORDS_UPPERCASE: list[str] = [word.upper() for word in COMMON_WORDS]
    COMMON_WORDS_CAPITAL: list[str] = [word.capitalize() for word in COMMON_WORDS]
    
    SEPARATORS: list[str] = [' ', '-', '.', ',', '(', ')', '[', ']', ':', '\n', '\t']
    
    WORDS = COMMON_WORDS + COMMON_WORDS_UPPERCASE + COMMON_WORDS_CAPITAL + SEPARATORS

 
class WikiScrapper:
    
    article_title: str
    article_text: str
    
    def __init__(self) -> None:
        
        self.article_title, self.article_text  = self._parse_content()
    
    @DeprecationWarning
    def _random_article(self) -> None:
        
        page = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
        print(page)

    @staticmethod
    def get_random_article_title() -> str:
        with open('titles_temp.txt', 'a') as titles:
            """
            TODO
            
            ADD EXCEPTION HANDLING FOR 
            NON-EXISTING ARTICLE ERROR
            """
        
            url = requests.get('https://en.wikipedia.org/wiki/Special:Random')
            soup = BeautifulSoup(url.content, 'html.parser')
            title = soup.find(class_='firstHeading').text
            
            titles.write(datetime.today().strftime('%Y-%m-%d') + f' {title}' + '\n')
            titles.close()
            
            return title 
    
    @staticmethod
    def get_article_text(title: str, print_content: bool = False) -> str:
        
        
        """
        TODO
        
        Test random article method with 
        list of articles
        """
        
        wiki = wikipedia.page(title)  # 'Belgian Ship A4'
        text_content = wiki.content
        
        if print_content: print(text_content)
        
        return text_content
        
    def _parse_content(self) -> tuple[str, str]:
        
        article_title = self.get_random_article_title()
        article_text = self.get_article_text(title=article_title)
        
        return article_title, article_text


class WikiArticleParser(WikiScrapper, Titles, Parameters):
    
    filtered_text: str

    def __init__(self) -> None:
        super(WikiArticleParser, self).__init__()

    @staticmethod
    def clean_text(text: str, clear_new_lines: bool) -> str:
        
        text = re.sub(r'==.*?==+', '', text)
        if clear_new_lines: text = text.replace('\n', '')
        
        return text
    
    def filter_article(self) -> str:
        
        self.filtered_text = ''
        
        for word in self.article_text:
            if word not in self.WORDS:
                
                word = ' '
                "{:<15}".format(word)
                
                word += self.filtered_text
                
            else: word+= self.filtered_text
            
    def get_content(self) -> tuple[str, str]:
        return self.article_title, self.article_text
            
def retry(self, ExceptionToCheck: Exception, m_tries: int, m_delay: float) -> Callable[[OriginalFunc], DecoratedFunc]:
    def decorator(f: OriginalFunc) -> DecoratedFunc:
        @wraps(f)
        def wrapper(*args, **kwargs) -> RetType:
            try: 
                f(*args, **kwargs)
            except Exception as e:
                while m_tries > 0:
                    f(*args, **kwargs)
                    max_tries -= 1
            return wrapper
        return decorator
        
      
if __name__ == "__main__":
    
    article_parser = WikiArticleParser()
    article_parser.get_article_text('Prehistory', print_content=True)
    
