import urllib,json
import urllib.request
from bs4 import BeautifulSoup as bs
import requests
import csv

API_KEY = ""
url = "http://api.giphy.com/v1/gifs/trending?&api_key="+API_KEY+"&limit=1000"
#url = "http://api.giphy.com/v1/gifs/search?q=ryan+gosling&api_key="+API_KEY+"&limit=5"
data=json.loads(urllib.request.urlopen(url).read())
#print (json.dumps(data, sort_keys=True, indent=4))
headers = {'User-Agent': 'Mozilla/5.0'}

#Trending Crawling (Dictionary-List)
for i in range(len(data["data"])):
    id = data["data"][i]["id"]
#   url_web = data["data"][i]["url"]
    title = data["data"][i]["title"]
    url_gif = data["data"][i]["images"]["fixed_height"]["url"]
#   html = requests.get(url_web, headers=headers)
#   soup = bs(html.text, "html.parser")
    #try:
    #    tags = soup.find("meta",{"name":"keywords"})["content"]
    #except:
    #    tags = 'GIF, Animated GIF'
    #print(title)

    if(title != ""):
        with open('db.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([id, url_gif, title])



