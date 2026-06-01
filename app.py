import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import google.generativeai as genai

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="BSc Management Student Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"
DEFAULT_API_KEY = "AQ.Ab8RN6KSEnxgUh1R98MZigwwsySa2gu9PpW4eWTWkR9GsDvNQA"

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin: {ADMIN_EMAIL}")

# Optional API Key override field
user_api_key = st.sidebar.text_input("Gemini API Key (Leave blank for default)", type="password")
ACTIVE_API_KEY = user_api_key if user_api_key else DEFAULT_API_KEY

page = st.sidebar.radio("Go to:", ["Dashboard", "AI Assistant", "News & Announcements", "Study Material", "Report Registration Issue"])

# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    st.markdown("""
        <div style="background: linear-gradient(to right, #2563eb, #4f46e5); color: white; padding: 30px; border-radius: 20px; margin-bottom: 25px;">
            <h1 style="margin: 0; color: white;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 5px; font-size: 16px;">
                Smart academic platform for study materials, notices, classroom access, and student issue management.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>Students</h3><h1 style="color: #2563eb; margin:0;">1,250</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Courses</h3><h1 style="color: #16a34a; margin:0;">18</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Notices</h3><h1 style="color: #ea580c; margin:0;">6</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Pending Issues</h3><h1 style="color: #dc2626; margin:0;">12</h1></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📚 Quick Overview: Connected Materials")
        materials = [
            {"subject": "Structural Geology", "teacher": "Dr. Sharma"},
            {"subject": "Mineralogy", "teacher": "Prof. Singh"},
            {"subject": "Engineering Mathematics", "teacher": "Dr. Verma"}
        ]
        for item in materials:
            with st.container():
                st.markdown(f"**{item['subject']}** — Teacher: {item['teacher']}")
                st.caption("🟢 Google Classroom Sync Active")
                st.divider()
                
    with right_col:
        st.subheader("⚡ Quick Access Controls")
        st.button("📋 Attendance Tracker", use_container_width=True)
        st.button("📝 Assignment Portal", use_container_width=True)
        st.button("📅 Academic Timetable", use_container_width=True)
        st.button("📊 Examination Results", use_container_width=True)

# --- PAGE: AI ASSISTANT (API KEY FIXED & ACTIVATED AS HELPER) ---
elif page == "AI Assistant":
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Ask me anything about your B.Sc Management subjects, academic syllabus, or Lucknow University rules.")
    
    try:
        # Configure using the determined active API key
        genai.configure(api_key=ACTIVE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask your helpful academic assistant..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Structured system contextual framing for helper response optimization
                    helper_context = (
                        "You are an empathetic, knowledgeable, and dedicated academic helper and counselor "
                        "for B.Sc Management students at Lucknow University. Provide actionable, supportive, "
                        f"and accurate answers to the student's request: {prompt}"
                    )
                    response = model.generate_content(helper_context)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"AI Assistant Initialization error. Please check your API key status. Details: {e}")

# --- PAGE: NEWS & ANNOUNCEMENTS ---
elif page == "News & Announcements":
    st.header("📢 Official Notices")
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Check for Latest Updates"):
        try:
            res = requests.get(lu_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            links = soup.find_all('a', href=True)
            found = 0
            for link in links:
                if "news" in link['href'] and len(link.text.strip()) > 15:
                    url = link['href'] if link['href'].startswith('http') else "https://www.lkouniv.ac.in" + link['href']
                    st.success(f"🔗 [{link.text.strip()}]({url})")
                    found += 1
                if found > 10: break
        except:
            st.error(f"Live feed unavailable. [Click here for LU News Site]({lu_url})")

# --- PAGE: STUDY MATERIAL ---
elif page == "Study Material":
    st.header("📚 Study Materials")
    st.write("Click the buttons below to access your Google Classrooms.")
    
    with st.container():
        st.subheader("BSc Management Core")
        st.info("Classroom Code: shf3hsat")
        st.link_button("Open Google Classroom", "
