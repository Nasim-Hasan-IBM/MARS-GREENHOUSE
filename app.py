import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
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
"http://127.0.0.1","http://localhost","http://0.0.0.0","/"]

CORS(
    app,
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

#3. Handling the Home/Base (/) Requests 
@app.route('/')
def home():
    return render_template('index.html')

#4. Parsing the JSON Response
def extract_mars_data(raw_json):
    try:
        # Get the first available Sol ID (e.g., "675")
        sol_keys = [key for key in raw_json.keys() if key.isdigit()]
        if not sol_keys:
            return "No valid Sol weather data found."
            
        latest_sol = sol_keys[0]
        sol_data = raw_json[latest_sol]
        
        # Flattening out the metrics safely with fallbacks (.get)
        # AT = Atmospheric Temperature, HWS = Horizontal Wind Speed, PRE = Atmospheric Pressure
        avg_temp = sol_data.get("AT", {}).get("av", "N/A")
        avg_wind = sol_data.get("HWS", {}).get("av", "N/A")
        avg_press = sol_data.get("PRE", {}).get("av", "N/A")
        season = sol_data.get("Season", "N/A")
        
        # Format a tight, human-readable summary string for your LLM prompt
        summary = (
            f"Martian Sol: {latest_sol}, "
            f"Season: {season}, "
            f"Avg Temp: {avg_temp}°C, "
            f"Avg Wind Speed: {avg_wind} m/s, "
            f"Avg Pressure: {avg_press} Pa"
        )
        return summary
    except Exception as e:
        return f"Error parsing data: {str(e)}"

#5-a. Predict Irrigation in MARS
@app.get("/api/irrigation")
def predict_irrigation():
    #6. Fetching Information from NASA's InSight MARS API
    resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
    resp.raise_for_status() 
    raw_data = resp.json()

    #7. Storing those Information into the IBM Cloudant
    # Setting Up Authenticator with the IBm Cloud API Key
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    # Initializing the Cloudant Client with the Service URL 
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_SERVICE_URL)

    #8. Inserting Documents in the Cloudant
    try:
        # This Generates an Unique Server-Side Document ID Automatically
        response = client.post_document(
                db=CLOUDANT_DB,
                document=resp.json()
            ).get_result()
        print("Success! Document inserted.")
        #9. Calling the JSON Parser
        mars_data = extract_mars_data(raw_data)
        #10. Prompt: using a JSON and returning
        prompt = f"""
        You are a space scientist. Analyze the following actual Mars weather telemetry 
        and predict irrigation viability inside an enclosed greenhouse system:
        {mars_data}
        """
        #Response from IBM WatsonX AI (granite-4-h-small) Model
        #res = model.generate(prompt=prompt)

        #Response from OpenAI (gpt-5) Model
        res = openaiclient.responses.create(
        model="gpt-5",
        input= prompt
        )
        return res.output_text
    
    #11. Capturing the Exceptions
    except ApiException as ae:
        return(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
    except Exception as e:
        return(f"An unexpected error occurred: {e}")
    
#5-b. Predict Diseases in MARS
@app.get("/api/disease")
def predict_disease():
    #6. Fetching Information from NASA's InSight MARS API
    resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
    resp.raise_for_status() 
    raw_data = resp.json()

    #7. Storing those Information into the IBM Cloudant
    # Setting Up Authenticator with the IBm Cloud API Key
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    # Initializing the Cloudant Client with the Service URL 
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_SERVICE_URL)

    #8. Inserting Documents in the Cloudant
    try:
        # This Generates an Unique Server-Side Document ID Automatically
        response = client.post_document(
                db=CLOUDANT_DB,
                document=resp.json()
            ).get_result()
        print("Success! Document inserted.")
        #9. Calling the JSON Parser
        mars_data = extract_mars_data(raw_data)
        #10. Prompt: using a JSON and returning
        prompt = f"""
        You are a space scientist. Analyze the following actual Mars weather telemetry 
        and predict disease viability inside an enclosed greenhouse system:
        {mars_data}
        """
        #Response from IBM WatsonX AI (granite-4-h-small) Model
        #res = model.generate(prompt=prompt)

        #Response from OpenAI (gpt-5) Model
        res = openaiclient.responses.create(
        model="gpt-5",
        input= prompt
        )
        return res.output_text
    
    #11. Capturing the Exceptions
    except ApiException as ae:
        return(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
    except Exception as e:
        return(f"An unexpected error occurred: {e}")
    
#5-c. Predict Energy Optimization in MARS
@app.get("/api/energy")
def predict_enery():
    #6. Fetching Information from NASA's InSight MARS API
    resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
    resp.raise_for_status() 
    raw_data = resp.json()

    #7. Storing those Information into the IBM Cloudant
    # Setting Up Authenticator with the IBm Cloud API Key
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    # Initializing the Cloudant Client with the Service URL 
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_SERVICE_URL)

    #8. Inserting Documents in the Cloudant
    try:
        # This Generates an Unique Server-Side Document ID Automatically
        response = client.post_document(
                db=CLOUDANT_DB,
                document=resp.json()
            ).get_result()
        print("Success! Document inserted.")
        #9. Calling the JSON Parser
        mars_data = extract_mars_data(raw_data)
        #10. Prompt: using a JSON and returning
        prompt = f"""
        You are a space scientist. Analyze the following actual Mars weather telemetry 
        and predict energy optimization viability inside an enclosed greenhouse system:
        {mars_data}
        """
        #Response from IBM WatsonX AI (granite-4-h-small) Model
        #res = model.generate(prompt=prompt)

        #Response from OpenAI (gpt-5) Model
        res = openaiclient.responses.create(
        model="gpt-5",
        input= prompt
        )
        return res.output_text
    
    #11. Capturing the Exceptions
    except ApiException as ae:
        return(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
    except Exception as e:
        return(f"An unexpected error occurred: {e}")
    
# For Flask App Running Point 
if __name__ == "__main__":
  # Bind to 0.0.0.0 and use the port provided by Render
  port = int(os.environ.get("PORT", 5000))
  #app.run(host="127.0.0.1", port=port, debug=True) #...For Local...#
  app.run(host="0.0.0.0", port=port, debug=True) #...For Production...#