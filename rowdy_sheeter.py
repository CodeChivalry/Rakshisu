import gemini.py
import pii.py
import NotoSansKannada_Condensed-Black.ttf
import pandas as pd
import numpy as np
import streamlit as st

rowdy_sheeter_variables_object = {
    "rs_district_name_mask" : {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "rs_unit_name_mask": {
        "value": False,
        "maps_with_key": "Unit_Name"
    },

    "rs_rowdy_sheet_no_mask" : {
        "value": False,
        "maps_with_key": "Rowdy_Sheet_No"
    },

    "rs_name" : {
        "value": False,
        "maps_with_key": "Name"
    },

    "rs_alias_name" : {
        "value": False,
        "maps_with_key": "AliasName"
    },

    "rs_open_date" : {
        "value": False,
        "maps_with_key": "RS_Open_Date"
    },

    "rs_rowdy_classification_details" : {
        "value": False,
        "maps_with_key": "Rowdy_Classification_Details"
    },

    "rs_activities_description" : {
        "value": False,
        "maps_with_key": "Activities_Description"
    },

    "rs_rowdy_category" : {
        "value": False,
        "maps_with_key": "Rowdy_Category"
    },

    "rs_prev_case_details" : {
        "value": False,
        "maps_with_key": "PrevCase_Details"
    },

    "rs_address" : {
        "value": False,
        "maps_with_key": "Address"
    },

    "rs_age" : {
        "value": False,
        "maps_with_key": "Age"
    },

    "rs_father_name" : {
        "value": False,
        "maps_with_key": "Father_Name"
    },

    "rs_source_of_income" :{
        "value": False,
        "maps_with_key": "Source_Of_Income"
    },

    "rs_last_updated_date" : {
        "value": False,
        "maps_with_key": "LastUpdatedDate"
    },

    "rs_present_whereabout" : {
        "value": False,
        "maps_with_key": "PresentWhereabout"
    }
}
# ROWDYSHEETERVARIABLES CLASS
class RowdySheeterVariables:
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

# INSTANCE OF ROWDYSHEETERVARIABLES CLASS
rowdy_sheeter_variables = RowdySheeterVariables({
"rs_district_name_mask" : {
 "value": False,
 "maps_with_key": "District_Name"
},
"rs_unit_name_mask": {
        "value": False,
        "maps_with_key": "Unit_Name"
},

    "rs_rowdy_sheet_no_mask" : {
        "value": False,
        "maps_with_key": "Rowdy_Sheet_No"
},

    "rs_name" : {
        "value": False,
        "maps_with_key": "Name"
},

    "rs_alias_name" : {
        "value": False,
        "maps_with_key": "AliasName"
},

    "rs_open_date" : {
        "value": False,
        "maps_with_key": "RS_Open_Date"
},

    "rs_rowdy_classification_details" : {
        "value": False,
        "maps_with_key": "Rowdy_Classification_Details"
},

    "rs_activities_description" : {
        "value": False,
        "maps_with_key": "Activities_Description"
},

    "rs_rowdy_category" : {
        "value": False,
        "maps_with_key": "Rowdy_Category"
},

    "rs_prev_case_details" : {
        "value": False,
        "maps_with_key": "PrevCase_Details"
},

    "rs_address" : {
        "value": False,
        "maps_with_key": "Address"
},

    "rs_age" : {
        "value": False,
        "maps_with_key": "Age"
},

    "rs_father_name" : {
        "value": False,
        "maps_with_key": "Father_Name"
},

    "rs_source_of_income" :{
        "value": False,
        "maps_with_key": "Source_Of_Income"
},

    "rs_last_updated_date" : {
        "value": False,
        "maps_with_key": "LastUpdatedDate"
},

    "rs_present_whereabout" : {
        "value": False,
        "maps_with_key": "PresentWhereabout"
}
})

# EXAMPLE USAGE
rowdy_sheeter_variables.set_mask_value("rs_district_name_mask", True) # Modify value for "rs_district_name_mask"

# ROWDY FUNCTION
def process_rowdy_sheeter_data(rowdy_sheeter_df):
    rowdy_sheeter_input = []
    rowdy_sheeter_pii_output = []
    #print(rowdy_sheeter_df)
    # Iterate through the rows
    row_dict=None
    for index in range(len(rowdy_sheeter_df)):
        row_dict = rowdy_sheeter_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            rowdy_sheeter_row_detection = pii_recognition(client, row_chunk)
            rowdy_sheeter_input.append(row_chunk)
            rowdy_sheeter_pii_output.append(rowdy_sheeter_row_detection)

    for index, result in enumerate(rowdy_sheeter_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(rowdy_sheeter_variables_object.keys())[index]
                inner_dict = rowdy_sheeter_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue


    combined_list = [item for sublist in rowdy_sheeter_input for item in sublist]

    rowdy_sheeter_input=combined_list

    rowdy_sheeter_list=rowdy_sheeter_input

    # PDF GENERATION

    from fpdf import FPDF
    import base64
    import os
    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        #index_name = rowdy_sheeter_df.index[0]
        index_name = rowdy_sheeter_df.index[0]
        pdf.cell(200,10,txt="Sheet: Rowdy Sheeter Details",align='C',ln=True)
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

    # Iterate over each index in the input data
    gem=1
    for i, string in enumerate(rowdy_sheeter_list):
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
            # Add action dropdown for PII detection
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            # Prompt user for masking preference for the string
            # Apply masking only if the user wants to mask the detected PII
            if action == "Mask":
                # Mask the string with asterisks if PII is detected
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            # Get the corresponding key based on the index
            key = list(rowdy_sheeter_variables.variables_object.keys())[rowdy_sheeter_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(rowdy_sheeter_variables.variables_object.keys())[rowdy_sheeter_list.index(string)]

            # Store original value along with the corresponding key
            all_masked_values.append((key, string))


    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:

        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values=unique_tuples

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
        index_name = rowdy_sheeter_df.index[0]
        generate_pdf(all_masked_values, f"rowdy_{index_name}.pdf")
        st.write("PDF exported successfully!")

    # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"rowdy_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True) 

# ROWDYSHEETER PAGE
def rowdy_sheeter_details_page():
    st.title("Rowdy Sheeter Details")
    # Add content specific to Rowdy Sheeter Details page
    # File uploader for CSV file
    st.write("Upload Rowdy Sheeter CSV file:")
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
        if 'Rowdy_Sheet_No' in df.columns:
            fir_numbers = df['Rowdy_Sheet_No'].unique()
            selected_fir = st.selectbox("Rowdy Sheet No.", fir_numbers)
            
            # Find the rows corresponding to the selected FIR Number
            selected_rows = df[df['Rowdy_Sheet_No'] == selected_fir]
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
                    
                # Pass the row to rowdysheeter_piidetect function
                process_rowdy_sheeter_data(selected_row)
