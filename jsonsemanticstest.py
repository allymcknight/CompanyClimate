import unirest


response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
                        headers={
                        "X-Mashape-Key": "Ww5fx7iRxAmshWkYsxLrFKxvGQPfp1FBnDJjsnKZ4hfLm4yZQz",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json"
                                },
  params={
    "language": "english",
    "text": "Exxon is the worst"}
)    

print response.body