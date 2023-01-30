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

class Wiki_Content_Parser():
    
    def __init__(self):
        
        article_text = self.get_article_text(title='Belgian Ship A4')
        article_text = self.clean_text(text=article_text)
        print(article_text)
    
    def get_article_list(self) -> None:
        session = requests.Session()
        response = session.get(url=API_URL, params=PARAMS)
        
        DATA = response.json()
        
        RANDOMS = DATA["query"]["random"]
        
        for r in RANDOMS:
            print(r["title"])

    @DeprecationWarning
    def random_article(self) -> None:
        """
        Get random wikipedia article
        
        :return 
        """
        
        page = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
        print(page)
        
    def get_random_article_title(self) -> None:
        url = requests.get('https://en.wikipedia.org/wiki/Special:Random')
        soup = BeautifulSoup(url.content, 'html.parser')
        title = soup.find(class_='firstHeading').text
        text = soup.p.text
        print(f'Article title: {title}')
        print(f'Article text: {text}')
        
    def get_article_text(self, title: str) -> str:
        wiki = wikipedia.page(title) # 'Belgian Ship A4'
        text_content = wiki.content
        
        return text_content
        
    def clean_text(self, text: str) -> None:
        
        text = re.sub(r'==.*?==+', '', text)
        text = text.replace('\n', '')
        
        return text
        
        
    
      
if __name__ == "__main__":
    
    content_parser = Wiki_Content_Parser()
    
