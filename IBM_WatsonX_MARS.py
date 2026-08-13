# pip install -U ibm-watsonx-ai python-dotenv
import os, json
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials, APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# 1) Load credentials
load_dotenv("Secrets.env")

#Required Parameters:WATSONX API KEY, WATSONX URL, WATSONX PROJECT ID
creds = Credentials(
    api_key=os.environ["WATSONX_API_KEY"],
    url=os.environ["WATSONX_URL"],
)
project_id = os.environ["WATSONX_PROJECT_ID"]

# 2) Init client + pick a Granite model that’s enabled for your account
client = APIClient(credentials=creds, project_id=project_id)

params = {
    GenParams.MAX_NEW_TOKENS: 300,
    GenParams.TEMPERATURE: 0.2,     # low temp for more factual outputs
    GenParams.TOP_P: 0.9,
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",  # or another Granite instruct model you have access to
    params=params,
    credentials=creds,
    project_id=project_id,
)

# 3) Prompt: ask for concise, structured JSON
prompt = """
You are a science assistant. Provide a factual summary of the planet Mars.
Return ONLY strict JSON with these keys and SI units where applicable:

{
  "mean_surface_temperature_C": number,
  "min_temperature_C": number,
  "max_temperature_C": number,
  "atmosphere_composition": [{"gas": "CO2", "percent": number}, ...],
  "surface_gravity_m_s2": number,
  "day_length_hours": number,
  "year_length_days": number,
  "mean_radius_km": number,
  "average_sun_distance_AU": number,
  "moons": ["Phobos","Deimos"],
  "notes": "1–2 concise sentences"
}

Do not add any text before or after the JSON.
"""

res = model.generate(prompt=prompt)
#print(res)
text = res["results"][0]["generated_text"].strip()

# 4) Parse and print JSON
data = json.loads(text)
print(json.dumps(data, indent=2))