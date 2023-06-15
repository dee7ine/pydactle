import unittest
from pydactle.wiki_scraper 
import random

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'pydactle', 'src')))


class TestWikiArticleParser(unittest.TestCase):

    def setup(self) -> tuple[wiki_scraper.articles.WikiArticleParser, list[str]]:
        
        parser = wiki_scraper.articles.WikiArticleParser()
        title_list = wiki_scraper.titles.ALL_TITLES
        return parser, title_list
    
    def test_random_article(self) -> None:
        parser, title_list = self.setup()
        
        parser.get_article_text(random.choice(title_list), print_content=True)


if __name__ == '__main__':
    unittest.main()
