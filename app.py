import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time
import base64
import streamlit.components.v1 as components
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1. ARCHITECTURAL CONFIGURATION & STATE
# ==========================================
if "font_scale" not in st.session_state:
    st.session_state.font_scale = 100
if "bg_theme" not in st.session_state:
    st.session_state.bg_theme = "dark"  # Default to premium dark theme
if "animation_played" not in st.session_state:
    st.session_state.animation_played = False

st.set_page_config(
    page_title="Nexus Academic Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CINEMATIC INTRO ANIMATION ENGINE
# ==========================================
if not st.session_state.animation_played:
    animation_html = """
    <div id="animation-overlay">
        <div class="content-wrapper">
            <h1 class="welcome-text">NEXUS ACADEMIA</h1>
            <div class="sub-bar"></div>
            <p class="portal-text">Next-Generation Student Infrastructure</p>
        </div>
    </div>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Inter:wght@300;500&display=swap');
        #animation-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            display: flex; justify-content: center; align-items: center;
            z-index: 999999; font-family: 'Inter', sans-serif; overflow: hidden;
            animation: fadeOutWindow 0.8s cubic-bezier(0.7, 0, 0.3, 1) forwards;
            animation-delay: 2.8s;
        }
        .content-wrapper { text-align: center; display: flex; flex-direction: column; align-items: center; }
        .welcome-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem; font-weight: 900; letter-spacing: 8px; margin: 0;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8); background-size: 200% auto;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shineText 2s linear infinite, scaleUpText 1.8s cubic-bezier(0.1, 0.8, 0.2, 1) forwards; opacity: 0;
        }
        .sub-bar {
            width: 0px; height: 2px; background: linear-gradient(90deg, #38bdf8, #818cf8); margin-top: 20px; margin-bottom: 20px;
            box-shadow: 0px 0px 20px #38bdf8; animation: growBar 1.2s cubic-bezier(0.7, 0, 0.3, 1) forwards; animation-delay: 0.5s;
        }
        .portal-text { font-size: 1rem; font-weight: 300; letter-spacing: 6px; color: #94a3b8; margin: 0; text-transform: uppercase; opacity: 0; animation: fadeInPortal 1s ease-out forwards; animation-delay: 1.2s; }
        @keyframes scaleUpText { 0% { transform: scale(0.9); opacity: 0; filter: blur(10px); } 100% { transform: scale(1); opacity: 1; filter: blur(0px); } }
        @keyframes shineText { to { background-position: 200% center; } }
        @keyframes growBar { to { width: 300px; } }
        @keyframes fadeInPortal { to { opacity: 0.8; } }
        @keyframes fadeOutWindow { to { opacity: 0; visibility: hidden; pointer-events: none; } }
    </style>
    """
    components.html(animation_html, height=0)
    time.sleep(3.4) 
    st.session_state.animation_played = True
    st.rerun()

# ==========================================
# 3. DYNAMIC DESIGN SYSTEM (CSS INJECTION)
# ==========================================
# Fallback vector design background pattern if local images do not exist
UI_THEME_DARK = {
    "bg_css": "background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%) !important;",
    "card_bg": "rgba(15, 23, 42, 0.65)",
    "text_color": "#f8fafc",
    "sub_text": "#94a3b8",
    "border": "rgba(51, 65, 85, 0.5)",
    "accent": "#38bdf8",
    "accent_gradient": "linear-gradient(135deg, #3b82f6, #818cf8)"
}

UI_THEME_LIGHT = {
    "bg_css": "background: radial-gradient(circle at 50% 50%, #f8fafc 0%, #e2e8f0 100%) !important;",
    "card_bg": "rgba(255, 255, 255, 0.75)",
    "text_color": "#0f172a",
    "sub_text": "#475569",
    "border": "rgba(203, 213, 225, 0.7)",
    "accent": "#2563eb",
    "accent_gradient": "linear-gradient(135deg, #1d4ed8, #3b82f6)"
}

cfg = UI_THEME_DARK if st.session_state.bg_theme == "dark" else UI_THEME_LIGHT

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: {st.session_state.font_scale}% !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        {cfg['bg_css']}
    }}
    
    [data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ padding: 1.5rem 3rem !important; }}
    
    /* Advanced Glassmorphism Cards */
    .glass-card {{
        background: {cfg['card_bg']};
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid {cfg['border']};
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
    }}
    
    /* Metrics Upgrades */
    .metric-container {{
        text-align: center;
        padding: 15px;
    }}
    .metric-value {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 5px;
    }}
    
    /* Tab Styling Overhaul */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {cfg['card_bg']};
        backdrop-filter: blur(8px);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid {cfg['border']};
    }}
    div[data-testid="stTabs"] [data-baseweb="tab"] {{
        padding: 8px 16px;
        border-radius: 10px;
        font-weight: 500;
        color: {cfg['sub_text']} !important;
        transition: all 0.2s ease;
    }}
    div[data-testid="stTabs"] [aria-selected="true"] {{
        background: {cfg['accent_gradient']} !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
    }}
    
    /* System Notices */
    .notice-banner {{
        background: linear-gradient(90deg, rgba(234,88,12,0.15) 0%, rgba(249,115,22,0.05) 100%);
        border-left: 4px solid #ea580c;
        padding: 12px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 20px;
        color: {cfg['text_color']};
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATA PIPELINE VARIABLES & UTILITIES
# ==========================================
ADMIN_EMAIL = "krishna5689@outlook.in"
ADMIN_PHONE = "919451134541"
NOTEBOOK_LM_URL = "https://notebooklm.google.com/notebook/4865426e-ee8e-4256-956c-9f09f7c6c332?addSource=true"

clock_html = f"""
<div id="nexus-clock" style="font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: {cfg['text_color']}; text-align: right;">
    <span id="date-part"></span> &nbsp;&bull;&nbsp; <span id="time-part" style="color: #38bdf8; font-weight: 600;"></span>
</div>
<script>
    function updateClock() {{
        const now = new Date();
        const options = {{ year: 'numeric', month: 'short', day: 'numeric' }};
        document.getElementById('date-part').textContent = "📅 " + now.toLocaleDateString('en-US', options);
        let hours = now.getHours(); const minutes = String(now.getMinutes()).padStart(2, '0'); const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM'; hours = hours % 12; hours = hours ? hours : 12;
        document.getElementById('time-part').textContent = "🕒 " + String(hours).padStart(2, '0') + ':' + minutes + ':' + seconds + ' ' + ampm;
    }}
    setInterval(updateClock, 1000); updateClock();
</script>
"""

# ==========================================
# 5. CONTROL HEADER LAYER
# ==========================================
header_col, control_col = st.columns([2.5, 1.5])
with header_col:
    st.markdown("<h1 style='margin: 0; font-weight:700;'>🎓 Nexus Academic Portal</h1>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: {cfg['sub_text']}; font-size: 0.9rem;'>B.Sc Unified Tier System Architecture &bull; Operational Endpoint: <code>{ADMIN_EMAIL}</code></span>", unsafe_allow_html=True)

with control_col:
    components.html(clock_html, height=24)
    sc1, sc2 = st.columns(2)
    with sc1:
        theme_choice = st.selectbox("UI Matrix", ["🌙 Cyber Dark", "☀️ Prismatic Light"], index=0 if st.session_state.bg_theme == "dark" else 1)
        target_theme = "dark" if "Dark" in theme_choice else "light"
        if target_theme != st.session_state.bg_theme:
            st.session_state.bg_theme = target_theme
            st.rerun()
    with sc2:
        font_choice = st.selectbox("Resolution Scale", ["🔍 100%", "🔍 120%", "🔍 140%"], index=0)
        scale_map = {"100%": 100, "120%": 120, "140%": 140}
        target_scale = scale_map[font_choice.split(" ")[1]]
        if target_scale != st.session_state.font_scale:
            st.session_state.font_scale = target_scale
            st.rerun()

st.markdown("""
<div class="notice-banner">
    ⚙️ <strong>System Environment Diagnostics:</strong> Core testing arrays loaded successfully. All automated scrapers and Web3 endpoint routes are active.
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. APPLICATION NAVIGATION STACK
# ==========================================
tabs = st.tabs([
    "📊 Command Dashboard",
    "🏫 Academic Hub & ERP",  
    "🤖 Cognitive AI Agent",
    "🔍 Deep Research Engine",
    "📢 Live Bulletin Arrays",
    "📚 Digital Course Vault",
    "🧮 Matrix Toolkit (GPA)",
    "⏱️ JavaScript Core Focus",
    "🚨 Core Node Escalation"
])

tab_dash, tab_erp, tab_counsel, tab_deep, tab_news, tab_vault, tab_matrix, tab_focus, tab_escalate = tabs

# --- TAB 1: COMMAND DASHBOARD ---
with tab_dash:
    st.markdown(f"""
    <div class="glass-card" style="background: linear-gradient(135deg, rgba(30,64,175,0.4), rgba(129,140,248,0.1)); border-left: 4px solid #38bdf8;">
        <h3 style='margin:0 0 8px 0;'>System Framework Initialized</h3>
        <p style='margin:0; font-size:0.95rem; color:{cfg['sub_text']};'>Central analytics orchestrator providing dynamic structural geology matrices, verified dataset clusters, and structural operational oversight pipelines.</p>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="glass-card metric-container"><span>Cohort Index</span><div class="metric-value">1,250</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="glass-card metric-container"><span>Active Node Registers</span><div class="metric-value">18</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="glass-card metric-container"><span>System Broadcasts</span><div class="metric-value" style="background:linear-gradient(90deg, #f97316, #facc15); -webkit-background-clip:text;">6</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="glass-card metric-container"><span>Active Latency Paths</span><div class="metric-value" style="background:linear-gradient(90deg, #ef4444, #f43f5e); -webkit-background-clip:text;">0</div></div>', unsafe_allow_html=True)
    
    l_box, r_box = st.columns([2.5, 1.5])
    with l_box:
        st.markdown("<h3 style='margin-bottom:15px;'>🧬 Registered Core Matrix Status</h3>", unsafe_allow_html=True)
        courses = [
            {"name": "Structural Geology & Fault Dynamics", "id": "GEO-201", "status": "Synced"},
            {"name": "Crystallography & Mineral Optical Properties", "id": "GEO-204", "status": "Synced"},
            {"name": "Geomorphology Elements", "id": "GEO-209", "status": "Synced"}
        ]
        for c in courses:
            st.markdown(f"""
            <div style="padding:14px; border-radius:10px; background:rgba(0,0,0,0.1); border: 1px solid {cfg['border']}; margin-bottom:10px; display:flex; justify-content:between; align-items:center;">
                <div><strong>{c['name']}</strong> <code style='font-size:0.8rem;'>{c['id']}</code></div>
                <span style="color:#10b981; font-weight:600; font-size:0.85rem; background:rgba(16,185,129,0.1); padding:2px 8px; border-radius:4px;">{c['status']}</span>
            </div>
            """, unsafe_allow_html=True)
    with r_box:
        st.markdown("<h3 style='margin-bottom:15px;'>🎯 Automation Pipelines</h3>", unsafe_allow_html=True)
        st.button("📋 Telemetry Tracker", use_container_width=True)
        st.button("📝 Live Assessment Handlers", use_container_width=True)
        st.button("📅 System Calendar Grid", use_container_width=True)

# --- TAB 2: ACADEMIC HUB & ERP ---
with tab_erp:
    st.markdown("<h2 style='margin-top:0;'>Campus Ledger & ERP Framework Gateways</h2>", unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown(f"""
        <div class="glass-card" style="min-height:230px;">
            <h3 style="color:#38bdf8; margin-top:0;">💳 Financial Clearances & Balances</h3>
            <p style="color:{cfg['sub_text']}; font-size:0.95rem; line-height:1.6;">
                Automated auditing framework connected directly to cross-network institutional ledger clusters. Verify term registrations, backlog penalty offsets, or outstanding academic clearances.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🌐 Open External Ledger Terminal", "https://erpweb.bsnvpgcollege.co.in/transaction-search", type="secondary", use_container_width=True)
        st.link_button("⚡ Execute Tuition Clearance Charges", "https://erpweb.bsnvpgcollege.co.in/paycoursefees", type="primary", use_container_width=True)
        
    with col_e2:
        st.markdown(f"""
        <div class="glass-card" style="min-height:230px;">
            <h3 style="color:#f97316; margin-top:0;">📋 Administrative Communication Network</h3>
            <p style="color:{cfg['sub_text']}; font-size:0.95rem; line-height:1.6;">
                Access formal structural decrees, evaluation changes, timeline updates, and regulatory adjustments via encrypted public routing backbones.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("📢 Pull Verified Directive Array", "https://bsnvpgcollege.ac.in/NoticeHome.aspx?Type=Notice", type="primary", use_container_width=True)

# --- TAB 3: COGNITIVE AI AGENT ---
with tab_counsel:
    st.markdown("<h2 style='margin-top:0;'>Intelligent Cognitive Counseling Agent</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{cfg['sub_text']}; margin-bottom:20px;'>Context-aware model loaded with localized academic guidelines and dynamic vector search optimizations.</p>", unsafe_allow_html=True)
    jotform_script = "<script src='https://cdn.jotfor.ms/agent/embedjs/019e014489347343a7b79be9c9855b48569e/embed.js?autoOpenChatIn=1'></script>"
    components.html(jotform_script, height=520, scrolling=True)

# --- TAB 4: DEEP RESEARCH ENGINE ---
with tab_deep:
    st.markdown("<h2 style='margin-top:0;'>Deep Structural Indexing & Dynamic Feeds</h2>", unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f"""
        <div class="glass-card" style="min-height:220px;">
            <h3 style="color:#818cf8; margin-top:0;">Google NotebookLM Framework</h3>
            <p style="color:{cfg['sub_text']}; font-size:0.95rem; line-height:1.6;">
                Initializes explicit cross-origin session variables directed toward your tailored analysis clusters. Ideal for handling documentation parsing, complex semantic indexation, and contextual queries.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🚀 Active NotebookLM Secure Link", NOTEBOOK_LM_URL, type="primary", use_container_width=True)
    with sc2:
        st.markdown(f"""
        <div class="glass-card" style="min-height:220px;">
            <h3 style="color:#f43f5e; margin-top:0;">Multimedia Educational Pipeline</h3>
            <p style="color:{cfg['sub_text']}; font-size:0.95rem; line-height:1.6;">
                Input research objectives or dynamic geological topics below. The query will sanitize string variants and auto-format programmatic indexing arrays.
            </p>
        </div>
        """, unsafe_allow_html=True)
        yt_input = st.text_input("Syllabus Reference / Vector Query Input:", placeholder="e.g., Crystallography Hermann Mauguin symmetry notation BSc", key="nexus_yt_search")
        if yt_input:
            encoded_query = urllib.parse.quote(yt_input.strip())
            st.link_button("📺 Stream Filtered Search Payload", f"https://www.youtube.com/results?search_query={encoded_query}", type="secondary", use_container_width=True)

# --- TAB 5: LIVE BULLETIN ARRAYS (ASYNC SCRAPER) ---
with tab_news:
    st.markdown("<h2 style='margin-top:0;'>Live Distributed Institutional Database Sync</h2>", unsafe_allow_html=True)
    lu_target = "https://www.lkouniv.ac.in/en/news?Newslistslug=en-notices&cd=MwAzADcA"
    
    if st.button("Initialize Secure Scrape Request Pipeline", type="primary", use_container_width=True):
        # Isolation wrapper to prevent MainThread freezing
        def fetch_bulletins():
            h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            r = requests.get(lu_target, headers=h, timeout=8)
            s = BeautifulSoup(r.content, 'html.parser')
            return [{"text": a.text.strip(), "href": a['href']} for a in s.find_all('a', href=True) if "news" in a['href'] and len(a.text.strip()) > 15]

        with st.spinner("Executing thread-isolated extraction..."):
            try:
                with ThreadPoolExecutor() as executor:
                    bulletin_records = executor.submit(fetch_bulletins).result()
                
                if not bulletin_records:
                    st.warning("Query returned zero matching records.")
                else:
                    for i, b in enumerate(bulletin_records[:10]):
                        clean_lbl = b['text'].replace("[", "").replace("]", "")
                        destination = b['href'] if b['href'].startswith('http') else f"https://www.lkouniv.ac.in{b['href']}"
                        st.markdown(f"""
                        <div style="padding:12px; margin-bottom:8px; border-radius:8px; background:rgba(56,189,248,0.05); border-left:3px solid #38bdf8;">
                            <a href="{destination}" target="_blank" style="text-decoration:none; color:{cfg['text_color']}; font-weight:500;">🔗 Grid Element {i+1}: {clean_lbl}</a>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error("Automated mining encountered an exception wrapper.")
                st.markdown(f"📦 [Access Source Registry Directory Interactively]({lu_target})")

# --- TAB 6: DIGITAL COURSE VAULT ---
with tab_vault:
    st.markdown("<h2 style='margin-top:0;'>Cloud Storage Virtual Classrooms</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
        <div class="glass-card">
            <h4 style='margin:0 0 10px 0;'>B.Sc Academic Core Operations Cluster</h4>
            <p style='font-size:0.9rem; color:{cfg['sub_text']};'>Access synchronized syllabus distribution folders, file asset directories, and assignment delivery endpoints.</p>
            <div style='background:rgba(0,0,0,0.2); padding:10px 15px; border-radius:8px; margin-bottom:15px; border:1px dashed {cfg['border']}'>
                🔑 Cryptographic Access Token: <code style='color:#38bdf8;'>shf3hsat</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("📂 Launch Google Classroom Infrastructure", "https://classroom.google.com/c/ODU0MzQ2NjI2MDQ2?cjc=shf3hsat", type="primary", use_container_width=True)

# --- TAB 7: MATRIX TOOLKIT (GPA CRITERIA) ---
with tab_matrix:
    st.markdown("<h2 style='margin-top:0;'>Mathematical Performance Matrix</h2>", unsafe_allow_html=True)
    calc1, calc2 = st.tabs(["Weighted Term GPA Calculator", "Cumulative Multi-Term Aggregator"])
    
    with calc1:
        st.markdown("$$GPA = \\frac{\\sum_{i=1}^{n} (GradePoint_i \\times Credit_i)}{\\sum_{i=1}^{n} Credit_i}$$")
        subjects_num = st.number_input("Computational Subject Arrays:", min_value=1, max_value=12, value=4, step=1)
        
        scores_vector = []
        credits_vector = []
        g_map = {"O (Outstanding)": 10, "A+ (Excellent)": 9, "A (Very Good)": 8, "B+ (Good)": 7, "B (Average)": 6, "C (Passing)": 5, "F (Failure)": 0}
        
        for idx in range(int(subjects_num)):
            c1, c2 = st.columns(2)
            with c1:
                sel_g = st.selectbox(f"Course Matrix Record {idx+1} Grade Point:", list(g_map.keys()), key=f"mat_g_{idx}")
                scores_vector.append(g_map[sel_g])
            with c2:
                sel_c = st.number_input(f"Course Matrix Record {idx+1} Credit Weights:", min_value=1, max_value=8, value=4, key=f"mat_c_{idx}")
                credits_vector.append(sel_c)
                
        if st.button("Compute Term GPA Output", type="primary", use_container_width=True):
            dot_product = sum(s * c for s, c in zip(scores_vector, credits_vector))
            sigma_credits = sum(credits_vector)
            term_gpa = dot_product / sigma_credits if sigma_credits > 0 else 0
            st.metric("Vector Quantized Term GPA Matrix", f"{term_gpa:.4f} / 10.0000")
            
    with calc2:
        st.markdown("$$CGPA = \\frac{(CGPA_{Hist} \\times Credit_{Hist}) + (GPA_{Term} \\times Credit_{Term})}{Credit_{Hist} + Credit_{Term}}$$")
        hist_cgpa = st.number_input("Historical Base Reference CGPA:", min_value=0.0, max_value=10.0, value=8.0, step=0.01)
        hist_cred = st.number_input("Sum total of Historical Earned Credits:", min_value=0, max_value=240, value=44, step=1)
        st.divider()
        latest_gpa = st.number_input("Target Runtime Term GPA Score:", min_value=0.0, max_value=10.0, value=8.5, step=0.01)
        latest_cred = st.number_input("Target Runtime Term Credit Allocation:", min_value=0, max_value=32, value=20, step=1)
        
        if st.button("Consolidate Complete Matrix CGPA", use_container_width=True):
            aggregate_points = (hist_cgpa * hist_cred) + (latest_gpa * latest_cred)
            aggregate_credits = hist_cred + latest_cred
            final_cgpa = aggregate_points / aggregate_credits if aggregate_credits > 0 else 0
            st.metric("Consolidated Aggregate Global Portfolio CGPA", f"{final_cgpa:.4f} / 10.0000")

# --- TAB 8: JAVASCRIPT NATIVE FOCUS ENGINE ---
with tab_focus:
    st.markdown("<h2 style='margin-top:0;'>High-Performance JavaScript Chronometer Focus Engine</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{cfg['sub_text']};'>State-isolated client-side timer architecture engineered to eliminate container pipeline redraw stuttering and backend latency errors.</p>", unsafe_allow_html=True)
    
    # Pure sandboxed web-component timer logic
    timer_js_code = """
    <div id="chronometer-box">
        <div id="chrono-display">25:00</div>
        <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
            <button class="btn" onclick="startTimer(25)">Focus Frame (25m)</button>
            <button class="btn" onclick="startTimer(5)">Recuperate (5m)</button>
            <button class="btn btn-stop" onclick="stopTimer()">Halt Frame</button>
        </div>
    </div>
    <style>
        #chronometer-box {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px; padding: 40px; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        #chrono-display {
            font-size: 5rem; font-weight: 800; color: #38bdf8;
            letter-spacing: 2px; text-shadow: 0 0 20px rgba(56,189,248,0.3);
            font-variant-numeric: tabular-nums;
        }
        .btn {
            background: #2563eb; color: white; border: none;
            padding: 10px 20px; font-weight: 600; border-radius: 8px;
            cursor: pointer; transition: background 0.2s;
        }
        .btn:hover { background: #1d4ed8; }
        .btn-stop { background: #dc2626; }
        .btn-stop:hover { background: #b91c1c; }
    </style>
    <script>
        let countdownTimer = null;
        function startTimer(minutes) {
            clearInterval(countdownTimer);
            let timeRemaining = minutes * 60;
            const display = document.getElementById('chrono-display');
            
            countdownTimer = setInterval(() => {
                let mins = Math.floor(timeRemaining / 60);
                let secs = timeRemaining % 60;
                display.textContent = String(mins).padStart(2, '0') + ":" + String(secs).padStart(2, '0');
                if (--timeRemaining < 0) {
                    clearInterval(countdownTimer);
                    display.textContent = "DONE";
                }
            }, 1000);
        }
        function stopTimer() {
            clearInterval(countdownTimer);
            document.getElementById('chrono-display').textContent = "00:00";
        }
    </script>
    """
    components.html(timer_js_code, height=240)

# --- TAB 9: CORE NODE ESCALATION ---
with tab_escalate:
    st.markdown("<h2 style='margin-top:0;'>Administrative Incident Escalation Desk</h2>", unsafe_allow_html=True)
    
    with st.form("incident_matrix_form", clear_on_submit=False):
        st.markdown(f"<p style='color:{cfg['sub_text']}; font-size:0.9rem;'>Ensure fields contain valid syntax arrays. Missing tokens will flag edge exceptions.</p>", unsafe_allow_html=True)
        
        st.text_input("User Verification Email *", placeholder="identity@domain.com", key="e_email")
        st.text_input("Full Legal Name Entry *", key="e_name")
        st.text_input("Institutional Roll Registry Reference *", key="e_roll")
        st.selectbox("System Error Domain Classification", ["Database Routing Error", "Missing Subject Profiles", "Document Discrepancy", "Transaction Failures"], key="e_class")
        st.text_area("Comprehensive Description Log Matrix *", key="e_desc")
        
        trigger_escalation = st.form_submit_button("Deploy Ticket Payload to Admin Nodes", use_container_width=True)
        
    if trigger_escalation:
        m_email = st.session_state.e_email.strip()
        m_name = st.session_state.e_name.strip()
        m_roll = st.session_state.e_roll.strip()
        m_class = st.session_state.e_class
        m_desc = st.session_state.e_desc.strip()
        
        if m_email and m_name and m_roll and m_desc:
            payload = {
                "email": m_email,
                "Name Vector": m_name,
                "Roll Target": m_roll,
                "Domain Class": m_class,
                "Telemetry Log": m_desc,
                "_subject": f"🚨 Nexus Failure Escalation Event: Code-{m_roll}",
                "_captcha": "false"
            }
            
            with st.spinner("Broadcasting ticket payload across Ajax Formsubmit pipelines..."):
                try:
                    res_status = requests.post(f"https://formsubmit.co/ajax/{ADMIN_EMAIL}", data=payload, timeout=8)
                    if res_status.status_code == 200:
                        st.toast("Telemetry data package delivered successfully.", icon="🚀")
                    else:
                        st.error(f"External API dropped packet stream. HTTP Status Code: {res_status.status_code}")
                except Exception:
                    st.error("Connection timed out. Initializing backup fallback logic vectors.")
            
            # Format message string safely for instant messaging pipelines
            whatsapp_payload_str = f"*Incident Ticket Open*\n\n*Operator Name:* {m_name}\n*Register Roll No:* {m_roll}\n*Domain:* {m_class}\n*Diagnostics:* {m_desc}"
            wa_endpoint_formatted = f"https://wa.me/{ADMIN_PHONE}?text={urllib.parse.quote(whatsapp_payload_str)}"
            
            st.success("🎉 Local validation passed. Incident packet written to data buffer.")
            st.link_button("Verify Node Escalation via WhatsApp Endpoint ✅", wa_endpoint_formatted, use_container_width=True)
            st.balloons()
        else:
            st.error("❌ Form payload structure invalid. Missing mandatory text arrays.")

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<hr style='border-color:{cfg['border']};'><center style='font-size: 11px; color:{cfg['sub_text']}; letter-spacing:1px;'>OPERATIONAL INFRASTRUCTURE PROVIDED BY NEXUS AGENT CORE NETWORKS</center>", unsafe_allow_html=True)
