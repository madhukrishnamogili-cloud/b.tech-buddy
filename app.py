import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra Long-Format Pro 🎓", page_icon="🚀", layout="wide")

ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra Pro 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- లాగిన్ సిస్టమ్ ---
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
                st.error("ఈమెయిల్ మరియు పాస్‌వర్డ్ కచ్చితంగా ఇవ్వాలి!")
    st.stop()

# --- సైడ్‌బార్ ---
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

# --- 🧠 చాలా పెద్దవిగా, పక్కాగా లాంగ్ ఆన్సర్స్ ఇచ్చే అడ్వాన్స్డ్ ఇంజిన్ ---
def get_long_comprehensive_answer(stream, prompt):
    text = prompt.lower()
    
    # 1. ENGINEERING STREAM (Long Answers)
    if "engineering" in stream.lower():
        if "cloud computing" in text or "cloud" in text:
            return """### ☁️ Comprehensive Study Report: Cloud Computing Architecture & Ecosystem

**1. Introduction & Theoretical Background:**
Cloud computing represents a paradigm shift in how information technology is consumed and managed. Instead of maintaining local physical servers and data storage facilities, organizations rent access to storage, processing power, and applications from hyperscale cloud providers such as Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). This eliminates capital expenditure (CapEx) and introduces a flexible operational expenditure (OpEx) model based on actual consumption.

**2. Detailed Breakdown of Service Models (SPI Framework):**
* **Infrastructure as a Service (IaaS):** 
  * *Description:* Serves as the foundational layer where providers supply virtualized computing resources over the public internet. Users have absolute control over operating systems, storage, and deployed applications without managing physical hardware racks.
  * *Key Examples:* Amazon EC2, Google Compute Engine, Microsoft Azure Virtual Machines.
* **Platform as a Service (PaaS):** 
  * *Description:* Delivers a robust framework and managed environment designed specifically for software developers. It abstracts underlying server maintenance, letting teams focus strictly on writing application code, testing algorithms, and database management.
  * *Key Examples:* Google App Engine, Heroku, AWS Elastic Beanstalk.
* **Software as a Service (SaaS):** 
  * *Description:* Completely functional end-user applications delivered over the internet on a subscription or pay-per-use model, accessible seamlessly via standard web browsers without local software installation.
  * *Key Examples:* Google Workspace, Microsoft 365, Salesforce CRM.

**3. Enterprise Deployment Models:**
* **Public Cloud:** Entire infrastructure is owned and operated by a third-party cloud service provider, sharing multi-tenant hardware resources with high elasticity.
* **Private Cloud:** Cloud infrastructure dedicated solely to a single organization, hosted either on-premises or managed externally for enhanced regulatory security.
* **Hybrid Cloud:** Combines public and private infrastructures, allowing sensitive workloads to remain secure internally while scaling non-sensitive traffic elastically into the public cloud.

**4. Strategic Business & Technical Advantages:**
* **Elastic Scalability:** Dynamic allocation of computing resources handles traffic surges seamlessly without manual infrastructure upgrades.
* **High Availability & Disaster Recovery:** Automated multi-region replication ensures business continuity and protects against catastrophic hardware failures."""

        elif "python" in text:
            return """### 🐍 In-Depth Technical Guide: Python Programming Language

**1. Historical Evolution & Core Philosophy:**
Python is a high-level, interpreted, object-oriented programming language created by Guido van Rossum, initially released in February 1991. The core philosophy of Python is encapsulated in the document *The Zen of Python*, which emphasizes code readability, explicit syntax over implicit complexity, and clean indentation rules that eliminate unnecessary curly braces or semicolons.

**2. Internal Mechanics & Execution Model:**
* **Interpreted & Bytecode Compilation:** Although traditionally classified as an interpreted language, modern Python implementations (such as CPython) compile human-readable source code (.py files) into intermediate bytecode (.pyc files) upon execution. This bytecode is subsequently evaluated by the Python Virtual Machine (PVM).
* **Dynamic Typing & Memory Management:** Variable data types are resolved dynamically at runtime rather than compile time. Memory allocation and deallocation are managed automatically via built-in reference counting and a sophisticated generational garbage collection algorithm.

**3. Major Industrial Domains and Frameworks:**
* **Artificial Intelligence & Deep Learning:** Python dominates the AI landscape owing to specialized mathematical computation libraries including TensorFlow, PyTorch, Scikit-Learn, Keras, and OpenCV.
* **Web Engineering & REST APIs:** Robust backend frameworks like Django, Flask, and FastAPI facilitate rapid creation of secure, highly scalable web architectures.
* **Data Science, Analytics & Automation:** Packages such as NumPy, Pandas, Matplotlib, and Seaborn enable heavy-duty data cleansing, statistical modeling, and process automation."""

        elif "plc" in text or "automation" in text:
            return """### ⚡ Advanced Industrial Automation: Programmable Logic Controllers (PLC)

**1. Comprehensive Introduction:**
A Programmable Logic Controller (PLC) is a specialized, ruggedized industrial computer designed to monitor complex electromechanical manufacturing processes, assembly automation lines, robotic cells, and continuous process plants. Unlike standard consumer computers, PLCs are engineered to operate reliably under extreme temperature variations, severe electrical noise, high humidity, and persistent physical vibrations.

**2. Internal Architecture & Hardware Modules:**
* **Central Processing Unit (CPU):** The core processor that executes the user-defined control program, continuously scans field inputs, and updates output actuator states.
* **Memory Subsystem:** Comprises volatile RAM for temporary data storage and non-volatile ROM/EEPROM/Flash memory for permanent storage of the operating system and user control logic.
* **Input / Output (I/O) Interfaces:** 
  * *Discrete/Digital Inputs:* Receive binary signals from limit switches, push buttons, and photoelectric sensors.
  * *Analog Inputs:* Process continuous voltage or current signals from temperature sensors, pressure transmitters, and flow meters.
  * *Outputs:* Drive motor contactors, pneumatic solenoid valves, indicator warning towers, and variable frequency drives (VFDs).

**3. Programming Languages (IEC 61131-3 Standard):**
* **Ladder Logic (LD):** The most popular graphical language mimicking traditional electrical relay schematic diagrams, making it intuitive for maintenance electricians.
* **Structured Text (ST):** A powerful, high-level textual programming language structurally similar to Pascal or C, ideal for complex mathematical computations and data manipulation."""

    # 2. PHARMACY STREAM (Long Answers)
    elif "pharmacy" in stream.lower():
        if "tablet" in text or "capsule" in text or "drug" in text:
            return """### 💊 Comprehensive Pharmaceutical Engineering: Tablet Manufacturing & Quality Control

**1. Introduction to Solid Dosage Forms:**
Tablets are solid unit pharmaceutical dosage forms containing one or more active pharmaceutical ingredients (APIs) combined with appropriate pharmaceutical excipients (diluents, binders, disintegrants, lubricants, and coloring agents), manufactured via compression or molding techniques. They represent the most popular, stable, and patient-compliant mode of drug delivery.

**2. Comprehensive Quality Control (QC) Evaluation Parameters:**
* **Tablet Hardness & Mechanical Strength:** 
  * *Significance:* Evaluates the tablet's structural integrity to withstand shock and friction during industrial packaging, transit, and consumer handling.
  * *Testing Instruments:* Monsanto tester, Pfizer tester, or Erweka hardness tester (acceptable limits typically range between 4 to 8 kg/cm²).
* **Friability Testing:** 
  * *Significance:* Measures vulnerability to surface abrasion and chipping.
  * *Procedure:* Pre-weighed tablets are placed inside a Roche friabilator drum and subjected to rolling impacts at 25 RPM for 4 minutes (100 rotations). Total weight loss should not exceed 1% for standard formulations.
* **Disintegration Time Test:** 
  * *Significance:* Determines the duration required for solid tablets to completely break apart into smaller particles inside simulated gastric fluid at 37°C before systemic absorption can initiate."""

    # 3. NURSING STREAM (Long Answers)
    elif "nursing" in stream.lower():
        if "vital" in text or "patient" in text or "assessment" in text:
            return """### 🩺 Advanced Clinical Nursing: Comprehensive Patient Assessment & Vital Signs Protocols

**1. Introduction to Patient Assessment:**
Systematic physical and clinical assessment forms the cornerstone of professional nursing practice. Monitoring baseline physiological parameters allows healthcare practitioners to detect acute systemic deterioration, evaluate therapeutic responses, and initiate immediate, life-saving clinical interventions.

**2. Detailed Breakdown of Core Vital Signs (TPR & BP):**
* **Body Temperature:** 
  * *Clinical Significance:* Measures the internal thermal equilibrium of the human body, governed by the hypothalamus. Normal baseline oral temperature is approximately 98.6°F (37°C). Elevated readings indicate pyrexia (fever) due to infection or systemic inflammation.
* **Pulse Rate & Rhythm:** 
  * *Clinical Significance:* Palpation of peripheral arteries (radial, carotid, or brachial) measures ventricular contractions per minute. Normal resting adult pulse ranges strictly between 60 to 100 beats per minute. Irregular rhythms require immediate ECG evaluation.
* **Respiration Rate:** 
  * *Clinical Significance:* Counting unannounced breathing cycles (inspiration and expiration) per minute. Normal adult rates range from 12 to 20 breaths per minute, evaluating pulmonary ventilation efficiency.
* **Blood Pressure (BP):** 
  * *Clinical Significance:* Measured using a sphygmomanometer and stethoscope, capturing systolic and diastolic arterial pressures (Standard normal baseline: 120/80 mmHg).

**3. Standard Clinical Nursing Responsibilities:**
* Maintain rigorous aseptic technique and hand hygiene during all patient interactions to prevent nosocomial infections.
* Document exact quantitative measurements accurately in electronic health records without delay."""

    # 4. MBA STREAM (Long Answers)
    elif "mba" in stream.lower():
        if "marketing" in text or "strategy" in text or "management" in text:
            return """### 📈 Executive MBA Study: Strategic Management & Advanced Marketing Frameworks

**1. Strategic Planning & SWOT Analysis Framework:**
Strategic management involves formulating and implementing cross-functional decisions that enable an organization to achieve long-term competitive advantage. A primary diagnostic tool is the **SWOT Matrix**:
* **Internal Analysis (Strengths & Weaknesses):** Evaluation of proprietary technological assets, financial capital liquidity, brand equity, operational bottlenecks, and skilled human resources.
* **External Analysis (Opportunities & Threats):** Assessment of macro-environmental shifts, emerging market trends, competitor positioning, regulatory changes, and economic volatility.

**2. Comprehensive Marketing Mix (The 4 Ps of Marketing):**
* **Product:** Encompasses core utility, quality standards, ergonomic design, packaging integrity, and brand positioning relative to market rivals.
* **Price:** Formulating pricing architectures based on cost-plus structures, value-based pricing, skimming models, or penetration pricing to capture market share.
* **Place (Distribution):** Designing efficient supply chain logistics and retail channel networks to ensure seamless product availability for target consumer demographics.
* **Promotion:** Integrating multi-channel advertising campaigns, digital performance marketing, public relations, and direct sales promotions to maximize brand visibility and customer acquisition."""

    # GENERAL LONG-FORMAT FALLBACK FOR ANY TOPIC
    return f"""### 📚 Comprehensive Academic & Technical Report: {prompt}

**1. Executive Summary & Foundational Theoretical Framework:**
* The selected subject matter **'{prompt}'** holds critical academic, industrial, and functional importance within the **{stream}** curriculum.
* It requires rigorous analytical evaluation, understanding of underlying mathematical or scientific principles, and structured practical implementation.

**2. Detailed Technical Architecture & Core Principles:**
* **System Design & Workflow:** Integrates sequential stages involving precise input data acquisition, systematic internal transformation or processing logic, and verifiable output generation.
* **Performance Optimization & Quality Control:** Emphasizes minimizing operational latency, maximizing systemic reliability, eliminating processing errors, and adhering strictly to institutional standards.

**3. Industrial Applications & Future Scope:**
* Extensively deployed across modern enterprise operations, advanced research laboratories, and cross-functional engineering projects.
* Future developmental trajectories point toward deeper automation, algorithmic efficiency, and integration with intelligent digital ecosystems."""

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

    if prompt := st.chat_input(f"Ask your {education_stream.split()[1]} doubt in detail..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("వివరణాత్మక లాంగ్ నోట్స్ సిద్ధం అవుతోంది... ⏳"):
            reply_text = get_long_comprehensive_answer(education_stream, prompt)
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
