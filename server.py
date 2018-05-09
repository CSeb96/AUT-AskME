#Python libraries that we need to import for our bot
import random
import requests
from flask import Flask, request
from pymessenger.bot import Bot 
import apiai, json

# FB creds
ACCESS_TOKEN = 'EAADKrgXhyyUBAEp4kVuSkicUui79hVCDx6CjYCZA2z2tCC1vuPXNZA0nzVaSIkxeisxg2JWOKxabHA1QkMhSP4gFGYCff4WS4D9MCs8x8VgzN9J9pKZAIEoXMxOiNlgcLzJCawIVZCbmOZAwZCPnrRXgk5anZBCK3pFnxNanXItPxj50NZCDToyC'
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)

# api.ai creds
CLIENT_ACCESS_TOKEN = "0cd86c9764784512b3816545578780cd"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
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
                        response_sent_text = reply(usermessge)
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def reply(msg):
    request = ai.text_request()
    request.query = msg

    byte_response = request.getresponse().read()
    json_response = byte_response.decode('utf-8').replace("'", '"') # replaces all quotes with double quotes
    response = json.loads(json_response)

    return response

#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are good!", "We're so proud of you.", "Keep on being you boo!", "We're greatful to know you boo:)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()
