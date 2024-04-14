import time
import base64
from typing import Optional
from google.auth import credentials as auth_credentials
from google.cloud import aiplatform
import os
import streamlit as st

def init_sample(
    key: str,
    project_id: str,
    location: str,
    experiment: Optional[str] = None,
    staging_bucket: Optional[str] = None,
    credentials: Optional[auth_credentials.Credentials] = None,
    encryption_spec_key_name: Optional[str] = None,
    service_account: Optional[str] = None,
):

    # Initialize Google Cloud AI Platform
    aiplatform.init(
        project=project_id,
        location=location,
        experiment=experiment,
        staging_bucket=staging_bucket,
        credentials=credentials,
        encryption_spec_key_name=encryption_spec_key_name,
        service_account=service_account,
    )

# Retrieve environment variables for key, project_id, and location
project_id = os.environ['GEMINI_PROJECT_ID']
location = os.environ['GEMINI_LOCATION']
key = os.environ['GEMINI_KEY']

# Call the function with the variable values
init_sample(key, project_id, location)

import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def gemini(pii_type,i):
    button_key = f"generate_button_{i}"
    def generate(text1): 
        vertexai.init(project=project_id, location=location)
        model = generative_models.GenerativeModel("gemini-1.0-pro-001")
        
        generation_config = {
            "max_output_tokens": 1000,
            "temperature": 0.8,
            "top_p": 0.4,
            "top_k": 5,
        }

        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }
                
        responses = model.generate_content(
            [text1],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )
         
        return responses    

    # Button to generate response
    if st.button("Guidelines for PII Redaction", key=button_key):
        # Call the generate function with appropriate text1 value
        if pii_type == "Person":
            text1 = """Provide a general reason that necessitates the masking of name of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "PersonType":
            text1 = """Provide a general reason that necessitates the masking of job designation of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "PhoneNumber":
            text1 = """Provide a general reason that necessitates the masking of phone number of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "Organization":
            text1 = """Provide a general reason that necessitates the masking of district of victim's residential address.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "Address":
            text1 = """Provide a general reason that necessitates the masking of house address of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "Email":
            text1 = """Provide a general reason that necessitates the masking of email ID of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "IPAddress":
            text1 = """Provide a general reason that necessitates the masking of IPAddress.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "DateTime":
            text1 = """Provide a general reason that necessitates the masking of date and time of registration of complaint by victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "Quantity":
            text1 = """Provide a general reason that necessitates the masking of job designation of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        elif pii_type == "International Banking Account Number (IBAN)":
            text1 = """Provide a general reason that necessitates the masking of any banking credentials like credit card or debit card of victim.  Also cite any one legal law under the Indian Judicial System that supports it. Do not use markdown language. Use numbered list."""
        else:
            st.error("Invalid PII type selected.")
            return        
        result=generate(text1)
        for word in result:
            st.text(word.text)
