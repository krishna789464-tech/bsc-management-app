import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CONFIGURATION & STYLING ---
# Use relative path or environment variable for logo
LOGO_PATH = os.getenv("LOGO_PATH", None)

logo_exists = LOGO_PATH and os.path.exists(LOGO_PATH)
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
    page_title="Academic Student Portal",
    page_icon=page_icon_val,
    layout="wide"
)

# Professional Enterprise Theme Styling
st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #f8fafc; }
    
    /* Clean Main Interface Cards */
    .main-card { 
        padding: 24px; 
        border-radius: 12px; 
        background: #ffffff; 
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px 0 rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
    }
    
    /* Metrics Interface */
    .metric-card { 
        background: #ffffff; 
        padding: 22px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        text-align: center; 
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    /* Structural Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 8px;
    }
    .sidebar-meta {
        font-size: 13px;
        color: #475569;
        background-color: #f1f5f9;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar Navigation Buttons */
    .sidebar-nav-button {
        width: 100%;
        padding: 12px 16px;
        margin: 6px 0;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background-color: #ffffff;
        color: #2563eb;
        text-align: center;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .sidebar-nav-button:hover {
        background-color: #f1f5f9;
        border-color: #2563eb;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
    }
    
    /* --- INVISIBLE HEADERS / DE-BRANDING STREAMLIT --- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    /* Clean up form spacing */
    .stForm {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE TARGET CONFIGURATION ---
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "support@example.com")
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+1234567890")

# --- 2. SIDEBAR NAVIGATION ---
if logo_exists and app_logo:
    st.logo(LOGO_PATH) 
else:
    st.sidebar.markdown("<h2 style='margin-top: 0; color: #2563eb; font-weight:700;'>🎓 System Portal</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-meta">
        <strong style="color:#0f172a;">🏫 Portal Verification</strong><br>
        <span style="opacity: 0.85; font-size:12px;">Access Tier: B.Sc Undergraduate</span><br>
        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #cbd5e1;">
        <strong style="color:#0f172a;">📧 Helpdesk Routing</strong><br>
        <a href="mailto:{ADMIN_EMAIL}" style="color: #2563eb; text-decoration: none; font-size:12px;">{ADMIN_EMAIL}</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-weight: 700; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 8px; color:#64748b;'>CORE WORKSPACES</p>", unsafe_allow_html=True)

# Fixed navigation indexing via Session State to prevent disappearance drops
if "current_page" not in st.session_state:
    st.session_state.current_page = "📊 Student Dashboard"

options_list = [
    "📊 Student Dashboard", 
    "🤖 AI Academic Assistant", 
    "📢 News & Notices", 
    "📚 Study Classrooms", 
    "🧮 Performance Toolkit", 
    "⏱️ Deep Focus Engine", 
    "🚨 Report Routing Terminal"
]

# Track current index safely
default_index = options_list.index(st.session_state.current_page)

page = st.sidebar.radio(
    label="Navigation Menu",
    options=options_list,
    index=default_index,
    label_visibility="collapsed"
)
st.session_state.current_page = page

st.sidebar.markdown("<div style='flex:1;'></div>", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION BUTTONS ---
st.sidebar.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-weight: 700; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 12px; color:#64748b;'>QUICK ACTIONS</p>", unsafe_allow_html=True)

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("🔄 Refresh", use_container_width=True, key="btn_refresh"):
        st.rerun()

with col2:
    if st.button("⚙️ Settings", use_container_width=True, key="btn_settings"):
        st.session_state.current_page = "⚙️ Settings"
        st.rerun()

st.sidebar.button("📞 Support", use_container_width=True, key="btn_support")
st.sidebar.button("ℹ️ About", use_container_width=True, key="btn_about")

st.sidebar.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.caption("System Status: Operational • v1.0")

# --- 3. PAGE ROUTING ---
if page == "📊 Student Dashboard":
    st.markdown("<h1 style='color: #2563eb;'>📊 Student Dashboard</h1>", unsafe_allow_html=True)
    st.info("Dashboard content coming soon...")
    
elif page == "🤖 AI Academic Assistant":
    st.markdown("<h1 style='color: #2563eb;'>🤖 AI Academic Assistant</h1>", unsafe_allow_html=True)
    st.info("AI Assistant feature coming soon...")
    
elif page == "📢 News & Notices":
    st.markdown("<h1 style='color: #2563eb;'>📢 News & Notices</h1>", unsafe_allow_html=True)
    st.info("News and notices coming soon...")
    
elif page == "📚 Study Classrooms":
    st.markdown("<h1 style='color: #2563eb;'>📚 Study Classrooms</h1>", unsafe_allow_html=True)
    st.info("Study classrooms coming soon...")
    
elif page == "🧮 Performance Toolkit":
    st.markdown("<h1 style='color: #2563eb;'>🧮 Performance Toolkit</h1>", unsafe_allow_html=True)
    st.info("Performance toolkit coming soon...")
    
elif page == "⏱️ Deep Focus Engine":
    st.markdown("<h1 style='color: #2563eb;'>⏱️ Deep Focus Engine</h1>", unsafe_allow_html=True)
    st.info("Deep focus engine coming soon...")
    
elif page == "🚨 Report Routing Terminal":
    st.markdown("<h1 style='color: #2563eb;'>🚨 Report Routing Terminal</h1>", unsafe_allow_html=True)
    st.info("Report routing terminal coming soon...")
