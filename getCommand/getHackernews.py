import json
import urllib.request
import random

url_top50 = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
url_article = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"

def getTop50ID():
    gettop50 = urllib.request.urlopen(url_top50).read()
    return json.loads(gettop50)

def getArticle(top, id):
    article = urllib.request.urlopen(url_article.format(id)).read()
    return json.loads(article)

def getRandomArticle(top):
    r = random.randint(0, len(top))
    article = urllib.request.urlopen(url_article.format(top[r])).read()
    return json.loads(article)