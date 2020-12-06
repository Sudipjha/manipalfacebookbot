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
    specialities = {'Cancer Care':'2','Cardiology':'3','Cardiothoracic Vascu':'27','Accident & Emergency':'57', 'Paediatric Endocrino': '71','Paediatric Surger':'65', 'Radiotherapy':'70','Gastrointestinal Sci':'6','Laparoscopic Surgery':'62','Nephrology':'8','Neurology':'9','Neurosurgery':'58','Obstetrics & Gynaeco':'10','Orthopaedics':'12','Paediatric And Child':'4','Rheumatology':'13','Spine Care':'14','Urology':'15','Anesthesiology':'17','Bariatric Surgery':'18','Dental Medicine':'21','Dermatology':'22','Diabetes and Endocri':'23','Ear Nose Throat':'24','Fetal Medicine':'25','General Medicine':'26','General Surgery':'28','Genetics':'27','Geriatric Medicine':'29','Hepatobiliary Surger':'34','ICU & Critical Care':'35','Infectious Disease':'36','Internal Medicine':'37','Laboratory Medicine':'39','Neonatology & NICU':'40','Nuclear Medicine':'41','Nutrition And Dietet':'42','Ophthalmology':'43','Plastic And Cosmetic':'46','Psychiatry':'48','Psychology':'49','Pulmonology':'50','Radiology':'51','Rehabilitation Medic':'52','Sports Medicine':'56','vascular-surgery':'63','Transfusion Medicine':'64','Pathology':'60','Organ Transplant':'12','Bone Marrow Transpla':'19','Hematology':'33','Microbiology':'61','Heart Care Clinic':'69','Lifestyle Clinic':'67','Liver Clinic':'68','Pain Medicine':'44','Physiotherapy':'59','Renal Sciences':'53','Robotic Assisted Sur':'55','Liver Transplantatio':'7','Clinical Psychology':'20','IVF and Infertility':'38'}
    api_response = requests.get('https://test.manipalhospitals.com/chatbot-get-doctor-by-speciality/'+str(req['location'])+'/'+specialities[req['speciality']],auth = HTTPBasicAuth('manipalchatbotapi','manipalchatbotapi'))

    speciality_response = json.loads(api_response.text)
    count = min(len(speciality_response),10)
   
    element = []
    for i in range(count):
        gallery = {
                  "image_url":speciality_response[i]['photo'],
                  "title":speciality_response[i]['doc_name'],
                  "subtitle":speciality_response[i]['DeptName'],
            "buttons":[
                {
                  "type":"show_block",
                  "block_names":["Welcome Message"],
                  "title":"Book Appointment"
                },
                {
                  "type":"web_url",
                   "webview_height_ratio": "tall",
                   "url":"https://www.manipalhospitals.com/?%20",
                   "title":"View Profile"
                },
            ]
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