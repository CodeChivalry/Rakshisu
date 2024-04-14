import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import streamlit as st

# Retrieve secrets from environment variables
azure_key = os.environ['AZURE_KEY']
azure_endpoint = os.environ['AZURE_ENDPOINT']
azure_location = os.environ['AZURE_LOCATION']

# Authenticate the client using key, endpoint, and location
def authenticate_client():
    ta_credential = AzureKeyCredential(azure_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=azure_endpoint, 
            credential=ta_credential,
            location=azure_location)  
    return text_analytics_client

# Create the client instance
client = authenticate_client()

# Detecting sensitive information (PII) from text 
def pii_recognition(client, documents_array):
    response = client.recognize_pii_entities(documents_array, language="kn")
    result = [doc for doc in response if not doc.is_error]
    return result
