#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot 
from bs4 import BeautifulSoup
import requests
import os, os.path, csv

app = Flask(__name__)
ACCESS_TOKEN = 'EAADKrgXhyyUBAEp4kVuSkicUui79hVCDx6CjYCZA2z2tCC1vuPXNZA0nzVaSIkxeisxg2JWOKxabHA1QkMhSP4gFGYCff4WS4D9MCs8x8VgzN9J9pKZAIEoXMxOiNlgcLzJCawIVZCbmOZAwZCPnrRXgk5anZBCK3pFnxNanXItPxj50NZCDToyC'
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)


listingurl = "https://www.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/software-development-major"
response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "html.parser")

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    usermessge = message['message'].get('text')
                    response_sent_text = is_msg(usermessge)         # Initialising variable with the function is_msg(message)
                    send_message(recipient_id, response_sent_text)
                ##if user sends us a GIF, photo,video, or any other non-text item
                #if message['message'].get('attachments'):
                #    response_sent_nontext = get_message()
                #    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def is_msg(message):
    greeting = ['hi', 'hello', 'heya', 'sup']
    req = ['links', 'get links']
    if(message in greeting):
        return 'Hi There! How can I help you?'
    
    if(message in req):
        #get_all_links()
        return 'Function get all links is wrong'

def get_all_links():
        content = soup.find("div", {"id": "tab-98630-1"})
        for link in content:
            return soup_find_all('a')


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()