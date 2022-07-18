from requests import get
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def parse_blog_articles(url):
    """
    This function used together with the get_blog_articles() function, 
    parses the html from the website and displays it in python
    """
    url = url
    
    # establish header
    headers = {'User-Agent':'CodeUp Data Science'}
    resposne = get(url, headers=headers)
    
    # create soup variable containing response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # create a dictionary that holds each url and its content
    output = {}
    output['title'] = soup.find('h1', class_ = 'entry-title').text
    output['published'] = soup.find('span', class_='published').text
    output['category'] = soup.find('a', rel='category tag').text
    output['content'] = soup.find('div', class_='entry-content').text.strip().replace('\n', ' ')
    
    return output


def get_blog_articles(url):
    """
    This function takes in a list of url from CodeUp blod articles.
    Used with pare_blog_articles, it looks for title, published date, category, and content
    then displays them.
    """
    output = []
    
    for urls in url:
        output.append(parse_blog_articles(urls))
        
    return output


def parse_news_article(article, category):
    output = {}

    output['category'] = category
    output['title'] = article.find('span', itemprop = 'headline').text.strip()
    output['author'] = article.find('span', class_ = 'author').text
    output['date'] = article.find('span', clas = 'date').text.split(',')[0]
    output['content'] = article.find('div', itemprop = 'articleBody').text

    return output



def parse_news_page(category):
    url = 'https://inshorts.com/en/read/' + category
    response = get(url)
    soup = BeautifulSoup(response.text)

    cards = soup.select('.news-card')
    articles = []

    for card in cards:
        articles.append(parse_news_article(card, category))

    return articles



# cache the data, and turn it into a dataframe (function)
def get_news_articles(use_cache=True):
    if os.path.exists('news_articles.json') and use_cache:
        return pd.read_json('news_articles.json')

    categories = ['business', 'sports', 'technology', 'entertainment']

    articles = []

    for category in categories:
        print(f'Getting {category} articles')
        articles.extend(parse_news_page(category))

    df = pd.DataFrame(articles)
    df.to_json('news_articles.json', orient='records')
    return df
