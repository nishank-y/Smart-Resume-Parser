# Smart Resume Parser
- A Streamlit-based resume parser that extracts Name, Email, Phone Number, Education, Skills, and Experience from resumes in PDF, DOCX formats.  
- This project uses NLP (spaCy) and Regex to process resumes and outputs structured data in JSON/CSV formats.  

# Features
- Extracts:
  - Name
  - Email
  - Phone Number
  - Education
  - Skills
  - Experience
- Interactive Streamlit UI
- Supports multiple file formats (PDF, DOCX)
- Handles multiple resumes at once
- Saves parsed output in JSON and CSV
- Easy to integrate into larger applications

# Tools & Libraries Used
- Python 3
- Streamlit (UI)
- spaCy (for NLP-based name/entity extraction)
- PyPDF2/python-docx (for text extraction)
- Regex(re) for email/phone extraction
- pandas (for saving CSV files)

# Run the script
- streamlit run ui/app.py
