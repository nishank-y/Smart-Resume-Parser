import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.extractor import extract_text
from parser.nlp_parser import parse_resume
from parser.utils import save_json, save_csv

st.set_page_config(page_title="Resume Parser", layout="centered")

st.title("Resume Parser")
st.write("Upload one or more resumes (PDF, DOCX, or TXT) to extract Name, Contact, Education, and Skills.")

uploaded_files = st.file_uploader(
    "Choose one or more files", type=["pdf","docx","txt"], accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    all_parsed_data = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join("resumes", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"{uploaded_file.name} uploaded successfully!")

        text = extract_text(file_path)
        parsed_data = parse_resume(text)
        parsed_data["Filename"] = uploaded_file.name  
        all_parsed_data.append(parsed_data)

    st.subheader("Parsed Resume Data")
    st.json(all_parsed_data)

    json_path = os.path.join("output", "all_resumes.json")
    csv_path = os.path.join("output", "all_resumes.csv")
    save_json(all_parsed_data, json_path)
    save_csv(all_parsed_data, csv_path)

    st.download_button(
        "Download JSON",
        data=open(json_path, 'rb').read(),
        file_name="all_resumes.json"
    )
    st.download_button(
        "Download CSV",
        data=open(csv_path, 'rb').read(),
        file_name="all_resumes.csv"
    )
