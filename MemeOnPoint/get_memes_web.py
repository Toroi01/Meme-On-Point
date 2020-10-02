import requests
from bs4 import BeautifulSoup as bs
import urllib
import urllib.request
from tweet_processing import *
import re
import random
from PIL import Image, ImageSequence
from math import log,ceil
import json


#Key api giphy
KEY = "iUHOf3pMBSV8Dy9lCf4cZ74BvGxk6GtH"

def get_meme_giphy(tweet_text):
    '''
    Input:
        string tweet_text
    Output:
        string output
            Filename of the downloaded meme stored at memes/
            usually the file will be at memes/temp.gif
        
    '''
    #Compute the key_words
    #key_words = get_key_words(tweet_text)
    key_words = get_key_words(tweet_text)
    if not key_words:
        key_words = tweet_text.split(" ")    


    #Request a meme with the key_words
    url = "http://api.giphy.com/v1/gifs/translate?s="+'+'.join(key_words)+"&api_key="+KEY+"&weirdness=0"
    request=json.loads(urllib.request.urlopen(url).read())

    #Take the gif with appropriate size and resolution
    #https://developer.twitter.com/en/docs/media/upload-media/uploading-media/media-best-practices
    max_size = 4883000
    max_width = 1280
    max_height = 1080

    best_image = ""
    temp_max_width = 0
    temp_max_height = 0

    for image in request["data"]["images"]:

        if "size" in request["data"]["images"][image] and "width" in request["data"]["images"][image] and "height" in request["data"]["images"][image]:
            image_size = int(request["data"]["images"][image]["size"])
            image_width = int(request["data"]["images"][image]["width"])
            image_height = int(request["data"]["images"][image]["height"])

            if(image_size<max_size and image_width<max_width and image_height<max_height and temp_max_width<image_width and temp_max_height<image_height):
                temp_max_width = image_width
                temp_max_height = image_height
                best_image = image

    #Download the meme
    url = request["data"]["images"][best_image]["url"]
    image_file = open("memes/temp.gif", "wb")
    request_gif = urllib.request.urlopen(url)
    image_file.write(request_gif.read())
    image_file.close()

    return "memes/temp.gif"   


    
def memeFinder(tweet_text):
    tweet_text = ' '.join(mention.text.split()[1:])
    #meme finder with NO API
    if(tweet_text == ""):
            return "memes/salu2.jpg"
        
    search = "-".join(get_key_words(tweet_text))
    
    url = "https://giphy.com/search/" + search
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    html = requests.get(url, headers=headers)
    soup = bs(html.text, "html.parser")

    allScripts = soup.findAll("script")
    ourScript = ""
    for script in allScripts:
        if("Giphy.renderSearch(document.getElementById('gif-results')" in script.get_text()):
            ourScript = script.get_text()
    gifsUrls = []
    pattern = "https://media2.giphy.com/media/.+?(?=\")"
    #Get all the links in the web and download source gif
    for match in re.finditer(pattern, ourScript):
        # Start index of match (integer)
        sStart = match.start()
        # Final index of match (integer)
        sEnd = match.end()
        # Complete match (string)
        sGroup = match.group()
        if(sGroup[-4:] == ".gif" and sGroup.find("source")!=-1):
            gifsUrls.append(sGroup)
            #print('Match "{}" found at: [{},{}]'.format(sGroup, sStart,sEnd))

    memeUrl = random.choice(gifsUrls)
    image_file = open("memes/temp.gif", "wb")
    request_gif = urllib.request.urlopen(memeUrl)
    gif_size = request_gif.length
    image_file.write(request_gif.read())
    image_file.close()
    gif = Image.open("memes/temp.gif")
    gif_dimensions = gif.size
    gif.close()

    #TODO: SOLVE THE TRANSOFRMATION INTO LESS BYTES = refactor resize_gif method
    if(gif_size>5000192):      
        print("Too many MB: "+str(gif_size/1048576))
        resize_gif(100,100)
        #reduce_dimension = ceil(log(gif_size/5000192)/(2*log(2)))
        #resize_gif(int(gif_dimensions[0]/(2**reduce_dimension)),int(gif_dimensions[1]/(2**reduce_dimension)))
    
    if(gif_dimensions[0]>2048 or gif_dimensions[1]>2048):
        resize_gif(2048,2048)

    return "memes/temp.gif"        

def resize_gif(w,h):
    # Output (max) size
    size = w, h

    # Open source
    im = Image.open("memes/temp.gif")

    # Get sequence iterator
    frames = ImageSequence.Iterator(im)

    # Wrap on-the-fly thumbnail generator
    def thumbnails(frames):
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail.thumbnail(size, Image.ANTIALIAS)
            yield thumbnail

    frames = thumbnails(frames)

    # Save output
    om = next(frames) # Handle first frame separately
    om.info = im.info # Copy sequence info
    om.save("memes/temp.gif", save_all=True, append_images=list(frames))
        



















def match(tweet_tokens):
	current_word = nlp(tweet_tokens)
	#print(current_word)
	meme_tags = ""
	best_similarity = 0
	
	with open('db.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				current_tag = nlp(row[2])
				current_similarity = current_word.similarity(current_tag)
				#print(current_similarity)
				#print(best_similarity)
				#print(row[2])
				
				if current_similarity >best_similarity:
					best_similarity = current_similarity
					best_row  = row
					
	if best_similarity < 0.3:
		return False
	else:
		#Request a meme with the key_words
		url = "http://api.giphy.com/v1/gifs?api_key="+KEY+"&ids="+best_row[0]
		request=json.loads(urllib.request.urlopen(url).read())

		#Take the gif with appropriate size and resolution
		#https://developer.twitter.com/en/docs/media/upload-media/uploading-media/media-best-practices
		max_size = 4883000
		max_width = 1280
		max_height = 1080

		best_image = ""
		temp_max_width = 0
		temp_max_height = 0
		
		#print(request["data"][0]["images"].keys())

		for image in request["data"][0]["images"]:

			if "size" in request["data"][0]["images"][image] and "width" in request["data"][0]["images"][image] and "height" in request["data"][0]["images"][image]:
				image_size = int(request["data"][0]["images"][image]["size"])
				image_width = int(request["data"][0]["images"][image]["width"])
				image_height = int(request["data"][0]["images"][image]["height"])

				if(image_size<max_size and image_width<max_width and image_height<max_height and temp_max_width<image_width and temp_max_height<image_height):
					temp_max_width = image_width
					temp_max_height = image_height
					best_image = image

		#Download the meme
		url = request["data"][0]["images"][best_image]["url"]
		image_file = open("memes/temp.gif", "wb")
		request_gif = urllib.request.urlopen(url)
		image_file.write(request_gif.read())
		image_file.close()
		return "memes/temp.gif" 

