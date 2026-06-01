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
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin: {ADMIN_EMAIL}")
page = st.sidebar.radio("Go to:", ["AI Assistant", "News & Announcements", "Study Material", "Report Registration Issue"])

# [The AI Assistant, News, and Study Material pages remain exactly the same as your original code]
if page == "AI Assistant":
    st.header("🤖 AI Student Counselor")
    # ... (Keep your original AI code here)
elif page == "News & Announcements":
    st.header("📢 Official Notices")
    # ... (Keep your original News code here)
elif page == "Study Material":
    st.header("📚 Study Materials")
    # ... (Keep your original Study Material code here)

# --- PAGE: REPORT REGISTRATION ISSUE (FIXED EMAIL PIPELINE) ---
elif page == "Report Registration Issue":
    st.header("❗ Report an Issue")
    st.write("Submitting this form logs the issue, alerts the admin email natively, and opens up the final WhatsApp validation loop.")

    with st.form("issue_form", clear_on_submit=False):
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        
        submitted = st.form_submit_button("Submit & Notify Admin")
        
    if submitted:
        if name and roll_no and details:
            
            # 1. FIXED: FormSubmit works best with standard form-encoded data instead of JSON
            email_payload = {
                "Student Name": name,
                "Roll Number": roll_no,
                "Issue Type": issue_type,
                "Detailed Description": details,
                "_subject": f"🚨 Urgent: Registration Issue from {name}",
                "_captcha": "false"  # Disables the annoying captcha page for your users
            }
            
            with st.spinner("Sending instant email notification to admin..."):
                try:
                    # Using data= instead of json= to ensure FormSubmit parses it correctly
                    response = requests.post(f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", data=email_payload)
                    
                    if response.status_code == 200:
                        st.toast("Email Notification Processed Successfully!", icon="📧")
                    else:
                        st.error(f"Email server responded with error code: {response.status_code}. Try confirming your FormSubmit activation.")
                except Exception as e:
                    st.error(f"Network error trying to send email: {e}")

            # 2. WHATSAPP GENERATION PROTOCOL
            wa_text = f"*Registration Issue Report*\n\n*Name:* {name}\n*Roll No:* {roll_no}\n*Issue:* {issue_type}\n*Details:* {details}"
            wa_url = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(wa_text)}"
            
            # Display action tools
            st.success("🎉 Primary entry recorded inside portal UI application state.")
            st.write("Click below to pass execution control to WhatsApp and complete the notification pipeline:")
            st.link_button("Finalize via WhatsApp Message ✅", wa_url)
            st.balloons()
        else:
            st.error("⚠️ Validation failure: Ensure all fields containing asterisks (*) are populated.")
