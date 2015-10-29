from bs4 import BeautifulSoup as BS
import requests
import lxml


allytest = requests.get('http://www.sfgate.com/technology/article/Hackbright-Academy-puts-women-coders-in-their-own-4843412.php', verify=True)
soup = BS(allytest.text, 'lxml')
print (soup.body.find_all('p'))
