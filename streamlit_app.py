import streamlit as st
from core.parse import read_file
from core.skills import load_skills, extract_skills
from core.score import rubric_score
from core.rewrite import suggest_additions


st.set_page_config(page_title='Career Copilot', layout='wide')


st.title('Career Copilot — Resume vs Job Match')
col1, col2 = st.columns(2)


skills = load_skills()
resume_text = ''
jd_text = ''


with col1:
uploaded = st.file_uploader('Upload your resume (PDF/DOCX)', type=['pdf','doc','docx'])
if uploaded:
with open('tmp_resume', 'wb') as f:
f.write(uploaded.read())
resume_text = read_file('tmp_resume')
st.text_area('Resume (extracted)', resume_text, height=250)


with col2:
jd_text = st.text_area('Paste Job Description', height=320)


if st.button('Analyze') and resume_text and jd_text:
jd_sk = set(extract_skills(jd_text, skills))
res_sk = set(extract_skills(resume_text, skills))
missing = jd_sk - res_sk
score = rubric_score(resume_text, jd_text, jd_sk, res_sk)


st.subheader(f'Match Score: {score}/100')
st.progress(score/100)


st.markdown('**Skills found in JD:** ' + ', '.join(sorted(jd_sk)))
st.markdown('**Skills present in resume:** ' + ', '.join(sorted(res_sk)) )
st.markdown('**Missing skills to address:** ' + (', '.join(sorted(missing)) or 'None'))


st.markdown('---')
st.markdown('### Suggested additions for your resume')
for s in suggest_additions(missing):
st.write('- ' + s)
