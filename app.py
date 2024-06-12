import streamlit as st
import openai
import json
import os

# Initialize OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

openai_params = {
    "model": "gpt-4-1106-preview",
    "temperature": 0.7,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "max_tokens": 600,
    "top_p": 1
}

def file_description_prompt(text, jd):
    prompt = f"""### HR Evaluation of Candidate's Soft Skills

### Objective:
As an HR professional, your task is to meticulously assess a candidate's resume to ascertain their alignment with the job's soft skill requirements.
By providing a comprehensive evaluation, you will facilitate the selection of the most qualified candidate for the role. Soft skills depends on role-to-role individually but in general it includes team coordination, collaboration with team members, effective communication and proactive nature.

### Instructions:
- Thoroughly analyze the resume to determine the candidate's suitability based on the soft skills outlined in the job description.
- Focus solely on the soft skills mentioned in the job description and compare them to those listed or implied in the candidate's resume.
- Assign a match score from 0-100, reflecting the degree of alignment between the candidate's soft skills and the job requirements.
- You ONLY need to focus on soft skills and ignore the technical and educational background.

### Detailed Evaluation:
**Resume:** {text}
**Job Description:** {jd}

### Evaluation Output:
1. **Soft Skills Match Score:** Provide a score of 0-100 for the alignment of soft skills between the resume and the job description.
2. **Analysis and Justification:**
   - **Why Hire:** Offer reasons based on the evaluation for why the candidate's soft skills would be a strong match for the position.
   - **Why Not Hire:** Highlight any areas where the candidate's soft skills may not meet the job's expectations or the company's needs.

### Conclusion:
Utilize your HR expertise to conduct a thorough and unbiased review of the candidate's soft skills. 
This evaluation is essential for guiding the recruitment team's decision-making process, ensuring that we advance only the most fitting applicants for further consideration.
"""
    return prompt

def get_evaluation(resume_text, jd_text):
    prompt = file_description_prompt(resume_text, jd_text)
    message = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(messages=message, **openai_params)
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
