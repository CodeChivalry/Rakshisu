import NotoSansKannada_CondensedBlack.ttf
#import gemini.py
import pii.py
import pandas as pd
import numpy as np
import streamlit as st
mob_details_variables_object = {
    "mob_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "mob_unit_name_mask": {
        "value": False,
        "maps_with_key": "Unit_Name"
    },

    "mob_name": {
        "value": False,
        "maps_with_key": "Name"
    },

    "mob_person_no": {
        "value": False,
        "maps_with_key": "Person_No"
    },

    "mob_mob_number": {
        "value": False,
        "maps_with_key": "MOB_Number"
    },

    "mob_mob_open_date": {
        "value": False,
        "maps_with_key": "MobOpenDate"
    },

    "mob_mob_open_year": {
        "value": False,
        "maps_with_key": "MOB_Open_Year"
    },

    "mob_arrested_by": {
        "value": False,
        "maps_with_key": "Arrested_By"
    },

    "mob_kgid": {
        "value": False,
        "maps_with_key": "KGID"
    },

    "mob_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "mob_grading": {
        "value": False,
        "maps_with_key": "Grading"
    },

    "mob_occupation": {
        "value": False,
        "maps_with_key": "Occupation"
    },

    "mob_ps_native": {
        "value": False,
        "maps_with_key": "PS_Native"
    },

    "mob_ps_district": {
        "value": False,
        "maps_with_key": "PS_District"
    },

    "mob_offender_class": {
        "value": False,
        "maps_with_key": "Offender_Class"
    },

    "mob_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "mob_actsection": {
        "value": False,
        "maps_with_key": "ActSection"
    },

    "mob_brief_fact": {
        "value": False,
        "maps_with_key": "Brief_Fact"
    },

    "mob_present_whereabouts": {
        "value": False,
        "maps_with_key": "Present_WhereAbouts"
    },

    "mob_gang_strength": {
        "value": False,
        "maps_with_key": "Gang_Strength"
    },

    "mob_ident_officer": {
        "value": False,
        "maps_with_key": "Ident_Officer"
    },

    "mob_officer_rank": {
        "value": False,
        "maps_with_key": "officer_rank"
    },

    "mob_crime_group1": {
        "value": False,
        "maps_with_key": "Crime_Group1"
    },

    "mob_crime_head2": {
        "value": False,
        "maps_with_key": "Crime_Head2"
    },

    "mob_class": {
        "value": False,
        "maps_with_key": "class"
    },

    "mob_age": {
        "value": False,
        "maps_with_key": "AGE"
    },

    "mob_present_age": {
        "value": False,
        "maps_with_key": "PresentAge"
    },

    "mob_dob": {
        "value": False,
        "maps_with_key": "DOB"
    },

    "mob_address": {
        "value": False,
        "maps_with_key": "Address"
    },

    "mob_sex": {
        "value": False,
        "maps_with_key": "SEX"
    },

    "mob_locality": {
        "value": False,
        "maps_with_key": "Locality"
    },

    "mob_last_updated_date": {
        "value": False,
        "maps_with_key": "LastUpdatedDate"
    }
}

# MOB DETAILS VARIABLES CLASS
class MOB_Details_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# INSTANCE OF MOB DETAILS VARIABLES CLASS
mob_details_variables = MOB_Details_Variables(mob_details_variables_object)

# EXAMPLE USAGE
mob_details_variables.set_mask_value("mob_district_name_mask", True)  # Modify value for "mob_district_name_mask"

#MOB FUNCTION
def process_mob_data(mob_df):
    mob_input = []
    mob_pii_output = []

    # Iterate through the rows
    for index in range(len(mob_df)):
        row_dict = mob_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            mob_row_detection = pii_recognition(client, row_chunk)
            mob_input.append(row_chunk)
            mob_pii_output.append(mob_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(mob_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(mob_details_variables_object.keys())[index]
                inner_dict = mob_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in mob_input for item in sublist]
    mob_input = combined_list
    mob_list = mob_input

    #GENERATE PDF
    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = mob_df.index[0]
        pdf.cell(200,10,txt="Sheet: MOBs Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(mob_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
            #gemini(pii_type,gem)
            st.write("Protection from further harm: Masking PII's of victims helps protect them from further victimization, harassment, or stalking.")
            st.write("Compliance with the Indian Evidence Act, 1872: Section 27 of the Indian Evidence Act allows for the production of evidence to rebut the presumption of innocence, but it also protects the privacy of victims.")
            gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(mob_details_variables.variables_object.keys())[mob_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(mob_details_variables.variables_object.keys())[mob_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name = mob_df.index[0]
        generate_pdf(all_masked_values, f"mob_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"mob_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

# MOB DETAILS PAGE
def mob_details_page():
    st.title("MOB Details")
    # Add content specific to MOB Details page
    # File uploader for CSV file
    st.write("Upload MOB Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select MOB ID
        if 'Mob_ID' in df.columns:
            mob_ids = df['Mob_ID'].unique()
            selected_mob = st.selectbox("MOB ID", mob_ids)
            
            # Find the row corresponding to the selected MOB ID
            selected_rows = df[df['Mob_ID'] == selected_mob]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                # Pass the row to process_mob_data function
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                process_mob_data(selected_row)
