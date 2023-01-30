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

def get_article_list() -> None:
    session = requests.Session()
    response = session.get(url=API_URL, params=PARAMS)
    
    DATA = response.json()
    
    RANDOMS = DATA["query"]["random"]
    
    for r in RANDOMS:
        print(r["title"])

@DeprecationWarning
def random_article() -> None:
    """
    Get random wikipedia article
    
    :return 
    """
    
    page = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
    print(page)
    
def get_random_article_title() -> None:
    url = requests.get('https://en.wikipedia.org/wiki/Special:Random')
    soup = BeautifulSoup(url.content, 'html.parser')
    title = soup.find(class_='firstHeading').text
    text = soup.p.text
    print(f'Article title: {title}')
    print(f'Article text: {text}')
    
def get_article_text() -> None:
    wiki = wikipedia.page('Belgian Ship A4')
    text = wiki.content
    
    #cleaning text
    text = re.sub(r'==.*?==+', '', text)
    text = text.replace('\n', '')
    print(text)
    print(type(text))
    
      
if __name__ == "__main__":
    # get_random_article()
    # get_article_list()
    get_article_text()
    
    
