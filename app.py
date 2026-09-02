import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra Offline Pro 🎓", page_icon="🚀", layout="wide")

ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- మెమరీ సెటప్ ---
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra Pro 🎓"
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

# --- ⚙️ సైడ్‌బార్ & స్ట్రీమ్ సెలెక్షన్ ---
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.rerun()
                
    st.divider()
    
    education_stream = st.selectbox("📚 Select Stream:", [
        "⚡ Engineering (B.Tech / EEE / CSE)", 
        "💊 Pharmacy (B.Pharm / Pharm.D)", 
        "🩺 Nursing (B.Sc / GNM)", 
        "📈 MBA (Management)"
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

# --- 🧠 పక్కా కచ్చితమైన, పెద్ద ఆన్సర్స్ ఇచ్చే అడ్వాన్స్డ్ లోకల్ నాలెడ్జ్ ఇంజిన్ ---
def get_bulletproof_answer(stream, prompt):
    text = prompt.lower()
    
    # 1. ENGINEERING STREAM
    if "engineering" in stream.lower():
        if "cloud computing" in text or "cloud" in text:
            return """### ☁️ Cloud Computing: Architecture, Services, and Models

**1. Comprehensive Definition:**
Cloud computing is the on-demand delivery of computing services—including data storage, servers, databases, networking, software, and intelligence—over the Internet. It replaces local hardware storage with centralized remote data centers managed by cloud providers (e.g., AWS, Google Cloud, Microsoft Azure).

**2. Core Service Models (SPI Framework):**
* **IaaS (Infrastructure as a Service):** Provides fundamental computing infrastructure such as virtual machines, raw storage, and firewalls. *Examples: AWS EC2, Google Compute Engine.*
* **PaaS (Platform as a Service):** Offers a pre-built platform and deployment environment enabling developers to build, test, and manage applications without worrying about underlying hardware. *Examples: Google App Engine, Heroku.*
* **SaaS (Software as a Service):** Delivers fully operational software applications over the internet on a subscription basis, accessible via web browsers. *Examples: Google Workspace, Microsoft 365, Salesforce.*

**3. Key Advantages:**
* **Cost Efficiency:** Eliminates capital expenditure on physical data centers.
* **Elasticity & Scalability:** Resources can be scaled up or down instantaneously based on workload demands.
* **Disaster Recovery & Security:** Automated backups, multi-site replication, and robust encryption protect enterprise data."""
        
        elif "python" in text:
            return """### 🐍 Python Programming Language: Core Concepts & Applications

**1. Introduction:**
Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum in 1991. Its design philosophy emphasizes code readability through the significant use of indentation.

**2. Key Technical Features:**
* **Interpreted Nature:** Code is executed line by line, simplifying debugging and error tracking.
* **Dynamic Typing:** Variable data types are determined automatically at runtime without explicit declarations.
* **Extensive Ecosystem:** Rich standard library and thousands of open-source packages available via PyPI.

**3. Primary Industry Applications:**
* **Artificial Intelligence & Machine Learning:** Leading libraries like TensorFlow, PyTorch, Scikit-Learn, and Keras.
* **Web Development:** Robust backend frameworks like Django, Flask, and FastAPI.
* **Data Science & Automation:** Pandas and NumPy for advanced data manipulation and process automation."""

        elif "plc" in text or "automation" in text:
            return """### ⚡ Programmable Logic Controller (PLC) in Industrial Automation

**1. Overview:**
A Programmable Logic Controller (PLC) is a ruggedized industrial digital computer designed to control manufacturing processes, assembly lines, robotic cells, and critical infrastructure.

**2. Hardware Architecture:**
* **CPU (Central Processing Unit):** Evaluates input conditions, executes the user control program, and updates output states.
* **Memory:** Stores the operating system, user ladder programs, and data variables (RAM/ROM/EEPROM).
* **I/O Modules:** Interface between field devices (sensors, push buttons, actuators, motor starters) and the CPU.

**3. Programming Standard (IEC 61131-3):**
* **Ladder Logic (LD):** The most widespread graphical programming language resembling traditional electrical relay schematics.
* **Structured Text (ST):** High-level textual language similar to Pascal or C."""

    # 2. PHARMACY STREAM
    elif "pharmacy" in stream.lower():
        if "tablet" in text or "capsule" in text or "drug" in text:
            return """### 💊 Pharmaceutical Dosage Forms: Tablet Manufacturing & Evaluation

**1. Definition of Tablets:**
Solid unit dosage forms containing one or more active pharmaceutical ingredients (APIs) with or without excipients, prepared by compression molding or heavy-duty punch presses.

**2. Critical Quality Control (QC) Evaluation Tests:**
* **Hardness Test:** Measures tablet breaking resistance to withstand mechanical shocks during packaging and transport (Tested via Monsanto or Pfizer testers).
* **Friability Test:** Evaluates surface abrasion resistance by tumbling tablets in a Roche friabilator at 25 RPM for 4 minutes. Weight loss should be less than 1%.
* **Disintegration Test:** Measures the time required for solid tablets to break down into tiny particles in simulated gastric fluid at 37°C."""
        else:
            return f"""### 💊 Pharmacy Academic Overview: {prompt}
* **Core Principles:** Focuses on drug formulation science, pharmacokinetics, medicinal chemistry, and regulatory compliance (FDA/ICH standards).
* **Practical Application:** Ensures therapeutic efficacy, chemical stability, safe dosage delivery, and quality assurance in pharmaceutical manufacturing."""

    # 3. NURSING STREAM
    elif "nursing" in stream.lower():
        if "vital" in text or "patient" in text or "assessment" in text:
            return """### 🩺 Clinical Nursing: Patient Vital Signs Assessment & Protocols

**1. Core Vital Parameters (TPR & BP):**
* **Body Temperature:** Reflects the balance between heat produced and heat lost by the body (Normal: 98.6°F / 37°C).
* **Pulse Rate:** Palpation of arterial walls (radial or carotid) measuring heart beats per minute (Normal: 60–100 bpm).
* **Respiration Rate:** Counting unannounced breathing cycles per minute (Normal: 12–20 breaths/min).
* **Blood Pressure (BP):** Measured via sphygmomanometer and stethoscope (Normal systolic/diastolic: 120/80 mmHg).

**2. Clinical Responsibilities:**
* Strictly maintain sterile asepsis and hand hygiene protocols.
* Accurately document baseline measurements in patient clinical charts.
* Report sudden clinical deteriorations immediately to the attending physician."""
        else:
            return f"""### 🩺 Nursing Care Study: {prompt}
* **Patient-Centric Approach:** Emphasizes holistic clinical care, precise medication administration, and continuous health monitoring.
* **Safety & Ethics:** Adheres to patient confidentiality, infection control mandates, and emergency intervention standards."""

    # 4. MBA STREAM
    elif "mba" in stream.lower():
        if "marketing" in text or "strategy" in text or "management" in text:
            return """### 📈 MBA Executive Framework: Strategic Management & Marketing

**1. SWOT Strategic Analysis:**
* **Internal Factors:** Evaluating organizational **Strengths** and **Weaknesses** (resources, core competencies, operational bottlenecks).
* **External Factors:** Assessing market **Opportunities** and **Threats** (competitor behavior, regulatory shifts, economic trends).

**2. Marketing Mix (The 4 Ps):**
* **Product:** Core features, quality, branding, and packaging.
* **Price:** Cost-plus pricing, value-based pricing, and discounting strategies.
* **Place:** Distribution channels, logistics, and retail positioning.
* **Promotion:** Advertising, digital marketing, public relations, and sales promotions."""
        else:
            return f"""### 📈 Business & Management Analysis: {prompt}
* **Core Framework:** Analyzes market dynamics, financial budgeting, supply chain logistics, and organizational behavior.
* **Executive Decision Making:** Utilizes quantitative data analytics and leadership models to drive long-term corporate profitability and competitive advantage."""

    # GENERAL FALLBACK FOR ANY TOPIC
    return f"""### 📚 Comprehensive Academic & Technical Report: {prompt}

**1. Executive Summary & Core Concept:**
* The selected topic **'{prompt}'** is an essential part of the **{stream}** curriculum. 
* It involves structured theoretical investigation, rigorous methodology, and standard practical application.

**2. Technical Parameters & Architecture:**
* **System Design:** Integrates functional workflows to streamline operations and ensure high reliability.
* **Performance Metrics:** Focuses on minimizing operational errors, optimizing resource utilization, and maximizing efficiency.

**3. Practical Applications & Scope:**
* Extensively applied across modern professional industries, academic lab research, and institutional projects."""

# --- Main Screen Layout ---
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
        
        with st.spinner("వివరణాత్మక నోట్స్ సిద్ధం అవుతోంది... ⏳"):
            reply_text = get_bulletproof_answer(education_stream, prompt)
            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header(f"🎪 {education_stream.split()[1]} Event & Workshop Planner")
    st.info(f"{education_stream.split()[1]} డిపార్ట్‌మెంట్ ఈవెంట్స్, సెమినార్లు మరియు వర్క్‌షాప్స్ ప్లానింగ్.")

elif app_mode == "📚 Exam Hacker":
    st.header(f"📚 {education_stream.split()[1]} Exam Hacker")
    st.info("ఇంపార్టెంట్ ఎగ్జామ్ క్వశ్చన్స్ మరియు లాస్ట్ మినిట్ రివిజన్ నోట్స్.")

elif app_mode == "💼 Placement Prep":
    st.header(f"💼 {education_stream.split()[1]} Placement & Career Prep")
    st.info("స్పెషలైజ్డ్ ఇంటర్వ్యూ క్వశ్చన్స్ మరియు ప్రిపరేషన్ గైడ్.")
