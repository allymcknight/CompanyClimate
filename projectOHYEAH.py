import simplejson
import unirest
import requests
import grequests
import json
import pprint
from bs4 import BeautifulSoup as BS 
import lxml
from flask import Markup
from yahoo_finance import Share

# printer = pprint.PrettyPrinter()


def run_googlenews_api(search):
  """Gathers the first 64 Google News articles from a search"""

  news_results = {}

  for i in range(8):
    payload = {'q': search, 'v': '1.0', "rsz":8, 'start' : i}
    response = requests.get("https://ajax.googleapis.com/ajax/services/search/news", params=payload).json()
    for e in range(8):
      content = Markup(response["responseData"]["results"][e]["content"])
      url = response["responseData"]["results"][e]["unescapedUrl"]
      title = Markup(response["responseData"]["results"][e]["title"])
      news_results[url] = [content, url, title]

  return news_results


def article_scraper(news_results):
  """Scrapes the article body from the article URL."""
  for url in news_results.keys():
    url_content = requests.get(url)
    soup = BS(url_content.text, 'lxml')
    article_body = (soup.body.find_all('p'))
    news_results[url].append(article_body)

  return news_results

def analyze_sentiment(article_info):

  rr = []
  for url in article_info.keys():
    rr.append(grequests.post("https://japerk-text-processing.p.mashape.com/sentiment/", 
                       headers={'X-Mashape-Key':'Ww5fx7iRxAmshWkYsxLrFKxvGQPfp1FBnDJjsnKZ4hfLm4yZQz',
                       'Content-Type':'application/x-www-form-urlencoded','Accept':'application/json'},
                       data={'language':'english','text':str(article_info[url][3])}))

      
  response_object = grequests.map(rr)

  for i in range(len(article_info.keys())):
    print i
    print type(i)

    article_info[article_info.keys()[i]].append(response_object[i].json()['probability']['neg'])
    article_info[article_info.keys()[i]].append(response_object[i].json()['probability']['pos'])
    article_info[article_info.keys()[i]].append(response_object[i].json()['label'])

  return article_info


#   for url in article_info.keys():
# result = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
#                        headers={
#                        "X-Mashape-Key": "Ww5fx7iRxAmshWkYsxLrFKxvGQPfp1FBnDJjsnKZ4hfLm4yZQz",
#                        "Content-Type": "application/x-www-form-urlencoded",
#                        "Accept": "application/json"
#                        },
#                        params={
#                        "language": "english",
#                        "text": "i love pineapple",
#   # "text": article_info[url][3]
#                        }
#                      )
#     article_info[url].append(result.body['probability']['neg'])
#     article_info[url].append(result.body['probability']['pos'])
#     article_info[url].append(result.body['label'])

  return article_info

def test_func(n):

  news = run_googlenews_api(n)
  results = article_scraper(news)
  sentiment = analyze_sentiment(results)

  return sentiment

def sort_results(news_w_sent):

  neg_results = {}
  pos_results = {}
  num_positive = 0
  num_negative = 0
  num_neutral = 0


  for url in news_w_sent.keys():
    if news_w_sent[url][4] > .6 or news_w_sent[url][6] == 'neg':
      neg_results[url] = [news_w_sent[url][0], news_w_sent[url][1], news_w_sent[url][2]]
      num_negative += 1

    elif news_w_sent[url][5] > .6 or news_w_sent[url][6] == 'pos':
      pos_results[url] = [news_w_sent[url][0], news_w_sent[url][1], news_w_sent[url][2]]
      num_positive += 1

    else:
      num_neutral =+ 1

  positive_value = pos_results.keys()
  positive_values = positive_value
  negative_value = neg_results.keys()
  negative_values = negative_value

  return neg_results, pos_results, positive_values, negative_values, num_positive, num_negative, num_neutral




