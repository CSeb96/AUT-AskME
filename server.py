#Python libraries that we need to import for our bot
import requests
from flask import Flask, request
from pymessenger.bot import Bot 
import apiai, json

# FB creds
ACCESS_TOKEN = 'EAADKrgXhyyUBAEp4kVuSkicUui79hVCDx6CjYCZA2z2tCC1vuPXNZA0nzVaSIkxeisxg2JWOKxabHA1QkMhSP4gFGYCff4WS4D9MCs8x8VgzN9J9pKZAIEoXMxOiNlgcLzJCawIVZCbmOZAwZCPnrRXgk5anZBCK3pFnxNanXItPxj50NZCDToyC'

# api.ai creds
CLIENT_ACCESS_TOKEN = "0cd86c9764784512b3816545578780cd"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return 'Hello World (from Flask!)', 200

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }

    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'
    req.query = message

    # get response from api.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        response = response_obj["result"]["fullfillment"]["speech"]
        reply(sender, response)

    return "ok"

if __name__ == '__main__':
    app.run()
