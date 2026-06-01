import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

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

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin: {ADMIN_EMAIL}")
page = st.sidebar.radio("Go to:", ["Dashboard", "AI Assistant", "News & Announcements", "Study Material", "Report Registration Issue"])

# --- PAGE: DASHBOARD (Translated from React to Streamlit) ---
if page == "Dashboard":
    st.markdown("""
        <div style="background: linear-gradient(to right, #2563eb, #4f46e5); color: white; padding: 30px; border-radius: 20px; margin-bottom: 25px;">
            <h1 style="margin: 0; color: white;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 5px; font-size: 16px;">
                Smart academic platform for study materials, notices, classroom access, and student issue management.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Grid
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

# --- PAGE: AI ASSISTANT ---
elif page == "AI Assistant":
    st.header("🤖 AI Student Counselor")
    st.write("Ask questions about your management subjects or Lucknow University.")
    import google.generativeai as genai
    
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = model.generate_content(f"You are a BSc Management assistant for Lucknow University. Question: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    else:
        st.warning("Please enter your Gemini API Key in the sidebar to talk to the AI.")

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
        st.link_button("Open Google Classroom", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat")
    
    st.divider()
    st.write("More subjects will be added here soon.")

# --- PAGE: REPORT REGISTRATION ISSUE ---
elif page == "Report Registration Issue":
    st.header("❗ Report an Issue")
    st.write("Submitting this form logs your information, routes an email to the admin system, and builds your WhatsApp confirmation route.")

    with st.form("issue_form", clear_on_submit=False):
        student_email = st.text_input("Your Email Address *", placeholder="student@example.com")
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        
        submitted = st.form_submit_button("Submit & Notify Admin")
        
    if submitted:
        if student_email and name and roll_no and details:
            
            email_payload = {
                "email": student_email,
                "Student Name": name,
                "Roll Number": roll_no,
                "Issue Type": issue_type,
                "Detailed Description": details,
                "_subject": f"🚨 Urgent: Registration Issue from {name}",
                "_captcha": "false"
            }
            
            with st.spinner("Processing form with target server..."):
                try:
                    response = requests.post(f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", data=email_payload)
                    if response.status_code == 200:
                        st.toast("Form processed! Email confirmation sent.", icon="📧")
                    else:
                        st.error(f"Server rejected delivery. Status Code: {response.status_code}")
                except Exception as e:
                    st.error(f"Network error trying to contact the email relay: {e}")

            # 2. WHATSAPP GENERATION PROTOCOL
            wa_text = f"*Registration Issue Report*\n\n*Name:* {name}\n*Roll No:* {roll_no}\n*Email:* {student_email}\n*Issue:* {issue_type}\n*Details:* {details}"
            wa_url = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(wa_text)}"
            
            st.success("🎉 Local data entry recorded successfully!")
            st.write("Click below to pass execution control to WhatsApp and notify the Admin directly:")
            st.link_button("Finalize via WhatsApp Message ✅", wa_url)
            st.balloons()
        else:
            st.error("⚠️ Validation failure: Please fill out all required fields marked with (*).")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='color: gray; font-size: 12px;'>Powered by Google Workspace • MicroHNM Technologies</center>", unsafe_allow_html=True)
