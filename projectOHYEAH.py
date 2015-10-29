import simplejson
import unirest
import requests
import json
import pprint
from bs4 import BeautifulSoup as BS 
import lxml

printer = pprint.PrettyPrinter()
def get_results(search):

  neg_results = {}
  pos_results = {}

  for i in range(8):
    payload = {'q': search, 'v': '1.0', "rsz":8, 'start' : i}
    response = requests.get("https://ajax.googleapis.com/ajax/services/search/news", params=payload).json()
    printer.pprint(response)


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
          neg_results[result.body['probability']['neg']-result.body['probability']['pos']]=[response["responseData"]["results"][e]["content"], response["responseData"]["results"][e]["unescapedUrl"], response["responseData"]["results"][e]["title"]]

      elif result.body['probability']['pos'] > .6 or result.body['label'] =='pos':
          pos_results[result.body['probability']['pos']-result.body['probability']['neg']]=[response["responseData"]["results"][e]["content"], response["responseData"]["results"][e]["unescapedUrl"], response["responseData"]["results"][e]["title"]]

  positive_values = pos_results.keys()
  negative_values = neg_results.keys()

  return neg_results, pos_results, positive_values, negative_values



