from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input, pdf_content,prompt):
  model=genai.GenerativeModel('gemini-1.5-flash')
  response=model.generate_content([input,pdf_content[0],prompt])
  return response.text

def input_pdf_setup(uploaded_file):
  if uploaded_file is not None:
    #convert the pdf to image
    Images=pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r"C:\Program Files (x86)\poppler\Library\bin")

    first_page=Images[0]

    #convert to bytes
    img_byte_arr=io.BytesIO()
    first_page.save(img_byte_arr,format='JPEG')
    img_byte_arr=img_byte_arr.getvalue()

    pdf_parts=[
      {
        "mime_type":"image/jpeg",
        "data":base64.b64encode(img_byte_arr).decode()
      }
    ]
    return pdf_parts
  else:
    raise FileNotFoundError("No file upload")
  
#streamlit app

st.set_page_config(page_title="ATS Resune EXpert")
st.header("ATS Tracker System")
input_text=st.text_area("Job Description:",key="input")
upload_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if upload_file is not None:
  st.write("PDF Uploaded Successfully")

submit1=st.button("Tell Me About The Resume")

#submit2=st.button("How Can I Improvise My Skill")

submit3=st.button("Percentage Match")

input_prompt1="""
You are an experienced HR with Tech Experience in the field of Data Science, Full stack web development,Big data Engineering, DEVOPS, Data Analyst,your task is to review the provided resume against thejob description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with this roles.
Highlight the strenths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3="""
You are a skilled ATS(Applicant Tracking System) scanner with a deep understanding of Data science and ATS full stack Web development ,Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality.
Your task is to evaluate  the resume against the provided job description, give me the percentage match if the resume matchs job description. First the output should come as percentage and then keywords missing and last final thougths.
"""

if submit1:
  if upload_file is not None:
    pdf_content=input_pdf_setup(upload_file)
    response=get_gemini_response(input_prompt1,pdf_content,input_text)
    st.subheader("The Response is")
    st.write(response)
  
  else:
    st.write("Please upload the resume")

elif submit3:
  if upload_file is not None:
    pdf_content=input_pdf_setup(upload_file)
    response=get_gemini_response(input_prompt3,pdf_content,input_text)
    st.subheader("The Response is")
    st.write(response)
  
  else:
    st.write("Please upload the resume")
