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

# --- PAGE: REPORT REGISTRATION ISSUE ---
elif page == "Report Registration Issue":
    st.header("❗ Report an Issue")
    st.write("Submitting this form logs your information, routes an email to the admin system, and builds your WhatsApp confirmation route.")

    # Using standard Streamlit form fields for layout but targeting the formsubmit backend underneath
    with st.form("issue_form", clear_on_submit=False):
        student_email = st.text_input("Your Email Address *", placeholder="student@example.com")
        name = st.text_input("Full Name *")
        roll_no = st.text_input("Roll Number / Student ID *")
        issue_type = st.selectbox("Issue Category", ["Login Problem", "Subject Not Showing", "Document Error", "Other"])
        details = st.text_area("Detailed Description *")
        
        submitted = st.form_submit_button("Submit & Notify Admin")
        
    if submitted:
        if student_email and name and roll_no and details:
            
            # FormSubmit payload matching the HTML Form data parameters perfectly
            email_payload = {
                "email": student_email, # Corresponds to <input type="email" name="email">
                "Student Name": name,
                "Roll Number": roll_no,
                "Issue Type": issue_type,
                "Detailed Description": details,
                "_subject": f"🚨 Urgent: Registration Issue from {name}",
                "_captcha": "false" # Bypasses captcha to process dynamically via backend API
            }
            
            with st.spinner("Processing form with target server..."):
                try:
                    # Executes the exact matching POST action to https://formsubmit.co/krishna5689@outlook.in
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
            export default function BSCStudentManagementApp() {
  const notices = [
    {
      title: 'Semester Exam Form Notice',
      date: '31 May 2026',
      desc: 'All B.Sc students must submit semester examination forms before 10 June 2026.',
    },
    {
      title: 'Google Classroom Integration Live',
      date: '28 May 2026',
      desc: 'Students can now access study materials directly from connected Google Classrooms.',
    },
  ];

  const registrationIssues = [
    'Low attendance issue',
    'Exam form submission pending',
    'Samarth portal login problem',
    'Fee payment verification pending',
  ];

  const studyMaterials = [
    {
      subject: 'Structural Geology',
      teacher: 'Dr. Sharma',
      classroom: 'Google Classroom Connected',
    },
    {
      subject: 'Mineralogy',
      teacher: 'Prof. Singh',
      classroom: 'Google Classroom Connected',
    },
    {
      subject: 'Engineering Mathematics',
      teacher: 'Dr. Verma',
      classroom: 'Google Classroom Connected',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-3xl p-8 shadow-xl mb-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">B.Sc Student Management Portal</h1>
              <p className="text-lg opacity-90">
                Smart academic platform for study materials, notices, classroom access, and student issue management.
              </p>
            </div>

            <button className="bg-white text-blue-700 px-6 py-3 rounded-2xl font-semibold shadow-md hover:scale-105 transition-transform">
              Login with Google
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-2">Students</h2>
            <p className="text-4xl font-bold text-blue-600">1,250</p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-2">Courses</h2>
            <p className="text-4xl font-bold text-green-600">18</p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-2">Notices</h2>
            <p className="text-4xl font-bold text-orange-500">6</p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-2">Pending Issues</h2>
            <p className="text-4xl font-bold text-red-500">12</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-3xl shadow-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Study Materials</h2>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition">
                  Sync Google Classroom
                </button>
              </div>

              <div className="space-y-4">
                {studyMaterials.map((item, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-2xl p-5 hover:shadow-md transition"
                  >
                    <div className="flex flex-col md:flex-row justify-between gap-4">
                      <div>
                        <h3 className="text-xl font-semibold">{item.subject}</h3>
                        <p className="text-gray-600">Teacher: {item.teacher}</p>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
                          {item.classroom}
                        </span>

                        <button className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 transition">
                          Open Classroom
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-6">News & Notices</h2>

              <div className="space-y-4">
                {notices.map((notice, index) => (
                  <div
                    key={index}
                    className="border-l-4 border-blue-600 bg-gray-50 p-4 rounded-xl"
                  >
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="text-lg font-semibold">{notice.title}</h3>
                      <span className="text-sm text-gray-500">{notice.date}</span>
                    </div>

                    <p className="text-gray-700">{notice.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-3xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-5">Registration Issues</h2>

              <div className="space-y-3">
                {registrationIssues.map((issue, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between bg-red-50 border border-red-100 p-4 rounded-2xl"
                  >
                    <p className="font-medium text-gray-700">{issue}</p>
                    <button className="bg-red-500 text-white px-3 py-1 rounded-lg text-sm hover:bg-red-600 transition">
                      Resolve
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-5">Quick Access</h2>

              <div className="grid grid-cols-2 gap-4">
                <button className="bg-blue-100 text-blue-700 py-4 rounded-2xl font-semibold hover:scale-105 transition-transform">
                  Attendance
                </button>

                <button className="bg-green-100 text-green-700 py-4 rounded-2xl font-semibold hover:scale-105 transition-transform">
                  Assignments
                </button>

                <button className="bg-orange-100 text-orange-700 py-4 rounded-2xl font-semibold hover:scale-105 transition-transform">
                  Timetable
                </button>

                <button className="bg-purple-100 text-purple-700 py-4 rounded-2xl font-semibold hover:scale-105 transition-transform">
                  Results
                </button>
              </div>
            </div>

            <div className="bg-gradient-to-br from-indigo-600 to-purple-700 text-white rounded-3xl p-6 shadow-lg">
              <h2 className="text-2xl font-bold mb-3">Admin Panel</h2>
              <p className="mb-4 opacity-90">
                Manage student records, notices, classroom connections, and registration support requests.
              </p>

              <button className="bg-white text-indigo-700 px-5 py-3 rounded-2xl font-semibold hover:scale-105 transition-transform">
                Open Dashboard
              </button>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center text-gray-500 text-sm">
          Powered by Google Workspace • MicroHNM Technologies

/*
DEPLOYMENT GUIDE

1. Install Node.js
2. Create React App using Vite or Next.js
3. Copy this component into App.jsx
4. Run:
   npm install
   npm run dev

5. Publish on Vercel:
   - Upload project to GitHub
   - Go to vercel.com
   - Import GitHub repository
   - Click Deploy

6. Optional Backend Integration:
   - Firebase Authentication
   - Firestore Database
   - Google Classroom API
   - Google OAuth Login

7. Recommended Features:
   - Student Login System
   - Admin Dashboard
   - Attendance Tracking
   - Assignment Upload
   - PDF Study Material Viewer
   - Notice Push Notifications
*/
        </div>
      </div>
    </div>
  );
}

        else:
            st.error("⚠️ Validation failure: Please fill out all required fields marked with (*).")
