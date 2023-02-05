from __future__ import annotations

import requests
import wikipedia
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
    def _get_random_article_title() -> str:
        with open('titles_temp.txt', 'a') as titles:
        
            url = requests.get('https://en.wikipedia.org/wiki/Special:Random')
            soup = BeautifulSoup(url.content, 'html.parser')
            title = soup.find(class_='firstHeading').text
            
            titles.write(datetime.today().strftime('%Y-%m-%d') + f' {title}' + '\n')
            titles.close()
            
            return title 
    
    @staticmethod
    def _get_article_text(title: str) -> str:
        
        wiki = wikipedia.page(title)  # 'Belgian Ship A4'
        text_content = wiki.content
        
        return text_content
        
    def _parse_content(self) -> tuple[str, str]:
        
        article_title = self._get_random_article_title()
        article_text = self._get_article_text(title=article_title)
        
        return article_title, article_text


class WikiArticleParser(WikiScrapper, Parameters):
    
    filtered_text: str

    def __init__(self) -> None:
        super(WikiArticleParser, self).__init__()
        
        print(f'Article title:  {self.article_title}')
        print(f'Article content:\n{self.article_text}')
        
        print(f'Word list:\n{self.WORDS}')
        self.filter_article()
        print(f'Filtered article:\n{self.filtered_text}')

    @staticmethod
    def clean_text(text: str, clear_new_lines: bool) -> str:
        
        text = re.sub(r'==.*?==+', '', text)
        if clear_new_lines: text = text.replace('\n', '')
        
        return text
    
    def filter_article(self) -> str:
        
        # article_text_list = [word for ]
        self.filtered_text = ''
        
        for word in self.article_text:
            if word not in self.WORDS:
                
                word = ' '
                "{:<15}".format(word)
                
                word += self.filtered_text
                
            else: word+= self.filtered_text
            
            
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
    
