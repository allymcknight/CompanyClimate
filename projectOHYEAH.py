import simplejson
import unirest
import requests
import json
import pprint

printer = pprint.PrettyPrinter()
range1 = range(8)

input1 = raw_input("Please search:")

for i in range1:
  payload = {'q': input1, 'v': '1.0', "rsz":8, 'start' : i}
  response = requests.get("https://ajax.googleapis.com/ajax/services/search/news", params=payload).json()
  # printer.pprint(response)


  total_content = []
  for e in range(len(response["responseData"]["results"])):
      total_content.append(response["responseData"]["results"][e]["content"])

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
    # print total_content[i]

    # print result.body
    if result.body['probability']['neg'] > .6 or result.body['label'] =='neg':
        print total_content[e]
        print "Pretty negative"
    elif result.body['probability']['pos'] > .6 or result.body['label'] =='pos':
        print total_content[e]
        print "Pretty positive"
