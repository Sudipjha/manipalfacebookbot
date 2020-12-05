# import flask dependencies
from flask import Flask, request, make_response, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json


# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    specialities = {'Cancer Care':'2','Cardeology':'3','Cardiothoracic Vascu':'27'}
    api_response = requests.get('https://test.manipalhospitals.com/chatbot-get-doctor-by-speciality/'+str(req['location'])+'/'+specialities[req['speciality']],auth = HTTPBasicAuth('manipalchatbotapi','manipalchatbotapi'))

    speciality_response = json.loads(api_response.text)
    count = min(len(speciality_response),10)
   
    element = []
    for i in range(10):
        gallery = {
                  "image_url":speciality_response[i]['photo'],
                  "title":speciality_response[i]['doc_name'],
                  "subtitle":speciality_response[i]['DeptName'],
        }
        element.append(gallery)
    if len(element)>0:
        answer = {
     "messages": [
        {
          "attachment":{
            "type":"template",
            "payload":{
              "template_type":"generic",
              "elements":element
            }
          }
        }
      ],
    }
    else:
        answer = {
         "messages": [
           {"text": "Sorry I couldn't find doctors for you."},
         ]
        }
    
    return answer
    
    
   

# create a route for webhook
@app.route('/sp/', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()