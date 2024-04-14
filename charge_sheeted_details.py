#import gemini.py
import pii.py
import NotoSansKannada_CondensedBlack.ttf
import pandas as pd
import numpy as np
import streamlit as st

charge_sheeted_details_variables_object = {
    "csd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "csd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "csd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "csd_ri": {
        "value": False,
        "maps_with_key": "RI"
    },

    "csd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "csd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "csd_fir_date": {
        "value": False,
        "maps_with_key": "FIR_Date"
    },

    "csd_report_date": {
        "value": False,
        "maps_with_key": "Report_Date"
    },

    "csd_final_report_date": {
        "value": False,
        "maps_with_key": "Final_Report_Date"
    },

    "csd_report_type": {
        "value": False,
        "maps_with_key": "Report_Type"
    },

    "csd_fir_id": {
        "value": False,
        "maps_with_key": "FIR_ID"
    },

    "csd_unit_id": {
        "value": False,
        "maps_with_key": "Unit_ID"
    },

    "csd_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "csd_fr_id": {
        "value": False,
        "maps_with_key": "FR_ID"
    }
}

#CHARGE SHEETED DETAILS VARIABLES CLASS
class Charge_Sheeted_Details_Variables:
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

# INSTANCE OF CHARGE SHEETED DETAILS VARIABLES
charge_sheeted_details_variables = Charge_Sheeted_Details_Variables(charge_sheeted_details_variables_object)

# Example usage:
charge_sheeted_details_variables.set_mask_value("csd_district_name_mask", True)  # Modify value for "csd_district_name_mask"

#CHARGE FUNCTION
def process_charge_sheeted_data(charge_sheeted_df):
    charge_sheeted_input = []
    charge_sheeted_pii_output = []

    # Iterate through the rows
    for index in range(len(charge_sheeted_df)):
        row_dict = charge_sheeted_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            charge_sheeted_row_detection = pii_recognition(client, row_chunk)
            charge_sheeted_input.append(row_chunk)
            charge_sheeted_pii_output.append(charge_sheeted_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(charge_sheeted_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(charge_sheeted_details_variables_object.keys())[index]
                inner_dict = charge_sheeted_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in charge_sheeted_input for item in sublist]
    charge_sheeted_input = combined_list
    charge_sheeted_list = charge_sheeted_input

    #GENERATE PDF
    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = charge_sheeted_df.index[0]
        pdf.cell(200,10,txt="Sheet: Charge Sheeted Details",align='C',ln=True)
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
    for i, string in enumerate(charge_sheeted_list):
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
            key = list(charge_sheeted_details_variables.variables_object.keys())[charge_sheeted_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(charge_sheeted_details_variables.variables_object.keys())[charge_sheeted_list.index(string)]
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
        index_name=charge_sheeted_df.index[0]
        generate_pdf(all_masked_values, f"charge_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"charge_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

#CHARGE SHEETED DETAILS PAGE
def charge_sheeted_details_page():
    st.title("Charge Sheeted Details")
    # Add content specific to Charge Sheeted Details page
    # File uploader for CSV file
    st.write("Upload Charge Sheeted Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Crime No
        if 'Crime_No' in df.columns:
            crime_numbers = df['Crime_No'].unique()
            selected_crime = st.selectbox("Crime No.", crime_numbers)
            
            # Find the row corresponding to the selected Crime No
            selected_rows = df[df['Crime_No'] == selected_crime]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_charge_sheeted_data function
                process_charge_sheeted_data(selected_row)
