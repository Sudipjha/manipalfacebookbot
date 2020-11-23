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
    
    
    if req['queryResult']['intent']['displayName'] == 'english - book appointment - banaguluru':
        search_id = req['queryResult']['parameters']['Banguluruhospitals']
        api_response = requests.get('https://test.manipalhospitals.com/chatbot-get-hospitals-speciality/'+str(search_id),auth = HTTPBasicAuth('manipalchatbotapi','manipalchatbotapi'))
        speciality_response = json.loads(api_response.text)
        items = []
        for i in range(len(speciality_response)):
            my_dict = {}
            my_dict["info"] = {"key":speciality_response[i]['name']}
            my_dict["title"] = speciality_response[i]['name']
            my_dict["image"] = {}
            items.append(my_dict)
        return {
        "fulfillmentMessages": [
          {
            "platform": "ACTIONS_ON_GOOGLE",
            "simpleResponses": {
              "simpleResponses": [
                {
                  "textToSpeech": "Select the specialty you are looking for:"
                }
              ]
            }
          },
          {
            "platform": "ACTIONS_ON_GOOGLE",
            "listSelect": {
              "title": "Centre Of Excellence",
              "items": items
            }
          }
        ]}
    
    if req['queryResult']['intent']['displayName'] == 'english - book appointment - otherhospitals':
        search_id = req['queryResult']['parameters']['otherhospitals']
        api_response = requests.get('https://test.manipalhospitals.com/chatbot-get-hospitals-speciality/'+str(search_id),auth = HTTPBasicAuth('manipalchatbotapi','manipalchatbotapi'))
        speciality_response = json.loads(api_response.text)
        items = []
        for i in range(len(speciality_response)):
            my_dict = {}
            my_dict["info"] = {"key":speciality_response[i]['name']}
            my_dict["title"] = speciality_response[i]['name']
            my_dict["image"] = {}
            items.append(my_dict)
        return {
        "fulfillmentMessages": [
          {
            "platform": "ACTIONS_ON_GOOGLE",
            "simpleResponses": {
              "simpleResponses": [
                {
                  "textToSpeech": "Select the specialty you are looking for:"
                }
              ]
            }
          },
          {
            "platform": "ACTIONS_ON_GOOGLE",
            "listSelect": {
              "title": "Centre Of Excellence",
              "items": items
            }
          }
      ]}
    
    #print(req)
    if req['queryResult']['intent']['displayName'] == 'english - find doctors - specialties1' or 'old airport road - cardiology':
        #loc_id= req['queryResult']['parameters']['Banguluruhospitals']['otherhospitals']
        
        search_id = req['queryResult']['parameters']['Specialties']
        api_response = requests.get('https://test.manipalhospitals.com/chatbot-get-doctor-by-speciality/'+req['queryResult']['outputContexts'][0]['parameters']['Banguluruhospitals']+'/'+str(search_id),auth = HTTPBasicAuth('manipalchatbotapi','manipalchatbotapi'))
#         api_response = requests.get('https://www.manipalhospitals.com/patient_api/index_get',auth = HTTPBasicAuth('manipal','M@AnipalDoc##2020'))
        api_response = json.loads(api_response.text)
        items = []
        for i in range(10):
            my_dict = {}
            image_dict = {}
            key = {}
            key['key'] = api_response[i]['DoctorCode']
            image_dict['imageUri'] = api_response[i]['photo']
            image_dict['accessibilityText'] = api_response[i]['doc_name']
            my_dict['info'] = key
            my_dict['title'] = api_response[i]['doc_name']
            my_dict['description'] = api_response[i]['DeptName']
            my_dict['image'] = image_dict
            items.append(my_dict)
        
        return  {'fulfillmentMessages': [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": "Here is the list of Doctors"
            }
          ]
        }
      },
       {
         "platform": "ACTIONS_ON_GOOGLE",
         "carouselSelect": {
           "items":items
         }
       }
     ]}
    
    
    # fetch action from json
    
    #return {'fulfillmentMessages':[{"text":{"text":['Hello']}}]}
    # return a fulfillment response
    

# create a route for webhook
@app.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()