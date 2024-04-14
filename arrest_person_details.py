import NotoSansKannada_Condensed-Black.ttf
import gemini-1.0-pro-001.py
import pii-detection.py
import pandas as pd
import numpy as np
arrest_person_details_variables_object = {
    "apd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "apd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "apd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "apd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "apd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "apd_name": {
        "value": False,
        "maps_with_key": "Name"
    },

    "apd_age": {
        "value": False,
        "maps_with_key": "age"
    },

    "apd_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "apd_profession": {
        "value": False,
        "maps_with_key": "Profession"
    },

    "apd_sex": {
        "value": False,
        "maps_with_key": "Sex"
    },

    "apd_present_address": {
        "value": False,
        "maps_with_key": "PresentAddress"
    },

    "apd_present_city": {
        "value": False,
        "maps_with_key": "PresentCity"
    },

    "apd_present_state": {
        "value": False,
        "maps_with_key": "PresentState"
    },

    "apd_permanent_address": {
        "value": False,
        "maps_with_key": "PermanentAddress"
    },

    "apd_permanent_city": {
        "value": False,
        "maps_with_key": "PermanentCity"
    },

    "apd_permanent_state": {
        "value": False,
        "maps_with_key": "PermanentState"
    },

    "apd_nationality_name": {
        "value": False,
        "maps_with_key": "Nationality_Name"
    },

    "apd_dob": {
        "value": False,
        "maps_with_key": "DOB"
    },

    "apd_person_no": {
        "value": False,
        "maps_with_key": "Person_No"
    },

    "apd_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "apd_arr_id": {
        "value": False,
        "maps_with_key": "Arr_ID"
    },

    "apd_charge_sheeted": {
        "value": False,
        "maps_with_key": "Charge_Sheeted"
    },

    "apd_charge_sheet_number": {
        "value": False,
        "maps_with_key": "Charge_Sheet_Number"
    }
}

#ARREST PERSON DETAILS VARIABLES CLASS
class Arrest_Person_Details_Variables:
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

# INSTANCE OF ARREST PERSON DETAILS VARIABLES CLASS
arrest_person_details_variables = Arrest_Person_Details_Variables(arrest_person_details_variables_object)

# EXAMPLE USAGE
arrest_person_details_variables.set_mask_value("apd_district_name_mask", True)  # Modify value for "apd_district_name_mask"

# ARREST FUNCTION
def process_arrest_person_data(arrest_person_df):
    arrest_person_input = []
    arrest_person_pii_output = []

    # Iterate through the rows
    for index in range(len(arrest_person_df)):
        row_dict = arrest_person_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            arrest_person_row_detection = pii_recognition(client, row_chunk)
            arrest_person_input.append(row_chunk)
            arrest_person_pii_output.append(arrest_person_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(arrest_person_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(arrest_person_details_variables_object.keys())[index]
                inner_dict = arrest_person_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in arrest_person_input for item in sublist]
    arrest_person_input = combined_list
    arrest_person_list = arrest_person_input

    #GENERATE PDF
    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = arrest_person_df.index[0]
        pdf.cell(200,10,txt="Sheet: Arrest Person Details",align='C',ln=True)
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
    for i, string in enumerate(arrest_person_list):
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
             gemini(pii_type,gem)
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
            key = list(arrest_person_details_variables.variables_object.keys())[arrest_person_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(arrest_person_details_variables.variables_object.keys())[arrest_person_list.index(string)]
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
        index_name=arrest_person_df.index[0]
        generate_pdf(all_masked_values, f"arrest_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"arrest_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

# ARREST PERSON DETAILS PAGE
def arrest_person_details_page():
    st.title("Arrest Person Details")
    # Add content specific to Arrest Person Details page
    # File uploader for CSV file
    st.write("Upload Arrest Person Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Person ID
        if 'Person_ID' in df.columns:
            person_ids = df['Person_ID'].unique()
            selected_person = st.selectbox("Person ID", person_ids)
            
            # Find the row corresponding to the selected Person ID
            selected_rows = df[df['Person_ID'] == selected_person]
            
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
                # Pass the row to process_arrest_person_data function
                process_arrest_person_data(selected_row)
