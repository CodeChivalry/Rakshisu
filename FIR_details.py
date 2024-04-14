import gemini.py
import pii-detection.py
import NotoSansKannada_Condensed-Black.ttf
import pandas as pd
import numpy as np
fir_details_data_variables_object = {
    "fd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "fd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "fd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "fd_ri": {
        "value": False,
        "maps_with_key": "RI"
    },

    "fd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "fd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "fd_offence_from_date": {
        "value": False,
        "maps_with_key": "Offence_From_Date"
    },

    "fd_offence_to_date": {
        "value": False,
        "maps_with_key": "Offence_To_Date"
    },

    "fd_fir_reg_datetime": {
        "value": False,
        "maps_with_key": "FIR_Reg_DateTime"
    },

    "fd_fir_date": {
        "value": False,
        "maps_with_key": "FIR_Date"
    },

    "fd_fir_type": {
        "value": False,
        "maps_with_key": "FIR Type"
    },

    "fd_fir_stage": {
        "value": False,
        "maps_with_key": "FIR_Stage"
    },

    "fd_complaint_mode": {
        "value": False,
        "maps_with_key": "Complaint_Mode"
    },

    "fd_crimegroup_name": {
        "value": False,
        "maps_with_key": "CrimeGroup_Name"
    },

    "fd_crimehead_name": {
        "value": False,
        "maps_with_key": "CrimeHead_Name"
    },

    "fd_latitude": {
        "value": False,
        "maps_with_key": "Latitude"
    },

    "fd_longitude": {
        "value": False,
        "maps_with_key": "Longitude"
    },

    "fd_actsection": {
        "value": False,
        "maps_with_key": "ActSection"
    },

    "fd_ioname": {
        "value": False,
        "maps_with_key": "IOName"
    },

    "fd_kgid": {
        "value": False,
        "maps_with_key": "KGID"
    },

    "fd_ioassigned_date": {
        "value": False,
        "maps_with_key": "IOAssigned_Date"
    },

    "fd_internal_io": {
        "value": False,
        "maps_with_key": "Internal_IO"
    },

    "fd_place_of_offence": {
        "value": False,
        "maps_with_key": "Place of Offence"
    },

    "fd_distance_from_ps": {
        "value": False,
        "maps_with_key": "Distance from PS"
    },

    "fd_beat_name": {
        "value": False,
        "maps_with_key": "Beat_Name"
    },

    "fd_village_area_name": {
        "value": False,
        "maps_with_key": "Village_Area_Name"
    },

    "fd_male": {
        "value": False,
        "maps_with_key": "Male"
    },

    "fd_female": {
        "value": False,
        "maps_with_key": "Female"
    },

    "fd_boy": {
        "value": False,
        "maps_with_key": "Boy"
    },

    "fd_girl": {
        "value": False,
        "maps_with_key": "Girl"
    },

    "fd_age_0": {
        "value": False,
        "maps_with_key": "Age 0"
    },

    "fd_victim_count": {
        "value": False,
        "maps_with_key": "VICTIM COUNT"
    },

    "fd_accused_count": {
        "value": False,
        "maps_with_key": "Accused Count"
    },

    "fd_arrested_male": {
        "value": False,
        "maps_with_key": "Arrested Male"
    },

    "fd_arrested_female": {
        "value": False,
        "maps_with_key": "Arrested Female"
    },

    "fd_arrested_count": {
        "value": False,
        "maps_with_key": "Arrested Count\tNo."
    },

    "fd_accused_chargesheeted_count": {
        "value": False,
        "maps_with_key": "Accused_ChargeSheeted Count"
    },

    "fd_conviction_count": {
        "value": False,
        "maps_with_key": "Conviction Count"
    },

    "fd_fir_id": {
        "value": False,
        "maps_with_key": "FIR_ID"
    },

    "fd_unit_id": {
        "value": False,
        "maps_with_key": "Unit_ID"
    },

    "fd_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    }
}

# FIR DETAILS DATA VARIABLES CLASS
class FIR_Details_Data_Variables:
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

# INSTANCE OF FIR DETAILS DATA VARIABLES CLASS
fir_details_data_variables = FIR_Details_Data_Variables(fir_details_data_variables_object)

# EXAMPLE USAGE
fir_details_data_variables.set_mask_value("fd_district_name_mask", True)  # Modify value for "fd_district_name_mask"

#FIR FUNCTION
def process_fir_details_data(fir_details_df):
    fir_details_input = []
    fir_details_pii_output = []

    # Iterate through the rows
    for index in range(len(fir_details_df)):
        row_dict = fir_details_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            fir_details_row_detection = pii_recognition(client, row_chunk)
            fir_details_input.append(row_chunk)
            fir_details_pii_output.append(fir_details_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(fir_details_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(fir_details_data_variables_object.keys())[index]
                inner_dict = fir_details_data_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in fir_details_input for item in sublist]
    fir_details_input = combined_list
    fir_details_list = fir_details_input

    #GENERATE PDF
    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = fir_details_df.index[0]
        pdf.cell(200,10,txt="Sheet: FIR Data Details",align='C',ln=True)
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
    for i, string in enumerate(fir_details_list):
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
            key = list(fir_details_data_variables.variables_object.keys())[fir_details_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(fir_details_data_variables.variables_object.keys())[fir_details_list.index(string)]
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
        index_name=fir_details_df.index[0]
        generate_pdf(all_masked_values, f"fir_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"fir_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

# FIR DETAILS PAGE
def fir_details_page():
    st.title("FIR Details")
    # Add content specific to FIR Details page
    # File uploader for CSV file
    st.write("Upload FIR Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select FIRNo
        if 'FIRNo' in df.columns:
            fir_numbers = df['FIRNo'].unique()
            selected_fir = st.selectbox("FIR No.", fir_numbers)
            
            # Find the row corresponding to the selected FIR Number
            selected_rows = df[df['FIRNo'] == selected_fir]
            
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
                # Pass the row to process_fir_details_data function
                process_fir_details_data(selected_row)
