from pydactle import articles, titles
from random import choice

parser = articles.WikiArticleParser()
titles_list = titles.ALL_TITLES
parser.get_article_text(choice(titles_list), print_content=False)
print('done')





