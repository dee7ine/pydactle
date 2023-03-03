import unittest
from wiki.articles import WikiArticleParser
from wiki.titles import Titles
import random


class TestWikiArticleParser(unittest.TestCase):

    def setup(self) -> tuple[WikiArticleParser, property]:
        
        parser = WikiArticleParser()
        titles = Titles.all_titles
        
        return parser, titles
    
    def test_random_article(self) -> None:
        parser, titles = self.setup()
        
        parser.get_article_text(random.choice(titles), print_content=True)


if __name__ == '__main__':
    unittest.main()
