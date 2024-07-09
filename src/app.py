import streamlit as st
import os
from controls import save_uploaded_file, Extract_text_from_pdf_Tesseract,Text_process,retrieve_information,extract_kpis
from langchain_community.llms import Cohere
from langchain_google_genai import GoogleGenerativeAI
from dotenv import dotenv_values
from fpdf import FPDF


env_values = dotenv_values(".env")
cohere_api_key = env_values['COHERE_API_KEY']
Gimni_API_KEY = env_values['Gimni_API_KEY']
Cohere_llm=Cohere(cohere_api_key=cohere_api_key,temperature=0.5)
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=Gimni_API_KEY,temperature=0.5)

# Initialize variables in session state
if "file_path" not in st.session_state:
    st.session_state.file_path = None
if "pdf_folder" not in st.session_state:
    st.session_state.pdf_folder = None
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "all_text" not in st.session_state:
    st.session_state.all_text = None


# Upload button

st.sidebar.title("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if st.sidebar.button("Upload"):
    with st.spinner('Uploading...'):
        if uploaded_file is not None:
            st.session_state.file_path, st.session_state.pdf_folder, st.session_state.pdf_name = save_uploaded_file(uploaded_file)
            if st.session_state.file_path and st.session_state.pdf_folder:
                all_text_file_path ,st.session_state.all_text= Extract_text_from_pdf_Tesseract(st.session_state.file_path, st.session_state.pdf_folder)
                st.session_state.vector_db = Text_process(st.session_state.all_text, st.session_state.pdf_name)
                st.sidebar.success(f"Uploaded {uploaded_file.name}")
        else:
            st.sidebar.error("Please upload a PDF file")



# Analyze button
st.title("PDF Analysis")
question = st.text_input("Ask a question about the PDF content:")

if st.button("Analyze"):
    with st.spinner('Analyzing...'):
        if uploaded_file is not None:
            if st.session_state.vector_db:
                if question:
                    result = retrieve_information(llm, st.session_state.vector_db, question)
                    st.write(f"Answer: {result['output_text']}")
                else:
                    st.error("Please ask a question")
            else:
                st.error("Vector database not defined. Please upload a PDF first.")
        else:
            st.error("Please upload a PDF file")






# Function to update text with new KPIs
def update_text_with_kpis(text, original_kpi, updated_kpi):
    return text.replace(original_kpi, updated_kpi)


# Extract KPIs button 
if st.button("Extract KPIs"):
    with st.spinner('Extracting...'):
        if st.session_state.vector_db:
            
        
            st.session_state.kpis=extract_kpis(st.session_state.pdf_name ,llm)
            
            st.success("KPIs extracted successfully.")
        else:
            st.error("Please upload a PDF first.")



# Display and update KPIs
if "kpis" in st.session_state:

    if "kpis" in st.session_state:
        st.title("Update KPI Values")
        
        st.write("### Original KPIs and Contexts")
        for kpi in st.session_state.kpis:
            st.write(f"**Context**: {kpi['context']}")
            st.write(f"**Original KPI**: {kpi['KPI']}")
            st.write("---")


    st.write("### Update KPI Values")
    updated_kpis = []
    
    original_value = st.text_input(f"Original KPI: ")
    updated_value = st.text_input(f"Update KPI: ")
    


    if st.button("Update KPIs in Document"):
        with st.spinner('Updating...'):
            if original_value and updated_value:
                updated_kpis={"original": original_value, "updated": updated_value}
                st.session_state.updated_kpis = updated_kpis
            else:
                st.error("Please add  Original KPI and Update KPI ")
        
            if "updated_kpis" in st.session_state:
                all_text_content = st.session_state.all_text  
                
                all_text_content = update_text_with_kpis(all_text_content, st.session_state.updated_kpis["original"], st.session_state.updated_kpis["updated"])
            
                st.write("### Updated Text:")
                st.write(all_text_content)
                
                # with open(output_pdf_path, "rb") as file:
                #     btn = st.download_button(
                #         label="Download Updated PDF",
                #         data=file,
                #         file_name="updated_document.pdf",
                #         mime="application/pdf"
                #     )
            else:
                st.error("No KPIs to update.")