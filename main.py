import pandas as pd
import streamlit as st
import numpy as np
import FIR_details.py
import MOB_details.py
import accident_reports.py
import accused_details.py
import arrest_person_details.py
import charge_sheeted_details.py
import complainant_details.py
import rowdy_sheeter.py
import victim_info_details.py
import time
import base64
from typing import Optional
from google.auth import credentials as auth_credentials
from google.cloud import aiplatform
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
def main():
    st.title("RAKSHISU")
    st.write("Choose the file types you want to work with:")

    # Define options for file types
    file_types = {
        "FIR Details": fir_details_page,
        "Rowdy Sheeter Details": rowdy_sheeter_details_page,
        "Arrest Person": arrest_person_details_page,
        "MOB Data": mob_details_page,
        "Victim Info Details": victim_info_details_page,
        "Complainant Details": complainant_details_page,
        "Charge Sheeted Details": charge_sheeted_details_page,
        "Accused Data": accused_details_page,
        "Accident Reports": accident_reports_page
    }

    # Multiselect widget to select file types
    selected_file_type = st.selectbox("", list(file_types.keys()))

    # Render selected file type pages
    # Render selected file type page
    file_types[selected_file_type]()

if __name__ == "__main__":
    main()
