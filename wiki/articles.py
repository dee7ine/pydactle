import requests
import wikipedia
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

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
    COMMON_WORDS = ['the', 'at', 'there', 'some', 'my',
                    'of', 'be', 'use', 'her', 'than',
                    'and', 'this','an'	,'would','first',
                    'a'	,'have'	,'each'	,'make'	,'water',
                    'to','from'	,'which','like'	,'been',
                    'in','or', 'do', 'into', 'who', 'how',		
                    'that', 'by', 'if', 'but', 'will', 'not',
                    'up', 'other', 'what', 'more', 'for', 'on',
                    'all', 'about', 'go', 'out', 'as', 'with', 'when',
                    'then', 'no', 'may', 'so', 'such', 'despite', 
                    'beneath', 'now', 'during', 'after', 'was', 'were',
                    'because', 'unlike', 'unless', 'through', 'onto',
                    'unto', 'beyond']
    
    COMMON_WORDS_UPPERCASE = (word.upper() for word in COMMON_WORDS)
    COMMON_WORDS_CAPITALIZE = (word.capitalize() for word in COMMON_WORDS)
    
    SEPARATORS = [' ', '-', '.', ',', '(', ')', '[', ']', ':']


class WikiContentParser:

    def __init__(self) -> None:
        
        self.article_text, self.article_title = self.parse_content()
        print(f'Article title:  {self.article_title}')
        print(f'Article content:\n{self.article_text}')

    @staticmethod
    def get_article_list() -> None:
        
        session = requests.Session()
        response = session.get(url=API_URL, params=PARAMS)
        
        data = response.json()
        
        random_articles = data["query"]["random"]
        
        for article in random_articles:
            print(article["title"])

    @DeprecationWarning
    def random_article(self) -> None:
        
        page = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
        print(page)

    @staticmethod
    def get_random_article_title() -> str:
        with open('titles_temp.txt', 'a') as titles:
        
            url = requests.get('https://en.wikipedia.org/wiki/Special:Random')
            soup = BeautifulSoup(url.content, 'html.parser')
            title = soup.find(class_='firstHeading').text
            
            titles.write(datetime.today().strftime('%Y-%m-%d') + f' {title}' + '\n')
            titles.close()
            
            return title 

    @staticmethod
    def get_article_text(title: str) -> str:
        
        wiki = wikipedia.page(title)  # 'Belgian Ship A4'
        text_content = wiki.content
        
        return text_content

    @staticmethod
    def clean_text(text: str, clear_new_lines: bool) -> str:
        
        text = re.sub(r'==.*?==+', '', text)
        if clear_new_lines: text = text.replace('\n', '')
        
        return text
    
    def parse_content(self) -> tuple[str, str]:
        
        article_title = self.get_random_article_title()
        
        article_text = self.get_article_text(title=self.get_random_article_title())
        article_text = self.clean_text(text=article_text, clear_new_lines=False)
        
        return article_text, article_title
      
if __name__ == "__main__":
    
    content_parser = WikiContentParser()
    
