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

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info("Admin: krishna5689@outlook.in")
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
            st.error("Live feed unavailable. [Click here for LU News Site]("+lu_url+")")

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

# --- PAGE: REGISTRATION ISSUES (WITH WHATSAPP & EMAIL) ---
elif page == "Report Registration Issue":
    st.header("❗ Report an Issue")
    st.write("Submitting this form will notify the admin via Email and redirect you to WhatsApp.")

    with st.form("issue_form", clear_on_submit=True):
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        
        submitted = st.form_submit_button("Submit & Notify Admin")
        
        if submitted:
            if name and roll_no and details:
                # 1. PREPARE DATA
                admin_email = "krishna5689@outlook.in"
                admin_phone = "919451134541"
                
                # 2. TRIGGER EMAIL NOTIFICATION (Using FormSubmit.co API)
                email_payload = {
                    "Name": name,
                    "RollNo": roll_no,
                    "Issue": issue_type,
                    "Details": details,
                    "_subject": f"New Registration Issue from {name}"
                }
                try:
                    requests.post(f"https://formsubmit.co/ajax/{admin_email}", data=email_payload)
                    st.toast("Email Notification Sent to Admin!", icon="📧")
                except:
                    st.error("Email notification failed, but you can still use WhatsApp.")

                # 3. PREPARE WHATSAPP REDIRECT
                wa_text = f"*Registration Issue Report*\n\n*Name:* {name}\n*Roll No:* {roll_no}\n*Issue:* {issue_type}\n*Details:* {details}"
                wa_url = f"https://wa.me/{admin_phone}?text={urllib.parse.quote(wa_text)}"
                
                st.success("Issue recorded! Please click the button below to finalize submission via WhatsApp.")
                st.link_button("Finalize on WhatsApp ✅", wa_url)
                st.balloons()
            else:
                st.error("Please fill in all required fields.")
