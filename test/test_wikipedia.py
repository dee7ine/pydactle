import unittest
from pydactle import articles, utilities, titles
import random

import sys, os
# sys.path.append(os.path.abspath(os.path.join('..', 'pydactle', 'src')))


class TestWikiArticleParser(unittest.TestCase):

    def setup(self) -> tuple[articles.WikiArticleParser, list[str]]:
        
        parser = articles.WikiArticleParser()
        title_list = titles.ALL_TITLES
        return parser, title_list
    
    def test_random_article(self):
        parser, title_list = self.setup()
        
        parser.get_article_text(random.choice(title_list), print_content=True)


if __name__ == '__main__':
    unittest.main()
