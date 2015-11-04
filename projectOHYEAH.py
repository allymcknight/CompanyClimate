import simplejson
import unirest
import requests
import json
import pprint
from bs4 import BeautifulSoup as BS 
import lxml
from flask import Markup
from yahoo_finance import Share

# printer = pprint.PrettyPrinter()

yahoo = Share('GOOG')
print yahoo.get_open()

def get_results(search):

  neg_results = {}
  pos_results = {}
  num_positive = 0
  num_negative = 0
  num_neutral = 0



  for i in range(8):
    payload = {'q': search, 'v': '1.0', "rsz":8, 'start' : i}
    response = requests.get("https://ajax.googleapis.com/ajax/services/search/news", params=payload).json()
    # printer.pprint(response)


    total_content = []
    for e in range(len(response["responseData"]["results"])):
        url_content = requests.get(response["responseData"]["results"][e]["unescapedUrl"])
        soup = BS(url_content.text, 'lxml')
        article_body = (soup.body.find_all('p'))
        total_content.append(article_body)

    for e in range(len(total_content)):

      result = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
      headers={
        "X-Mashape-Key": "Ww5fx7iRxAmshWkYsxLrFKxvGQPfp1FBnDJjsnKZ4hfLm4yZQz",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      },
      params={
        "language": "english",
        "text": total_content[e]
      
      }
    )

      
      if result.body['probability']['neg'] > .6 or result.body['label'] =='neg':

        sentiment_score = result.body['probability']['neg']-result.body['probability']['pos']
        content = Markup(response["responseData"]["results"][e]["content"])
        url =  Markup(response["responseData"]["results"][e]["unescapedUrl"])
        title = Markup(response["responseData"]["results"][e]["title"])
        article = [content, url, title]
        print title
        neg_results[title] = article
        num_negative += 1

      elif result.body['probability']['pos'] > .6 or result.body['label'] =='pos':
        
        sentiment_score = result.body['probability']['neg']-result.body['probability']['pos']
        content = Markup(response["responseData"]["results"][e]["content"])
        url =  Markup(response["responseData"]["results"][e]["unescapedUrl"])
        title = Markup(response["responseData"]["results"][e]["title"])
        article = [content, url, title]
        print title
        pos_results[title] = article
        num_positive += 1

      else:
        num_neutral += 1

  positive_value = pos_results.keys()
  positive_values = positive_value
  negative_value = neg_results.keys()
  negative_values = negative_value
  return neg_results, pos_results, positive_values, negative_values, num_positive, num_negative, num_neutral



