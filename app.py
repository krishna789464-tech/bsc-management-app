import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="BSc Management Student Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- EMAIL CONFIGURATION SYSTEM ---
SMTP_SERVER = "smtp.gmail.com"  # Change this if not using Gmail (e.g., smtp.office365.com for Outlook)
SMTP_PORT = 587
SENDER_EMAIL = "your_system_email@gmail.com"   # The email account used to dispatch notifications
SENDER_PASSWORD = "your_app_password"          # The App Password generated for the system email
ADMIN_EMAIL = "krishna5689@outlook.in"         # The target admin inbox receiving alerts
ADMIN_PHONE = "919451134541"                   # WhatsApp Target Phone Number

def send_admin_email(student_name, roll_no, issue_type, details):
    """Handles SMTP connection secure delivery to the administrator."""
    try:
        # Setup MIME structures
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = ADMIN_EMAIL
        message["Subject"] = f"🚨 New Registration Issue from {student_name}"

        # Formulate Email Text Body
        body = f"""
Dear Admin,

A new registration issue has been flagged on the Student Portal.

[STUDENT DETAILS]
--------------------------------------
Name: {student_name}
Roll Number / ID: {roll_no}
Issue Category: {issue_type}

[DESCRIPTION]
--------------------------------------
{details}

Please take appropriate action.

Best regards,
Student Hub Automation Engine
        """
        message.attach(MIMEText(body, "plain"))

        # Connect, upgrade security protocols, and transmit
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        return False

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin Liaison: {ADMIN_EMAIL}")
page = st.sidebar.radio("Go to:", ["AI Assistant", "News & Announcements", "Study Material", "Report Registration Issue"])

# --- PAGE: AI ASSISTANT ---
if page == "AI Assistant":
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

# --- PAGE: REGISTRATION ISSUES (EMAIL & WHATSAPP INTEGRATION) ---
elif page == "Report Registration Issue":
    st.header("❗ Report an Issue")
    st.write("Submitting this form will silently alert the admin via automated email and generate your custom WhatsApp submission link.")

    with st.form("issue_form", clear_on_submit=False):
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        
        submitted = st.form_submit_button("Submit & Process Notifications")
        
    if submitted:
        if name and roll_no and details:
            with st.spinner("Processing your report and updating admin via email..."):
                # Run the backend email function
                email_sent = send_admin_email(name, roll_no, issue_type, details)
            
            if email_sent:
                st.toast("Email notice sent directly to Admin inbox!", icon="📧")
            else:
                st.error("Admin Email pipeline failed, but you can still proceed to complete it manually using the WhatsApp step below.")
            
            # Formulate the WhatsApp string URL format
            wa_text = f"*Registration Issue Report*\n\n*Name:* {name}\n*Roll No:* {roll_no}\n*Issue:* {issue_type}\n*Details:* {details}"
            wa_url = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(wa_text)}"
            
            st.success("🎉 Registration problem logged successfully into the portal system!")
            st.write("Please click the confirmation link below to finalize the submission to your admin's mobile device directly.")
            st.link_button("Finalize Submission on WhatsApp ✅", wa_url)
            st.balloons()
        else:
            st.error("⚠️ All fields marked with (*) are strict requirements. Please populate them before submitting.")
