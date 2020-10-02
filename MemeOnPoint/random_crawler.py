import urllib,json
import urllib.request
from bs4 import BeautifulSoup as bs
import requests
import csv
API_KEY = "1PIXETdt6VmffxPn36D1zwNc54JR4VEI"
headers = {'User-Agent': 'Mozilla/5.0'}

#Random Crawling (Only One Gif by petition)
for i in range(100000):
    url = "http://api.giphy.com/v1/gifs/random?&api_key="+API_KEY
    data=json.loads(urllib.request.urlopen(url).read())
    id = data["data"]["id"]
    #url_web = data["data"]["url"]
    title = data["data"]["title"]
    url_gif = data["data"]["images"]["fixed_height"]["url"]
    #html = requests.get(url_web, headers=headers)
    #soup = bs(html.text, "html.parser")
    #try:
    #    tags = soup.find("meta",{"name":"keywords"})["content"]
    #except:
    #    tags = 'GIF, Animated GIF'

    #Deleted confirmation duplicates (a lot of time)
    if(title != ""):
        with open('db.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([id, url_gif, title])
