import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image
from datetime import date

# --- 1. CONFIGURATION & STYLING ---
LOGO_PATH = r"C:\Users\ADMIN\Desktop\app logo.png"

# Fallback mechanism for logo path
logo_exists = os.path.exists(LOGO_PATH)
if logo_exists:
    try:
        app_logo = Image.open(LOGO_PATH)
        page_icon_val = app_logo
    except Exception:
        app_logo = None
        page_icon_val = "🎓"
else:
    app_logo = None
    page_icon_val = "🎓"

st.set_page_config(
    page_title="B.Sc Student Portal",
    page_icon=page_icon_val,
    layout="wide"
)

# Render logo
if logo_exists and app_logo:
    try:
        st.logo(LOGO_PATH)
    except AttributeError:
        # Fallback if older Streamlit version is used
        st.sidebar.image(app_logo, width=150)
else:
    st.sidebar.markdown("<h1 style='text-align: center;'>🎓</h1>", unsafe_allow_html=True)

# Custom responsive CSS targeting better visual separation
st.markdown("""
    <style>
    .metric-card {
        background-color: var(--background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .notice-card {
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2563eb;
        background-color: rgba(37, 99, 235, 0.05);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"

# --- 2. SESSION STATE MANAGEMENT & ROUTING ---
# Allows quick access links on dashboard to redirect the user to other pages smoothly
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"task": "Submit Structural Geology Practical File", "due": str(date.today()), "completed": False},
        {"task": "Review Mineralogy Lecture 4 notes", "due": str(date.today()), "completed": True}
    ]

# Callback to update page selection programmatically
def navigate_to(page_name):
    st.session_state.page = page_name

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 Student Portal")
st.sidebar.info(f"Admin: {ADMIN_EMAIL}")

page_options = [
    "Dashboard", 
    "AI Assistant", 
    "News & Announcements", 
    "Study Material", 
    "Timetable & Calendar",
    "GPA Calculator & Planner",
    "Report Registration Issue"
]

# Sync sidebar radio selection with session state
current_index = page_options.index(st.session_state.page) if st.session_state.page in page_options else 0
selected_page = st.sidebar.radio("Go to:", page_options, index=current_index, key="nav_radio")

# Ensure state updates correctly
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# --- PAGE: DASHBOARD ---
if st.session_state.page == "Dashboard":
    st.title("Welcome to the Dashboard")
    st.markdown("""
        <div style="background: linear-gradient(to right, #2563eb, #4f46e5); color: white; padding: 30px; border-radius: 15px; margin-bottom: 25px;">
            <h1 style="margin: 0; color: white;">B.Sc Student Management Portal</h1>
            <p style="opacity: 0.9; margin-top: 5px; font-size: 16px;">
                Smart academic platform for accessing study materials, viewing schedules, calculation utilities, and direct administration queries.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Modernized metrics layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h4>Enrolled Students</h4><h2 style="color: #2563eb; margin:0;">1,250</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>B.Sc Specializations</h4><h2 style="color: #16a34a; margin:0;">4</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4>Active Classrooms</h4><h2 style="color: #ea580c; margin:0;">8</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h4>Pending System Issues</h4><h2 style="color: #dc2626; margin:0;">12</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📚 Quick Overview: Connected Materials")
        materials = [
            {"subject": "Structural Geology", "teacher": "Dr. Sharma", "code": "shf3hsat"},
            {"subject": "Mineralogy", "teacher": "Prof. Singh", "code": "min-202"},
            {"subject": "Engineering Mathematics", "teacher": "Dr. Verma", "code": "math-301"}
        ]
        for item in materials:
            with st.container():
                st.markdown(f"**{item['subject']}** — Instructor: *{item['teacher']}*")
                st.caption(f"🟢 Google Classroom Active (Code: `{item['code']}`)")
                st.divider()
                
    with right_col:
        st.subheader("⚡ Quick Access Controls")
        if st.button("📅 View Academic Timetable", use_container_width=True):
            navigate_to("Timetable & Calendar")
        if st.button("📖 Access Study Materials", use_container_width=True):
            navigate_to("Study Material")
        if st.button("📊 CGPA Calculator & Planner", use_container_width=True):
            navigate_to("GPA Calculator & Planner")
        if st.button("🚨 Report a Registration Issue", use_container_width=True):
            navigate_to("Report Registration Issue")

# --- PAGE: AI ASSISTANT ---
elif st.session_state.page == "AI Assistant":
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Our automated academic helper is loading below. If it does not display automatically, please locate the chat widget on your screen.")
    
    jotform_script = """
    <script
      src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'>
    </script>
    """
    components.html(jotform_script, height=600, scrolling=True)

# --- PAGE: NEWS & ANNOUNCEMENTS ---
elif st.session_state.page == "News & Announcements":
    st.header("📢 Official Notices & Live Feed")
    st.write("Fetch real-time updates directly from the Lucknow University notifications board.")
    
    lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Fetch Latest Bulletins", type="primary"):
        with st.spinner("Checking University Servers..."):
            try:
                res = requests.get(lu_url, timeout=10)
                soup = BeautifulSoup(res.content, 'html.parser')
                links = soup.find_all('a', href=True)
                found = 0
                
                for link in links:
                    link_text = link.text.strip().replace("[", "").replace("]", "")
                    if "news" in link['href'] and len(link_text) > 15:
                        href_val = link['href']
                        url = href_val if href_val.startswith('http') else "https://www.lkouniv.ac.in" + href_val
                        
                        st.markdown(f"""
                        <div class="notice-card">
                            <strong style="color: #2563eb;">📌 Update</strong><br>
                            <a href="{url}" target="_blank" style="text-decoration: none; font-weight: 500;">{link_text}</a>
                        </div>
                        """, unsafe_allow_html=True)
                        found += 1
                    if found >= 10: 
                        break
                if found == 0:
                    st.info("No formatted announcements matching filter targets were found on the homepage structure.")
            except Exception:
                st.error(f"Live feed temporarily unresponsive. You can access the website directly:")
                st.link_button("Go to LU News Portal 🔗", lu_url)

# --- PAGE: STUDY MATERIAL ---
elif st.session_state.page == "Study Material":
    st.header("📚 Study Materials & Resources")
    st.write("Organized repository categorized by academic level. Click directly to launch classrooms.")
    
    tab1, tab2, tab3 = st.tabs(["Semester I & II", "Semester III & IV", "Semester V & VI"])
    
    with tab1:
        st.subheader("First Year B.Sc Core")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🪨 Geology & Mineralogy")
            st.write("Course Syllabus covering crystallography, crystal optics, and basic rock types.")
            st.info("Classroom Code: **shf3hsat**")
            st.link_button("Join Classroom", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", use_container_width=True)
        with col2:
            st.markdown("### 📐 Mathematics & Mechanics")
            st.write("Calculus, analytical geometry, and core mechanical theories.")
            st.info("Classroom Code: **math-101**")
            st.link_button("Join Classroom", "https://classroom.google.com", use_container_width=True)
            
    with tab2:
        st.subheader("Second Year Advanced Core")
        st.write("More structured classroom streams will load below as semester modules deploy.")
        st.caption("No custom class configurations are active for Semester III & IV currently.")
        
    with tab3:
        st.subheader("Third Year Specialization Tracks")
        st.write("Practical labs, project files, and dynamic curriculum files.")
        st.link_button("View Standard Project Guidelines (PDF)", "https://classroom.google.com")

# --- PAGE: TIMETABLE & CALENDAR ---
elif st.session_state.page == "Timetable & Calendar":
    st.header("📅 Academic Timetable & Schedules")
    st.write("Plan your week. Switch tabs below to check schedules by day.")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    tabs = st.tabs(days)
    
    schedule_data = {
        "Monday": [
            {"Time": "09:00 AM - 10:00 AM", "Subject": "Structural Geology", "Room": "L-12", "Teacher": "Dr. Sharma"},
            {"Time": "10:15 AM - 11:15 AM", "Subject": "Mineralogy Lab", "Room": "Lab C", "Teacher": "Prof. Singh"},
            {"Time": "11:30 AM - 12:30 PM", "Subject": "Applied Mathematics", "Room": "LH-2", "Teacher": "Dr. Verma"}
        ],
        "Tuesday": [
            {"Time": "09:00 AM - 10:00 AM", "Subject": "Physics Principles", "Room": "LH-4", "Teacher": "Dr. Gupta"},
            {"Time": "10:15 AM - 11:15 AM", "Subject": "Structural Geology", "Room": "L-12", "Teacher": "Dr. Sharma"}
        ],
        "Wednesday": [
            {"Time": "09:00 AM - 10:00 AM", "Subject": "Structural Geology", "Room": "L-12", "Teacher": "Dr. Sharma"},
            {"Time": "10:15 AM - 11:15 AM", "Subject": "Mineralogy Theory", "Room": "LH-1", "Teacher": "Prof. Singh"},
            {"Time": "11:30 AM - 12:30 PM", "Subject": "Applied Mathematics", "Room": "LH-2", "Teacher": "Dr. Verma"}
        ],
        "Thursday": [
            {"Time": "09:00 AM - 10:00 AM", "Subject": "Physics Lab", "Room": "Physics Lab A", "Teacher": "Dr. Gupta"},
            {"Time": "01:30 PM - 02:30 PM", "Subject": "Extra Curricular Activity", "Room": "Ground", "Teacher": "N/A"}
        ],
        "Friday": [
            {"Time": "10:15 AM - 11:15 AM", "Subject": "Mineralogy Theory", "Room": "LH-1", "Teacher": "Prof. Singh"},
            {"Time": "11:30 AM - 12:30 PM", "Subject": "Applied Mathematics", "Room": "LH-2", "Teacher": "Dr. Verma"}
        ],
        "Saturday": [
            {"Time": "09:00 AM - 11:00 AM", "Subject": "Fieldwork/Practical Seminars", "Room": "Seminar Hall", "Teacher": "Department Faculty"}
        ]
    }
    
    for i, day in enumerate(days):
        with tabs[i]:
            day_classes = schedule_data.get(day, [])
            if day_classes:
                df = pd.DataFrame(day_classes)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No lectures scheduled for this day.")

# --- PAGE: CGPA CALCULATOR & PLANNER ---
elif st.session_state.page == "GPA Calculator & Planner":
    st.header("📊 Interactive Academic Planner")
    
    plan_tab, calc_tab = st.tabs(["📋 To-Do & Task Tracker", "🧮 SGPA Calculator"])
    
    with plan_tab:
        st.subheader("Manage Study Tasks & Assignments")
        
        # Display current tasks
        for idx, task_item in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
            with col1:
                # Use a unique key for each dynamic checkbox
                is_completed = st.checkbox("", value=task_item["completed"], key=f"task_{idx}")
                st.session_state.tasks[idx]["completed"] = is_completed
            with col2:
                if is_completed:
                    st.markdown(f"~~{task_item['task']}~~")
                else:
                    st.markdown(f"**{task_item['task']}**")
            with col3:
                st.caption(f"📅 Due: {task_item['due']}")
                
        # Add new task form
        st.divider()
        st.write("Add New Study Goal:")
        with st.form("new_task_form", clear_on_submit=True):
            new_title = st.text_input("Task/Assignment Name")
            due_date = st.date_input("Due Date", min_value=date.today())
            submitted_task = st.form_submit_button("Add Task")
            
            if submitted_task and new_title:
                st.session_state.tasks.append({
                    "task": new_title,
                    "due": str(due_date),
                    "completed": False
                })
                st.toast("New academic task added successfully!", icon="✅")
                st.rerun()

    with calc_tab:
        st.subheader("Semester SGPA Calculator")
        st.write("Estimate your performance using standard Choice Based Credit System (CBCS) scales:")
        
        grade_scale = {
            "O (Outstanding) [10]": 10,
            "A+ (Excellent) [9]": 9,
            "A (Very Good) [8]": 8,
            "B+ (Good) [7]": 7,
            "B (Above Average) [6]": 6,
            "C (Average) [5]": 5,
            "P (Pass) [4]": 4,
            "F (Fail) [0]": 0
        }
        
        num_subjects = st.number_input("How many subjects are in your semester?", min_value=1, max_value=10, value=5)
        
        total_credits = 0
        weighted_points = 0
        
        col_names, col_grades, col_credits = st.columns([3, 2, 2])
        
        with col_names:
            st.caption("Subject Name")
        with col_grades:
            st.caption("Grade Received")
        with col_credits:
            st.caption("Course Credits")
            
        for i in range(int(num_subjects)):
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.text_input(f"Subject {i+1}", value=f"Course {i+1}", key=f"subj_name_{i}", label_visibility="collapsed")
            with col2:
                selected_grade = st.selectbox("", list(grade_scale.keys()), index=2, key=f"subj_grade_{i}", label_visibility="collapsed")
                grade_val = grade_scale[selected_grade]
            with col3:
                credits_val = st.number_input("", min_value=1, max_value=8, value=4, key=f"subj_credit_{i}", label_visibility="collapsed")
                
            total_credits += credits_val
            weighted_points += (grade_val * credits_val)
            
        st.divider()
        if total_credits > 0:
            sgpa = weighted_points / total_credits
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Estimated Semester SGPA", f"{sgpa:.2f} / 10.00")
            with col_res2:
                if sgpa >= 9.0:
                    st.success("Remark: Outstanding Academic Performance!")
                elif sgpa >= 7.5:
                    st.success("Remark: First Class with Distinction!")
                elif sgpa >= 6.0:
                    st.info("Remark: First Division")
                elif sgpa >= 5.0:
                    st.warning("Remark: Second Division")
                else:
                    st.error("Remark: Needs Improvement")

# --- PAGE: REPORT REGISTRATION ISSUE ---
elif st.session_state.page == "Report Registration Issue":
    st.header("❗ Report registration anomalies")
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
                except Exception:
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
