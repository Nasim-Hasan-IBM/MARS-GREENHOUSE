#Install
#pip install ibmcloudant
import os, json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
from ibm_cloud_sdk_core import ApiException

# 1. Load credentials
load_dotenv("Secrets.env")
CLOUDANT_API_KEY = os.environ["CLOUDANT_API_KEY"]
CLOUDANT_SERVICE_URL = os.environ["CLOUDANT_SERVICE_URL"]
CLOUDANT_DB = os.environ["CLOUDANT_DB"]
CLOUDANT_DOC_ID = os.environ["CLOUDANT_DOC_ID"]

# 2. Setup authenticator with your IBM Cloud API Key
authenticator = IAMAuthenticator(CLOUDANT_API_KEY)

# 3. Initialize the Cloudant client with your Service URL
client = CloudantV1(authenticator=authenticator)
client.set_service_url(CLOUDANT_SERVICE_URL)

try:
    # 4. Define the document content as a Python dictionary
    my_document = {
            "temperature (C)": -25,
            "humidity (%)": 55,
            "min. temperature (C)": -85,
            "mx. temperature (C)": 350
        }

    # 5. Insert the document into the database
    # This generates a unique server-side document ID automatically
    response = client.post_document(
            db=CLOUDANT_DB,
            document=my_document
        ).get_result()

    # 6. Output the successful result metadata
    print("Success! Document inserted.")
    print(json.dumps(response, indent=2))

#7. Capturing the Exceptions
except ApiException as ae:
    print(f"IBM Cloudant API exception occurred: {ae.code} - {ae.message}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# 8. Fetch a specific document from a database
response = client.get_document(db=CLOUDANT_DB, doc_id=CLOUDANT_DOC_ID)

document = response.get_result()
print(document)

