# Install
# pip install -U ibm-watsonx-ai python-dotenv
# pip install ibmcloudant
# pip install flask flask-cors
# pip install -U ibm-watsonx-ai python-dotenv
# pip install openai
# pip install fastapi
# pip install gunicorn
import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS  # allow cross-origin requests in dev
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
# from ibm_watsonx_ai import Credentials, APIClient
# from ibm_watsonx_ai.foundation_models import ModelInference
# from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from openai import OpenAI
#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware

#For Flask App
app = Flask(__name__)
#For FastAPI
#app = FastAPI()

ALLOWED_ORIGINS = ["https://onrender.com",
"http://127.0.0.1","http://localhost"]

CORS(
    #app,
    resources={r"/api/*": {"origins": ALLOWED_ORIGINS}},
    supports_credentials=True, # only if you use cookies
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization","Accept"],
    max_age=86400
)

# 1. Load Credentials & Global Variables
load_dotenv("Secrets.env")
NASA_API_KEY = os.environ["NASA_API_KEY"]
CLOUDANT_API_KEY = os.environ["CLOUDANT_API_KEY"]
CLOUDANT_SERVICE_URL = os.environ["CLOUDANT_SERVICE_URL"]
CLOUDANT_DB = os.environ["CLOUDANT_DB"]
#Connection Process for IBM WatsonX AI Model (granite-4-h-small)
# WATSONX_API_KEY = os.environ["WATSONX_API_KEY"]
# WATSONX_URL = os.environ["WATSONX_URL"]
# WATSONX_PROJECT_ID = os.environ["WATSONX_PROJECT_ID"]
# creds = Credentials(
# api_key=os.environ["WATSONX_API_KEY"],
# url=os.environ["WATSONX_URL"],
# )
# project_id = os.environ["WATSONX_PROJECT_ID"]

# #2. Init Client + Picking Up a Granite Model for the account
# client = APIClient(credentials=creds, project_id=project_id)
# params = {
# GenParams.MAX_NEW_TOKENS: 300,
# GenParams.TEMPERATURE: 0.2,     # low temp for more factual outputs
# GenParams.TOP_P: 0.9,
# }
# model = ModelInference(
# model_id="ibm/granite-4-h-small",  # or another Granite instruct model you have access to
# params=params,
# credentials=creds,
# project_id=project_id,
# )

#Connection Process for the OpenAI (GPT-5) Model
openaiclient = OpenAI()

#3-a. Predict Irrigation in MARS
@app.get("/api/irrigation")
def predict_irrigation():
    #4. Fetching Information from NASA's InSight MARS API
    resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
    resp.raise_for_status() 

    #5. Storing those Information into the IBM Cloudant
    # Setting Up Authenticator with the IBm Cloud API Key
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    # Initializing the Cloudant Client with the Service URL 
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_SERVICE_URL)

    #6. Inserting Documents in the Cloudant
    try:
        # This Generates an Unique Server-Side Document ID Automatically
        response = client.post_document(
                db=CLOUDANT_DB,
                document=resp.json()
            ).get_result()
        print("Success! Document inserted.")
    
    #7. Capturing the Exceptions
    except ApiException as ae:
        print(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
  
    #8. Prompt: using a JSON and returning
    prompt=f"""
    You are a space scientist. So, could you please analyze the data {resp.json()} and predict the irrigation in Mars?
    """
    #Response from IBM WatsonX AI (granite-4-h-small) Model
    #res = model.generate(prompt=prompt)

    #Response from OpenAI (gpt-5) Model
    res = openaiclient.responses.create(
    model="gpt-5",
    input= prompt
    )
    print(res.output_text)
    #print(res["results"][0]["generated_text"])
    return res.output_text

#3-b. Predict Diseases in MARS
@app.get("/api/disease")
def predict_disease():
    #4. Fetching Information from NASA's InSight MARS API
    resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
    resp.raise_for_status() 

    #5. Storing those Information into the IBM Cloudant
    # Setting Up Authenticator with the IBm Cloud API Key
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    # Initializing the Cloudant Client with the Service URL 
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_SERVICE_URL)

    #6. Inserting Documents in the Cloudant
    try:
        # This Generates an Unique Server-Side Document ID Automatically
        response = client.post_document(
                db=CLOUDANT_DB,
                document=resp.json()
            ).get_result()
        print("Success! Document inserted.")
    
    #7. Capturing the Exceptions
    except ApiException as ae:
        print(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    #8. Prompt: using a JSON and returning
    prompt=f"""
    You are a space scientist. So, could you please analyze the data {resp.json()} and predict the diseases in Mars?
    """
    #Response from IBM WatsonX AI (granite-4-h-small) Model
    #res = model.generate(prompt=prompt)
    
    #Response from OpenAI (gpt-5) Model
    res = openaiclient.responses.create(
    model="gpt-5",
    input= prompt
    )
    print(res.output_text)
    #print(res["results"][0]["generated_text"])
    return res.output_text

#3-c. Predict Energy Optimization in MARS
@app.get("/api/energy")
def predict_enery():
    #4. Fetching Information from NASA's InSight MARS API
    resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
    resp.raise_for_status() 

    #5. Storing those Information into the IBM Cloudant
    # Setting Up Authenticator with the IBm Cloud API Key
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    # Initializing the Cloudant Client with the Service URL 
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_SERVICE_URL)

    #6. Inserting Documents in the Cloudant
    try:
        # This Generates an Unique Server-Side Document ID Automatically
        response = client.post_document(
                db=CLOUDANT_DB,
                document=resp.json()
            ).get_result()
        print("Success! Document inserted.")
    
    #7. Capturing the Exceptions
    except ApiException as ae:
        print(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    #8. Prompt: using a JSON and returning
    prompt=f"""
    You are a space scientist. So, could you please analyze the data {resp.json()} and predict the energy optimization in Mars?
    """
    #Response from IBM's WatsonX AI (granite-4-h-small) Model
    #res = model.generate(prompt=prompt)
    
    #Response from OpenAI (gpt-5) Model
    res = openaiclient.responses.create(
    model="gpt-5",
    input= prompt
    )
    print(res.output_text)
    #print(res["results"][0]["generated_text"])
    return res.output_text

# For Flask App Running Point 
if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000, debug=True)