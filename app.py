import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra Multi-Stream AI 🎓", page_icon="🚀", layout="wide")

DEFAULT_TOKEN = "AQ.Ab8RN6KPeVyNXJrhwzkxqoaqH0rH2hRSa3W4BCudsQMSeOZjWg"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_TOKEN
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra Multi-Stream 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 🚀 వన్-టైమ్ లాగిన్ సిస్టమ్ ---
if "user" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.user_email = st.query_params["user"]
else:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

if not st.session_state.logged_in:
    st.markdown(f"<h1 style='text-align: center;'>🔐 Login to {st.session_state.app_name}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email_input = st.text_input("📧 Email Address")
        password_input = st.text_input("🔑 Password", type="password")
        if st.button("🚀 Login", use_container_width=True):
            if email_input and password_input:
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.query_params["user"] = email_input 
                st.rerun()
            else:
                st.error("బాస్, ఈమెయిల్ మరియు పాస్‌వర్డ్ కచ్చితంగా ఇవ్వాలి!")
    st.stop()

# --- ⚙️ సైడ్‌బార్ & ఎడ్యుకేషన్ స్ట్రీమ్ సెలెక్టర్ ---
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            new_token = st.text_input("Token / Key:", st.session_state.api_key, type="password")
            
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.session_state.api_key = new_token
                st.rerun()
                
    st.divider()
    
    # అన్ని ఎడ్యుకేషన్ సిస్టమ్స్ డ్రాప్‌డౌన్
    education_stream = st.selectbox("📚 Select Education Stream:", [
        "⚡ Engineering (B.Tech / EEE / CSE)", 
        "💊 Pharmacy (B.Pharm / Pharm.D)", 
        "🩺 Nursing (B.Sc / General Nursing)", 
        "📈 MBA (Management & Business)"
    ])
    
    st.divider()
    
    app_mode = st.radio("Select Feature:", [
        "🤖 Project & Lab Guide", 
        "🎪 Event Planner", 
        "📚 Exam Hacker", 
        "💼 Placement Prep"
    ])
    st.divider()
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.query_params.clear()
        st.rerun()

# --- 🧠 అన్ని ఎడ్యుకేషన్ సిస్టమ్స్ కోసం స్మార్ట్ మల్టీ-బ్రాంచ్ రెస్పాన్స్ ఇంజిన్ ---
def get_multistream_answer(stream, prompt):
    text_lower = prompt.lower()
    
    if "engineering" in stream.lower():
        if "plc" in text_lower or "automation" in text_lower:
            return """### ⚡ Engineering Lab Report: PLC Automation
**1. Aim:** To study the architecture and ladder logic programming of Programmable Logic Controllers (PLC) in industrial automation.
**2. Apparatus Required:** PLC Trainer Kit, Input switches, Output actuators, Programming Cable, and PC with software.
**3. Theory:** PLCs monitor input signals from field sensors, process the user program (Ladder Logic), and control industrial machinery safely and efficiently."""
        else:
            return f"""### ⚡ Engineering Technical Guide ({prompt})
**1. Core Principles:** Focuses on circuit analysis, software/hardware design principles, efficiency optimization, and standard industrial protocols.
**2. Implementation:** Utilizes structured mathematical modeling, microcontroller/programming logic, and rigorous testing methodologies to ensure structural reliability."""

    elif "pharmacy" in stream.lower():
        if "tablet" in text_lower or "capsule" in text_lower or "drug" in text_lower:
            return """### 💊 Pharmacy Lab Guide: Tablet Compression & Evaluation
**1. Objective:** To formulate and evaluate pharmaceutical tablets for weight variation, hardness, friability, and disintegration time.
**2. Materials:** Active Pharmaceutical Ingredient (API), binders (Starch, PVP), lubricants (Magnesium stearate), and disintegrants.
**3. Evaluation Tests:** 
* *Hardness Test:* Measures tablet breaking force using Monsanto or Pfizer tester.
* *Friability Test:* Evaluates resistance to surface abrasion using Roche friabilator."""
        else:
            return f"""### 💊 Pharmacy Academic Overview ({prompt})
**1. Pharmacology & Pharmaceutics:** Studies drug action mechanisms, pharmacokinetics, pharmacodynamics, and dosage form design.
**2. Quality Control:** Ensures drug safety, stability testing, regulatory compliance (FDA/ICH guidelines), and therapeutic efficacy."""

    elif "nursing" in stream.lower():
        if "first aid" in text_lower or "patient" in text_lower or "vital" in text_lower:
            return """### 🩺 Nursing Clinical Guide: Vital Signs & Patient Assessment
**1. Core Assessment Parameters:** Monitoring temperature, pulse rate, respiration rate, and blood pressure (TPR & BP).
**2. Clinical Procedure:** 
* Maintain sterile techniques and hand hygiene.
* Record baseline observations accurately in patient charts.
* Report sudden deviations to the attending physician immediately."""
        else:
            return f"""### 🩺 Nursing Care & Clinical Study ({prompt})
**1. Patient-Centric Care:** Focuses on holistic nursing care, patient monitoring, medication administration protocols, and emergency response management.
**2. Ethics & Safety:** Adheres strictly to patient confidentiality, infection control standards, and clinical safety guidelines."""

    elif "mba" in stream.lower():
        if "marketing" in text_lower or "finance" in text_lower or "management" in text_lower:
            return """### 📈 MBA Executive Case Study: Strategic Management
**1. Executive Summary:** Analysis of market positioning, competitive advantage, financial resource allocation, and consumer behavior.
**2. SWOT Analysis:** Evaluating Strengths, Weaknesses, Opportunities, and Threats to formulate long-term corporate growth strategies."""
        else:
            return f"""### 📈 Business & Management Analysis ({prompt})
**1. Strategic Frameworks:** Analyzes market dynamics, operational logistics, supply chain management, and financial budgeting.
**2. Decision Making:** Uses data-driven analytics and leadership methodologies to optimize organizational performance."""

    else:
        return f"""### 📚 Academic & Project Reference: {prompt}
* **Stream Selected:** {stream}
* **Comprehensive Overview:** Detailed theoretical analysis, standard practical frameworks, and technical evaluation metrics tailored for advanced academic curricula."""

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} - {education_stream.split()[1]} Lab Guide")
    
    tab1, tab2, tab3 = st.tabs(["💬 Text Chat", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab2:
        uploaded_file = st.file_uploader("లాబ్ మాన్యువల్ లేదా ఫోటో అప్‌లోడ్ చేయండి", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_to_send = Image.open(uploaded_file)
            st.image(img_to_send, caption="అప్‌లోడ్ చేసిన ఇమేజ్", width=300)
    with tab3:
        camera_photo = st.camera_input("ఫోటో తీయండి")
        if camera_photo:
            img_to_send = Image.open(camera_photo)
            st.image(img_to_send, caption="కెమెరా ఫోటో", width=300)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(f"Ask your {education_stream.split()[1]} doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("వివరణాత్మక ఆన్సర్ సిద్ధం అవుతోంది... ⏳"):
            reply_text = get_multistream_answer(education_stream, prompt)
            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header(f"🎪 {education_stream.split()[1]} Event & Workshop Planner")
    st.info(f"{education_stream.split()[1]} డిపార్ట్‌మెంట్ ఈవెంట్స్ మరియు సెమినార్ల ప్లానింగ్ కోసం.")

elif app_mode == "📚 Exam Hacker":
    st.header(f"📚 {education_stream.split()[1]} Exam Hacker")
    st.info("ఇంపార్టెంట్ ఎగ్జామ్ క్వశ్చన్స్ మరియు లాస్ట్ మినిట్ రివిజన్ నోట్స్.")

elif app_mode == "💼 Placement Prep":
    st.header(f"💼 {education_stream.split()[1]} Placement & Career Prep")
    st.info("స్పెషలైజ్డ్ ఇంటర్వ్యూ క్వశ్చన్స్ మరియు ప్రిపరేషన్ గైడ్.")
