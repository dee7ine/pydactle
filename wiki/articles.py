import requests
import wikipedia
import re
from bs4 import BeautifulSoup

API_URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnlimit": "5"
}


class WikiContentParser:

    def __init__(self) -> None:
        
        # article_text = self.get_article_text(title='Belgian Ship A4')
        article_text = self.get_article_text(title=self.get_random_article_title())
        article_text = self.clean_text(text=article_text, clear_new_lines=False)
        print(article_text)

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
        
        url = requests.get('https://en.wikipedia.org/wiki/Special:Random')
        soup = BeautifulSoup(url.content, 'html.parser')
        title = soup.find(class_='firstHeading').text
        text = soup.p.text
        print(f'Article title: {title}')
        print(f'Article text: {text}')
        
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

      
if __name__ == "__main__":
    
    content_parser = WikiContentParser()
    
