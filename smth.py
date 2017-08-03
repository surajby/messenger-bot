from flask import Flask, request
import json
import requests

app = Flask(__name__)

PAT='EAABuoWG7a6QBAGlwn7oWpuIeTZCPZAynfiCCpeZBwnDyvGlWPY4mLwDQWAkQOwPPrvfMrP5LBCqaKL584aBiJWmZAE0IgA96AU8WQ5xPH7Pz1EpAxW6esPZAoltRjs6ZBAhuY1oyoVrCiOrdHPYkDVS8C24AYjcMX3N23Sk8FJsiPNjCy640kg'
@app.route('/',methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token','') == 'brahma_eswara_maheswara':
        return request.args.get('hub.challenge','')
    else:
        return "is it to late to say sorry, coz im literally missing body"
        
@app.route('/',methods=['POST'])
def handle_messages():
    payload = request.get_data()
    for sender,message in messaging_events(payload):
        send_message(PAT, sender, message)
    return "ok"
    
def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data['entry'][0]['messaging']
    for event in messaging_events:
        if 'message' in event and 'text' in event['message']:
            yield event['sender']['id'], event['message']['text'].encode('unicode_escape')
        else:
            yield event['sender']['id'], "Oops!"
            
def send_message(token, recipient, text):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
params={"access_token": token},
data=json.dumps({
  "recipient": {"id": recipient},
  "message": {"text": text.decode('unicode_escape')}
}),
headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

if __name__ == '__main__':
  app.run()                        
    
    