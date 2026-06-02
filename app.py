import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image
from datetime import date

# --- 1. THEME CONFIGURATION & FONTS ---
# Standardize professional font rendering and structural styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .stWidgetForm {
        font-family: 'Inter', sans-serif !important;
    }
    
    .metric-card {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.15);
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 12px;
    }
    
    .notice-card {
        padding: 16px;
        border-radius: 10px;
        border-left: 4px solid #2563eb;
        background-color: rgba(37, 99, 235, 0.03);
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    .stButton>button {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Target local logo image location securely
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"
logo_exists = os.path.exists(LOGO_PATH)
app_logo = None

if logo_exists:
    try:
        app_logo = Image.open(LOGO_PATH)
        page_icon_val = app_logo
    except Exception:
        logo_exists = False

if not logo_exists:
    page_icon_val = "🎓"

st.set_page_config(
    page_title="B.Sc Student Management Portal",
    page_icon=page_icon_val,
    layout="wide"
)

# Render Application Logo natively in Sidebar
if logo_exists and app_logo:
    try:
        st.logo(LOGO_PATH)
    except AttributeError:
        # Fallback block for older execution environments
        st.sidebar.image(app_logo, width=130)
else:
    st.sidebar.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🎓</h2>", unsafe_allow_html=True)

# --- 2. SECURE ADMIN CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 3. SESSION STATE CONFIGURATION ---
# Initialize navigation key
if "nav_radio" not in st.session_state:
    st.session_state.nav_radio = "Dashboard"

# Initialize Study Planner base items
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"task": "Submit Structural Geology Practical File", "due": date.today(), "completed": False},
        {"task": "Review Mineralogy Lecture 4 Notes", "due": date.today(), "completed": True},
        {"task": "Prepare for Math Revision Test", "due": date.today(), "completed": False}
    ]

# Navigation handler function
def navigate_to(page_name):
    st.session_state.nav_radio = page_name
    st.rerun()

# --- 4. SIDEBAR SELECTION SYSTEM ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.caption(f"Developer Contact: {ADMIN_EMAIL}")

page_options = [
    "Dashboard", 
    "AI Assistant", 
    "News & Announcements", 
    "Study Material", 
    "Timetable & Calendar",
    "GPA Calculator & Planner",
    "Report Registration Issue"
]

# Primary menu implementation
selected_page = st.sidebar.radio(
    "Go to:", 
    page_options, 
    key="nav_radio"
)

# --- PAGE: DASHBOARD ---
if selected_page == "Dashboard":
    st.title("Academic Dashboard")
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 28px; border-radius: 14px; margin-bottom: 25px;">
            <h1 style="margin: 0; color: white; font-size: 28px; font-weight: 700;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 8px; font-size: 15px;">
                Central hub to track coursework schedules, academic standing, live notices, and support documentation.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h4>Enrolled Students</h4><h2 style="color: #2563eb; margin:0; font-weight: 700;">1,250</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>Courses Offered</h4><h2 style="color: #10b981; margin:0; font-weight: 700;">18</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4>Live Notices</h4><h2 style="color: #f59e0b; margin:0; font-weight: 700;">10+</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h4>Resolved Tickets</h4><h2 style="color: #6b7280; margin:0; font-weight: 700;">94%</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📚 Subject Stream Overview")
        subjects_list = [
            {"subject": "Structural Geology", "faculty": "Dr. Sharma", "status": "Active Class"},
            {"subject": "Mineralogy & Crystallography", "faculty": "Prof. Singh", "status": "Lab Active"},
            {"subject": "Engineering Mathematics", "faculty": "Dr. Verma", "status": "Active Class"}
        ]
        for item in subjects_list:
            with st.container():
                st.markdown(f"**{item['subject']}** — Instructor: *{item['faculty']}*")
                st.caption(f"🟢 Synchronized via Google Workspace — `{item['status']}`")
                st.divider()
                
    with right_col:
        st.subheader("⚡ Quick Navigation")
        if st.button("📅 View Class Timetable", use_container_width=True):
            navigate_to("Timetable & Calendar")
        if st.button("📖 Download Study Materials", use_container_width=True):
            navigate_to("Study Material")
        if st.button("📊 Calculate CGPA/SGPA", use_container_width=True):
            navigate_to("GPA Calculator & Planner")
        if st.button("🚨 Report Student Portal Issue", use_container_width=True):
            navigate_to("Report Registration Issue")

# --- PAGE: AI ASSISTANT ---
elif selected_page == "AI Assistant":
    st.header("🤖 AI Student Counselor & Assistant")
    st.write("Interact with our automated system to solve minor scheduling questions, queries, or policy reviews.")
    
    jotform_script = """
    <script
      src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'>
    </script>
    """
    components.html(jotform_script, height=600, scrolling=True)

# --- PAGE: NEWS & ANNOUNCEMENTS ---
elif selected_page == "News & Announcements":
    st.header("📢 Official Notices & Bulletins")
    st.write("Dynamic, real-time announcements sourced directly from the Lucknow University database.")
    
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Fetch Live University Bulletins", type="primary"):
        with st.spinner("Accessing Lucknow University news servers..."):
            try:
                # Add professional headers to mimic an interactive web browser
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                }
                res = requests.get(lu_url, headers=headers, timeout=12)
                soup = BeautifulSoup(res.content, 'html.parser')
                links = soup.find_all('a', href=True)
                found = 0
                
                for link in links:
                    link_text = link.text.strip().replace("[", "").replace("]", "")
                    # Match standard notice and practical examination routes
                    if ("news" in link['href'] or "upload" in link['href']) and len(link_text) > 15:
                        href_val = link['href']
                        url = href_val if href_val.startswith('http') else "https://www.lkouniv.ac.in" + href_val
                        
                        st.markdown(f"""
                        <div class="notice-card">
                            <strong style="color: #2563eb;">📌 Official Circular</strong><br>
                            <a href="{url}" target="_blank" style="text-decoration: none; font-weight: 500;">{link_text}</a>
                        </div>
                        """, unsafe_allow_html=True)
                        found += 1
                        
                    if found >= 8: 
                        break
                if found == 0:
                    st.info("No active circular elements were identified on the landing page layout.")
            except Exception:
                st.warning("The automated university query timed out. Please access the live site directly:")
                st.link_button("Access Official News Site 🔗", lu_url)

# --- PAGE: STUDY MATERIAL ---
elif selected_page == "Study Material":
    st.header("📚 Digital Classrooms & Resources")
    st.write("Retrieve syllabi, dynamic class folders, and assignment portals mapped to academic tiers.")
    
    tab1, tab2 = st.tabs(["Semester I & II (First Year)", "Advanced Levels (Semester III-VI)"])
    
    with tab1:
        st.subheader("B.Sc Core Modules")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🪨 Structural Geology & Mineralogy")
            st.write("Foundational study paths of mineral characteristics, optical properties, and physical crust formations.")
            st.info("Google Classroom Entry Code: **shf3hsat**")
            st.link_button("Open Classroom Terminal", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", use_container_width=True)
        with col2:
            st.markdown("#### 📐 Calculus & Advanced Algebra")
            st.write("Analytical vectors, matrices, differential mathematical modeling, and core equations.")
            st.info("Google Classroom Entry Code: **math-302**")
            st.link_button("Open Classroom Terminal", "https://classroom.google.com", use_container_width=True)
            
    with tab2:
        st.subheader("B.Sc Senior Semesters")
        st.write("Assigned folders will activate sequentially in accordance with your registered course choices.")
        st.caption("Consult your academic advisor if your specialized subjects are currently not populated.")

# --- PAGE: TIMETABLE & CALENDAR ---
elif selected_page == "Timetable & Calendar":
    st.header("📅 Weekly Academic Schedules")
    st.write("Review active lecture halls, laboratory periods, and assigned professors.")
    
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    tabs = st.tabs(days_of_week)
    
    schedule_data = {
        "Monday": [
            {"Hour": "09:00 AM - 10:00 AM", "Subject": "Structural Geology", "Lecture Hall": "Room 102", "Faculty": "Dr. Sharma"},
            {"Hour": "10:15 AM - 11:15 AM", "Subject": "Mineralogy Laboratory", "Lecture Hall": "Mineral Lab C", "Faculty": "Prof. Singh"},
            {"Hour": "11:30 AM - 12:30 PM", "Subject": "Engineering Math", "Lecture Hall": "Hall 4", "Faculty": "Dr. Verma"}
        ],
        "Tuesday": [
            {"Hour": "09:00 AM - 10:00 AM", "Subject": "Physics Foundations", "Lecture Hall": "Room 205", "Faculty": "Dr. Gupta"},
            {"Hour": "10:15 AM - 11:15 AM", "Subject": "Structural Geology", "Lecture Hall": "Room 102", "Faculty": "Dr. Sharma"}
        ],
        "Wednesday": [
            {"Hour": "09:00 AM - 10:00 AM", "Subject": "Structural Geology", "Lecture Hall": "Room 102", "Faculty": "Dr. Sharma"},
            {"Hour": "10:15 AM - 11:15 AM", "Subject": "Mineralogy Core", "Lecture Hall": "Room 104", "Faculty": "Prof. Singh"},
            {"Hour": "11:30 AM - 12:30 PM", "Subject": "Engineering Math", "Lecture Hall": "Hall 4", "Faculty": "Dr. Verma"}
        ],
        "Thursday": [
            {"Hour": "09:00 AM - 11:00 AM", "Subject": "Practical Physics Lab", "Lecture Hall": "Physics Wing", "Faculty": "Dr. Gupta"}
        ],
        "Friday": [
            {"Hour": "10:15 AM - 11:15 AM", "Subject": "Mineralogy Core", "Lecture Hall": "Room 104", "Faculty": "Prof. Singh"},
            {"Hour": "11:30 AM - 12:30 PM", "Subject": "Engineering Math", "Lecture Hall": "Hall 4", "Faculty": "Dr. Verma"}
        ],
        "Saturday": [
            {"Hour": "09:00 AM - 11:00 AM", "Subject": "Practical Presentation / Seminar", "Lecture Hall": "Auditorium-B", "Faculty": "Geology Dept"}
        ]
    }
    
    for idx, day in enumerate(days_of_week):
        with tabs[idx]:
            day_schedule = schedule_data.get(day, [])
            if day_schedule:
                df = pd.DataFrame(day_schedule)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No active lecture sessions are booked for this day.")

# --- PAGE: GPA CALCULATOR & PLANNER ---
elif selected_page == "GPA Calculator & Planner":
    st.header("📊 Performance & Task Planner")
    
    tab_planner, tab_gpa = st.tabs(["📋 Study Task Planner", "🧮 CBCS Grade Point Calculator"])
    
    with tab_planner:
        st.subheader("Course Task Tracker")
        st.write("Organize and manage upcoming assignments, practical logbooks, or test prep natively:")
        
        # Build DataFrame from task list safely
        df_tasks = pd.DataFrame(st.session_state.tasks)
        
        # Render a structured interactive data editor
        edited_df = st.data_editor(
            df_tasks,
            column_config={
                "task": st.column_config.TextColumn("Academic Assignment / Objective", width="large", required=True),
                "due": st.column_config.DateColumn("Target Due Date", format="YYYY-MM-DD", required=True),
                "completed": st.column_config.CheckboxColumn("Completed State", default=False)
            },
            num_rows="dynamic", # Dynamic row additions/removals natively enabled
            use_container_width=True,
            key="task_editor"
        )
        
        # Save edits back to session state stably
        if st.session_state.get("task_editor") is not None:
            st.session_state.tasks = edited_df.to_dict("records")

    with tab_gpa:
        st.subheader("CBCS Semester SGPA Estimator")
        st.write("Provide course credits and grade letters based on the standard 10-point scale:")
        
        grade_system = {
            "O (Outstanding) [10]": 10,
            "A+ (Excellent) [9]": 9,
            "A (Very Good) [8]": 8,
            "B+ (Good) [7]": 7,
            "B (Above Average) [6]": 6,
            "C (Average) [5]": 5,
            "P (Pass) [4]": 4,
            "F (Fail) [0]": 0
        }
        
        subject_count = st.number_input("Input Number of Core/Elective Subjects:", min_value=1, max_value=12, value=4)
        
        accumulated_credits = 0
        cumulative_grades = 0
        
        col_name, col_grade, col_credit = st.columns([3, 2, 2])
        with col_name:
            st.caption("Class Name")
        with col_grade:
            st.caption("Obtained Grade")
        with col_credit:
            st.caption("Course Weight (Credits)")
            
        for i in range(int(subject_count)):
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.text_input(f"Course Name {i+1}", value=f"Course Module {i+1}", key=f"title_c_{i}", label_visibility="collapsed")
            with col2:
                selected_grade_lbl = st.selectbox("", list(grade_system.keys()), index=2, key=f"val_g_{i}", label_visibility="collapsed")
                numerical_grade = grade_system[selected_grade_lbl]
            with col3:
                allocated_credit = st.number_input("", min_value=1, max_value=8, value=4, key=f"val_c_{i}", label_visibility="collapsed")
                
            accumulated_credits += allocated_credit
            cumulative_grades += (numerical_grade * allocated_credit)
            
        st.divider()
        if accumulated_credits > 0:
            sgpa_score = cumulative_grades / accumulated_credits
            col_met, col_rem = st.columns(2)
            with col_met:
                st.metric("Estimated Semester SGPA", f"{sgpa_score:.2f} / 10.00")
            with col_rem:
                if sgpa_score >= 9.00:
                    st.success("Outcome Classification: Outstanding Performance Class")
                elif sgpa_score >= 7.50:
                    st.success("Outcome Classification: First Division with Distinction")
                elif sgpa_score >= 6.00:
                    st.info("Outcome Classification: First Division Pass")
                elif sgpa_score >= 5.00:
                    st.warning("Outcome Classification: Second Division Pass")
                else:
                    st.error("Outcome Classification: Below Standard (Requires Consultation)")

# --- PAGE: REPORT REGISTRATION ISSUE ---
elif selected_page == "Report Registration Issue":
    st.header("🚨 Report System & Portal Anomaly")
    st.write("Submit technical issues, access problems, or course verification errors to the administration console.")

    with st.form("issue_submission_form", clear_on_submit=False):
        student_email = st.text_input("University Email Address *", placeholder="e.g., student@lkouniv.edu")
        student_name = st.text_input("Registered Full Name *")
        student_id = st.text_input("Enrollment/Roll Number *")
        issue_cat = st.selectbox("Categorize the Problem", ["System Login Issue", "Missing Subject Selection", "Document Verification Error", "Other Tech Failure"])
        issue_desc = st.text_area("Detailed System Error Description *")
        
        trigger_submission = st.form_submit_button("Submit Form & Alert Administration")
        
    if trigger_submission:
        if student_email and student_name and student_id and issue_desc:
            
            payload = {
                "email": student_email.strip(),
                "Student Name": student_name.strip(),
                "Enrollment Number": student_id.strip(),
                "Issue Type": issue_cat,
                "Detailed Description": issue_desc.strip(),
                "_subject": f"⚠️ Ticket: Student Portal Issue - {student_name.strip()}",
                "_captcha": "false"
            }
            
            with st.spinner("Submitting technical payload directly to secure routing servers..."):
                try:
                    response = requests.post(
                        f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", 
                        data=payload,
                        timeout=12
                    )
                    if response.status_code == 200:
                        st.toast("Administrative payload delivered successfully.", icon="📨")
                    else:
                        st.error("Submission was acknowledged but could not complete automated verification.")
                except Exception:
                    st.error("Primary transfer timeout. Proceeding via active fallback channel.")

            whatsapp_msg = f"*Student System Defect Submission*\n\n*Name:* {student_name}\n*Enrollment ID:* {student_id}\n*Email:* {student_email}\n*Type:* {issue_cat}\n*Log Description:* {issue_desc}"
            whatsapp_link = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(whatsapp_msg)}"
            
            st.success("Entry registered in state storage!")
            st.write("To verify routing or initiate immediate support with administrative staff, finalize via direct message below:")
            st.link_button("Initiate Direct Administrative WhatsApp Help ✅", whatsapp_link)
            st.balloons()
        else:
            st.error("Form validation failed. Please populate all fields marked with an asterisk (*).")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='color: gray; font-size: 11px;'>Core Infrastructure Supported by Google Workspace APIs & Microhnm Technologies</center>", unsafe_allow_html=True)
