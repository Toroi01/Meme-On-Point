import tweepy
import logging
from config import create_api
import time
import schedule
from datetime import datetime
from get_memes_web import *
import random
import os
from reply_chat_bot import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
api = create_api()

#DEV NOTE: 1179083987404427267

#---------Reply with memes--------------
NUMERO_DE_TONTOS = 3
FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def request_with_memes():
    logger.info(f"###########################################")
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id)

    #Iterate through all the mentions and reply each one
    for mention in reversed(mentions):
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        #tweet_text = ' '.join(mention.text.split()[1:])
        #DELETE chivato
        logger.info(f"------------------------------> Replying to {mention.user.screen_name} {mention.text}")

        #Chose the meme for the tweet
        most_accurate_meme = ""
        try:
            most_accurate_meme = get_meme_giphy(mention.text)          
            #most_accurate_meme = memeFinder(tweet_text)
        except:
            most_accurate_meme="memes/tonto"+str(random.randrange(1,NUMERO_DE_TONTOS+1))+".jpg"
            
        #Reply with the meme
        api.update_status('@' + mention.user.screen_name,in_reply_to_status_id=mention.id,media_ids=[api.media_upload(most_accurate_meme).media_id])
    logger.info(f"###########################################")
#---------END--------------

#---------Chat--------------
def get_last_message_id(sender_id):
    '''
    if exist return the last message id
    else False
    '''
    with open("direct_messages_log.txt") as f:
        lines = f.readlines()
        for line in lines:
            clean_line = line.replace('\n', '')
            temp_sender_id = clean_line.split(":")[0]
            if(temp_sender_id == str(sender_id)):
                return clean_line.split(":")[1]
        return False
    
def store_new_entry(sender_id, message_id):
    f_write = open("direct_messages_log.txt", 'a+')
    f_write.write(str("\n")+str(sender_id)+":"+str(message_id))
    f_write.close()      
    return

def update_message_id(sender_id,new_message_id):
    with open("direct_messages_log.txt",'r') as f:
        lines = f.readlines()
        for index,line in enumerate(lines):
            clean_line = line.replace('\n', '')
            temp_sender_id = clean_line.split(":")[0]
            if(temp_sender_id == str(sender_id)):
                lines[index]=str(sender_id)+":"+str(new_message_id)+str("\n")
                with open('direct_messages_log.txt', 'w') as file:
                    file.writelines(lines)
                return
        return False

def get_chat_format(sender_id,direct_messages):
    messages = []
    #Get messages from sender_id
    for message in reversed(direct_messages):
        if(str(sender_id) == message.message_create["sender_id"]):
            messages.append("You: "+message.message_create["message_data"]["text"])
            
        elif(str(sender_id) == message.message_create["target"]["recipient_id"]):
            messages.append("Me: "+message.message_create["message_data"]["text"])

    chat = "\n".join(messages)

    #Limit the chat in the last 4 messages, WE ASUME THAT THE MODEL WILL CREATE \n
    try:
        num_messages = [i for i, ltr in enumerate(chat) if ltr == "\n"]
        reduced_chat = chat[num_messages[3]::]
        return reduced_chat
    except:
        return chat
    
    
def chat_bot():
    direct_messages = api.list_direct_messages()
    for message in direct_messages:
        sender_id = int(message.message_create["sender_id"])
        message_id = int(message.id)        

        if(sender_id!=1169058495934713856):
            #Check if sender_id exist
            #YES -> go to else
            #NO -> Create a new entry sender_id:message_id
            last_message_id = get_last_message_id(sender_id)
            if (last_message_id == False):
                store_new_entry(sender_id,message_id)
                chat = get_chat_format(sender_id,direct_messages)
                logger.info(f"------------------------------> Direct message to {sender_id}")
                reply = get_reply(chat)
                api.send_direct_message(sender_id,reply)
            else:
                #Check if message_id>last_message_id
                #Yes = update message_id and reply
                #No pass
                if(message_id>int(last_message_id)):
                    update_message_id(sender_id,message_id)
                    chat = get_chat_format(sender_id,direct_messages)
                    logger.info(f"------------------------------> Direct message to {sender_id}")
                    reply = get_reply(chat)
                    logger.info(f"Reply: {reply}")
                    api.send_direct_message(sender_id,reply)
            
            

        
        #Check if is the newest message (bigger last_message_id) from sender_id
        #YES -> update last_message_id, update is_replyed=false and reply
        #NO ->  pass

        #For all the messages that have is_replyed=false reply to them with the model
        
        
    

#---------END--------------
def memeOnPoint():
    chat_bot()
    request_with_memes()
    


def main():
    while(True):
        chat_bot()
        request_with_memes()
        time.sleep(60)
        
##    schedule.every(60).seconds.do(memeOnPoint)
##    while True:
##        schedule.run_pending()
##        logger.info("Waiting "+str(((schedule.next_run()-datetime.now()).seconds)))
##        time.sleep(1)
    

if __name__ == "__main__":
    main()
