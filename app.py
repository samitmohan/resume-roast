import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import re


gemini_api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=gemini_api_key)

def read_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def gemini_response(resume_text, mode="Roast"):
    model = genai.GenerativeModel("gemini-1.5-flash") 

    intro_roast = "You are a grizzled engineering hiring manager known for brutally honest, line-by-line feedback."
    intro_review = "You are a seasoned career coach with deep expertise in technical hiring."
    ats_text = "ATS compatibility score"

    if mode == "Roast":
        prompt = f"""
{intro_roast}
For each bullet or sentence in this resume:
1. Call out the problem bluntly (tone: witty, gen-z, sarcastic, and a bit mocking).
2. Immediately follow with a one-sentence tip on how to fix it.
3. Keep each point under 40 words.

At the end, provide a 2–3-bullet “Overall Takeaway” summarizing the top improvements.
Also include an {ats_text} (0–100) with a brief rationale.

Resume Text:
{resume_text}
"""
    else:
        prompt = f"""
{intro_review}
Review this resume and for each section (Professional Summary, Experience, Education, Skills) provide:
1. A Section Summary.
2. What’s Working (2–3 strengths).
3. What’s Missing or Weak (2–3 actionable critiques).
4. Concrete Improvements (exact phrasing or formatting examples).

At the end, provide a 2–3-bullet “Overall Takeaway” summarizing the top improvements.
Also include an {ats_text} (0–100) with a brief rationale.
Be concise—no more than 150 words per section—and focus on clarity, ATS-friendliness, impact, and readability.

Resume Text:
{resume_text}
"""

    response = model.generate_content(prompt)
    return response.text

st.set_page_config(page_title="Resume Bot", layout="centered")
st.markdown('<h1 class="custom-title">Resume Bot</h1>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;700&display=swap');
    :root {
      --bg: #ffffff;
      --fg: #000000;
      --accent: #1e90ff;
      --font: 'Jost', sans-serif;
      --secondary-bg: #f5f5f5;
    }
    body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], header, section[data-testid="stToolbar"] {
      background-color: var(--bg) !important;
      color: var(--fg) !important;
      font-family: var(--font) !important;
    }
    .custom-title, .stHeader {
      font-family: var(--font) !important;
      font-weight: 300 !important;
      color: var(--accent) !important;
      text-align: center !important;
    }
    /* Style all buttons */
    button {
      background-color: var(--accent) !important;
      color: #000000 !important;
      font-size: 1.25rem !important;
      padding: 0.75rem 1.5rem !important;
      border-radius: 8px !important;
      width: 200px !important;
    }
    /* Ensure all Streamlit buttons use black text */
    .stButton > button, button {
      color: #000000 !important;
    }
    .stFileUploader button {
      width: 200px !important;
    }
    input[type="text"], textarea, div[role="combobox"] > div {
      background-color: var(--secondary-bg) !important;
      color: var(--fg) !important;
    }
    input[type="text"]::placeholder, textarea::placeholder {
      color: rgba(0,0,0,0.6) !important;
    }
    /* Sidebar main separator */
    [data-testid="stSidebar"] {
      border-right: 2px solid rgba(0,0,0,0.3) !important;
      position: sticky !important;
      top: 0;
      height: 100vh;
      overflow-y: auto !important;
    }
    /* Add padding to main content for visual separation */
    [data-testid="stAppViewContainer"] {
      padding-left: 1rem !important;
    }
    /* Remove excessive spacing */
    .css-1d391kg, .css-1v3fvcr, form {
      padding: 0.5rem !important;
      margin-bottom: 1rem !important;
    }
    /* Card shadows for uploader and feedback container */
    .css-1d391kg, .css-1v3fvcr, .stFileUploader > div, .stTextArea {
      box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
    }
    /* Uploader styling */
    .stFileUploader > div {
      background-color: var(--secondary-bg) !important;
      border: 1px solid rgba(0,0,0,0.3) !important;
      border-radius: 8px;
      padding: 1rem;
    }
    .stFileUploader label {
      color: var(--fg) !important;
    }
    /* ATS score styling */
    .ats-score {
      font-size: 2rem !important;
      color: var(--accent) !important;
      font-weight: 300 !important;
      margin-top: 1rem;
    }
    /* Uploader placeholder text and icons in drop area */
    .stFileUploader p, 
    .stFileUploader div p {
      color: #111111 !important;
    }
    .stFileUploader svg {
      fill: #111111 !important;
    }
    /* Improve line-height and constrain feedback width */
    .stMarkdown {
      line-height: 1.6 !important;
      max-width: 60ch !important;
      margin: 0 auto !important;
    }
    /* Subtle separator under section headings */
    .stMarkdown h3 {
      border-bottom: 1px solid rgba(0,0,0,0.1) !important;
      padding-bottom: 0.25rem !important;
    }
    /* Hover underline on headings */
    .stMarkdown h3:hover {
      text-decoration: underline;
      cursor: pointer;
    }
    button:focus, input:focus, textarea:focus, select:focus {
      outline: 2px solid var(--accent) !important;
      outline-offset: 2px !important;
    }
    /* Fix Cloud uploader to light background + dark text */
    /* Container wrapper */
    [data-testid="file-uploader-container"] > div {
    background-color: var(--secondary-bg) !important;  /* your #f5f5f5 */
    border-color: rgba(0,0,0,0.1) !important;
    }
    /* Inner drag/drop zone */
    [data-testid="upload-droppable"] {
    background-color: var(--secondary-bg) !important;
    }
    /* Make sure all placeholder text & icons inside are dark */
    [data-testid="upload-droppable"] *,
    [data-testid="file-uploader-container"] p,
    [data-testid="file-uploader-container"] svg {
    color: var(--fg) !important;  /* your #000 */
    fill: var(--fg) !important;
    }
    /* Style the Browse button in the uploader */
    [data-testid="file-uploader-container"] button {
    background-color: var(--accent) !important;
    color: var(--fg) !important;
    min-width: 200px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    mode = st.radio("Mode", ["Roast", "Review"], index=0)

mode_text = "Roast" if "Roast" in mode else "Review"

with st.form("resume_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Drop your resume here (PDF)", type=["pdf"])
    submit = st.form_submit_button("Roast Me" if mode_text=="Roast" else "Review Me")

if submit and uploaded_file:
    with st.spinner("Reading your resume..."):
        resume_text = read_pdf(uploaded_file)

    with st.spinner("Hold on, the wrapper of a wrapper is currently at work..."):
        response = gemini_response(resume_text, mode=mode_text)

    st.markdown("---")

    # parse response into main feedback, overall takeaways, and ATS score
    main_part = response
    takeaway = ""
    ats = ""
    if "**Overall Takeaway:**" in response:
        main_part, rest = response.split("**Overall Takeaway:**", 1)
        if "**ATS Compatibility Score:**" in rest:
            takeaway, ats_part = rest.split("**ATS Compatibility Score:**", 1)
            ats = ats_part.strip()
        else:
            takeaway = rest.strip()

    st.markdown("### Feedback")
    st.markdown(main_part, unsafe_allow_html=True)

    # render overall takeaways separately
    if takeaway:
        st.markdown("### Overall Takeaway")
        # Parse bullets and render as HTML list
        items = [
            line.strip().lstrip("* ").strip()
            for line in takeaway.strip().splitlines()
            if line.strip()
        ]
        list_html = "<ul style='margin:0; padding-left:1.5rem;'>"
        for item in items:
            list_html += f"<li>{item}</li>"
        list_html += "</ul>"
        st.markdown(
            f"<div style=\"background-color: var(--secondary-bg); border-left: 4px solid var(--accent); padding:1rem; border-radius:4px;\">{list_html}</div>",
            unsafe_allow_html=True
        )

    # split ATS score into number and rationale : re magic
    score_text = ats
    rationale = ""
    if ats:
        m = re.match(r"\s*([0-9]{1,3}/100)\s*(.*)", ats)
        if m:
            score_text = m.group(1)
            rationale = m.group(2).strip()

    if rationale.lower().startswith("rationale:"):
        rationale = rationale.split(":", 1)[1].strip()
    # Clean any remaining leading 'Rationale:' text
    rationale = re.sub(r'^[Rr]ationale:\s*', '', rationale)

    if ats:
        st.metric(label="ATS Compatibility Score", value=score_text)
        if rationale:
            st.markdown(f"**Rationale:** {rationale}")
