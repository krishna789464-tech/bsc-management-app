import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CONFIGURATION & STYLING ---
# Target local logo image location dynamically across absolute paths securely
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"

# Fallback mechanism to keep the application from crashing if the file is moved or renamed
logo_exists = os.path.exists(LOGO_PATH)
if logo_exists:
    # Open the image using PIL for better compatibility with page_icon
    app_logo = Image.open(LOGO_PATH)
    page_icon_val = app_logo
else:
    app_logo = None
    page_icon_val = "🎓" # Fallback to a default emoji if path is missing

st.set_page_config(
    page_title="Company Dashboard",
    page_icon=page_icon_val,
    layout="wide"
)

# Custom Styling for App and Components
st.markdown("""
    <style>
    /* App background */
    .stApp { background-color: #f4f7f6; }
    
    /* Custom cards */
    .main-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    
    /* Professional Sidebar adjustments */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 10px;
    }
    .sidebar-meta {
        font-size: 13px;
        color: #4b5563;
        background-color: #f3f4f6;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }
    .sidebar-meta strong {
        color: #1f2937;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 2. PROFESSIONAL SIDEBAR NAVIGATION ---
# Top Logo Section
if logo_exists and app_logo:
    st.logo(LOGO_PATH) 
else:
    st.sidebar.markdown("<h2 style='margin-top: 0; color: #2563eb;'>🎓 Portal</h2>", unsafe_allow_html=True)

# System / Meta Info Block
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-meta">
        <strong>🏫 Academic System</strong><br>
        <span style="opacity: 0.85;">Role: Student Access</span><br>
        <hr style="margin: 8px 0; border: 0; border-top: 1px solid #d1d5db;">
        <strong>📧 Support Contact</strong><br>
        <a href="mailto:{ADMIN_EMAIL}" style="color: #2563eb; text-decoration: none;">{ADMIN_EMAIL}</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-weight: 600; font-size: 14px; margin-bottom: 5px; color:#4b5563;'>NAVIGATION</p>", unsafe_allow_html=True)

# Main Navigation using Streamlit Selectbox/Radio
page = st.sidebar.radio(
    label="Navigation Menu",
    options=["Dashboard", "AI Assistant", "News & Announcements", "Study Material", "Report Registration Issue"],
    label_visibility="collapsed"
)

# Optional Footer Info at bottom of Sidebar
st.sidebar.markdown("<vdiv style='flex:1;'></div>", unsafe_allow_html=True) # Spacer
st.sidebar.caption("v1.2.0 • Secure Session")


# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    st.title("Welcome to the Dashboard")
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

# --- PAGE: AI ASSISTANT (JOTFORMS EMBED) ---
elif page == "AI Assistant":
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Our automated academic agent is loading below. If it does not open automatically, please look for a chat icon on the screen.")
    
    jotform_script = """
    <script
      src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'>
    </script>
    """
    components.html(jotform_script, height=600, scrolling=True)

# --- PAGE: NEWS & ANNOUNCEMENTS ---
elif page == "News & Announcements":
    st.header("📢 Official Notices")
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Check for Latest Updates"):
        try:
            res = requests.get(lu_url, timeout=10)
            soup = BeautifulSoup(res.content, 'html.parser')
            links = soup.find_all('a', href=True)
            found = 0
            for link in links:
                if "news" in link['href'] and len(link.text.strip()) > 15:
                    clean_text = link.text.strip().replace("[", "").replace("]", "")
                    href_val = link['href']
                    url = href_val if href_val.startswith('http') else "https://www.lkouniv.ac.in" + href_val
                    st.success(f"🔗 [{clean_text}]({url})")
                    found += 1
                if found > 10: break
        except Exception:
            st.error(f"Live feed temporarily unavailable. [Click here for LU News Site]({lu_url})")

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
                "email": student_email.strip(),
                "Student Name": name.strip(),
                "Roll Number": roll_no.strip(),
                "Issue Type": issue_type,
                "Detailed Description": details.strip(),
                "_subject": f"🚨 Urgent: Registration Issue from {name.strip()}",
                "_captcha": "false"
            }
            
            with st.spinner("Processing form with target server..."):
                try:
                    response = requests.post(
                        f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", 
                        data=email_payload,
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.toast("Form processed! Email confirmation sent.", icon="📧")
                    else:
                        st.error(f"Endpoint verification issue encountered. Status Code: {response.status_code}")
                except Exception as e:
                    st.error("Automated transmission pipeline timeout. Proceeding to direct alternative routing.")

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
st.markdown("<center style='color: gray; font-size: 12px;'>Powered by Google Workspace and Microhnm Technologies</center>", unsafe_allow_html=True)
