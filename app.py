import streamlit as st
import openai
import json

# Initialize OpenAI API key
openai.api_key = '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'
openai_params = {"model":"gpt-4-1106-preview",
                 "temperature":0.7,
                 "frequency_penalty":0.0,
                 "presence_penalty":0.0,
                 "max_tokens":600,
                 "top_p":1}

def file_description_prompt(text, jd):
    prompt = f"""### HR Evaluation of Candidate's Resume

### Objective:
As an HR professional, your task is to meticulously assess a candidate's resume to ascertain their alignment with the job's requirements.
By providing a comprehensive evaluation, you will facilitate the selection of the most qualified candidate for the role.

### Instructions:
- Thoroughly analyze the resume to determine the candidate's suitability based on key criteria outlined in the job description,
including but not limited to skills, experiences, education, and personal attributes.
- Provide section wise scores for each of the resume and Job description pairs based on below parameters.
    i. Skills section in Resume < - > Skills required by the job description
    ii. Tools & Technologies section in Resume < - > Techstack section in job description
    iii. Professional Experience section in Resume < - > Seniority level and Experience required in job description
    iv. Education Degree and qualification section in Resume < - > Education and qualification required in Job description
    v. Extracurriculars and soft skills in Resume < - > Roles, Responsibilities and extra curriculars in job description
- Assign a match score from 1-100, reflecting the degree of alignment between the candidate's profile and the job requirements.

### Detailed Evaluation:
**Resume:** {text}
**Job Description:** {jd}

### Evaluation Output:
1. **Section-wise match score** Provide a score of 1-100 for each section like Education, Skills, Experience, Extra-curriculars and Techstack
1. **Match Score:** Provide a match score between 1 and 100, reflecting the candidate’s suitability for the position.
2. **Hiring Recommendations:**
   - **Why Hire:** Offer reasons based on the evaluation for why the candidate would be a strong match for the position.
   - **Why Not Hire:** Highlight any areas where the candidate may not meet the job's expectations or the company's needs.

### Conclusion:
Utilize your HR expertise to conduct a thorough and unbiased review of the candidate's qualifications.
This evaluation is essential for guiding the recruitment team's decision-making process, ensuring that we
advance only the most fitting applicants for further consideration.

"""
    return prompt

def get_evaluation(resume_text, jd_text):
    prompt = file_description_prompt(resume_text, jd_text)
    message = [{"role":"user","content":prompt}]
    response = openai.ChatCompletion.create(messages=message,
                                      **openai_params)
    return response.choices[0].message.content

# Streamlit App
st.title("Resume and Job Description Match Score")

# Input JSON files
resume_file = st.file_uploader("Upload Resume JSON", type=["json"])
jd_file = st.file_uploader("Upload Job Description JSON", type=["json"])

if resume_file and jd_file:
    resume_json = json.load(resume_file)
    jd_json = json.load(jd_file)
    
    resume_text = json.dumps(resume_json, indent=2)
    jd_text = json.dumps(jd_json, indent=2)

    st.subheader("Resume")
    st.text(resume_text)
    
    st.subheader("Job Description")
    st.text(jd_text)
    
    if st.button("Evaluate Match Score"):
        with st.spinner("Evaluating..."):
            evaluation = get_evaluation(resume_text, jd_text)
            st.subheader("Evaluation Output")
            st.text(evaluation)
