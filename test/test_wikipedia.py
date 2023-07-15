import unittest
from pydactle import articles, utilities, titles
from random import choice

class TestWikiArticleParser(unittest.TestCase):

    def setup(self) -> tuple[articles.WikiArticleParser, list[str]]:
        
        parser = articles.WikiArticleParser()
        title_list = titles.ALL_TITLES
        return parser, title_list
    
    def test_random_article(self):
        parser, title_list = self.setup()
        
        parser.get_article_text(choice(title_list), print_content=False)


if __name__ == '__main__':
    unittest.main()
