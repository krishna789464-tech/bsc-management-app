import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- SETTINGS ---
st.set_page_config(page_title="BSc Management Portal", layout="wide")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .card { padding: 20px; border-radius: 10px; background-color: white; border: 1px solid #ddd; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 BSc Management")
page = st.sidebar.radio("Menu", ["News & Announcements", "Study Material", "Report Registration Issue"])

# --- PAGE 1: NEWS & ANNOUNCEMENTS ---
if page == "News & Announcements":
    st.header("📢 News & Announcements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("University of Lucknow Notices")
        # Scraper for LU
        lu_url = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
        st.caption(f"Fetching live data from LU Website...")
        try:
            res = requests.get(lu_url, timeout=5)
            soup = BeautifulSoup(res.content, 'html.parser')
            # Look for links that usually contain notices
            links = soup.find_all('a', href=True)
            count = 0
            for link in links:
                if "news" in link['href'] and len(link.text.strip()) > 20 and count < 8:
                    full_link = link['href'] if link['href'].startswith('http') else "https://www.lkouniv.ac.in" + link['href']
                    st.markdown(f"✅ [{link.text.strip()}]({full_link})")
                    count += 1
        except:
            st.error("Could not load live news. [Visit Official Site]("+lu_url+")")

    with col2:
        st.subheader("📤 Upload Custom Notice")
        custom_title = st.text_input("Notice Headline")
        custom_file = st.file_uploader("Upload PDF or Image", type=['pdf', 'png', 'jpg'])
        if st.button("Publish Locally"):
            if custom_title and custom_file:
                st.success(f"Published: {custom_title}")
                st.info("Note: Files uploaded here are visible during this session.")

# --- PAGE 2: STUDY MATERIAL ---
elif page == "Study Material":
    st.header("📚 Study Material Section")
    st.write("Click a subject to open the Google Classroom folder.")

    # SUBJECT LIST - EASY TO EDIT
    subjects = [
        {"name": "BSc Management Core (Group)", "url": "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat"},
        # To add more subjects, copy the line below and change name/url:
        # {"name": "Business Finance", "url": "LINK_HERE"},
    ]

    for sub in subjects:
        st.markdown(f"""
        <div class="card">
            <h3>{sub['name']}</h3>
            <p>Access notes, assignments, and links.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(f"Open {sub['name']}", sub['url'])

# --- PAGE 3: REGISTRATION ISSUES ---
elif page == "Report Registration Issue":
    st.header("❗ Report an Issue")
    st.write("Fill out this form for app or course registration problems.")
    
    with st.form("issue_form"):
        name = st.text_input("Your Name")
        roll = st.text_input("Roll Number")
        category = st.selectbox("Issue Type", ["App Registration", "Login Error", "Incorrect Subject", "Other"])
        desc = st.text_area("Details")
        
        if st.form_submit_button("Submit to Admin"):
            if name and desc:
                st.success("Issue submitted successfully!")
                st.balloons()
            else:
                st.warning("Please fill in all fields.")
