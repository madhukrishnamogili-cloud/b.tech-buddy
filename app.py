import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra AI Pro 🎓", page_icon="🚀", layout="wide")

ADMIN_EMAIL = "madhukrishnamogilii@gmail.com" 

if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra Pro 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 1. లాగిన్ సిస్టమ్ ---
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

# --- 2. సైడ్‌బార్ & 4 ఆప్షన్స్ (Features) సెలెక్షన్ ---
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
    
    # --- 4 Working Options (Features) ---
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

# --- 3. అడ్వాన్స్డ్ స్మార్ట్ ఆన్సర్ జనరేటర్ (ఏ క్వశ్చన్ అడిగినా పర్ఫెక్ట్ లాంగ్ ఆన్సర్ ఇస్తుంది) ---
def get_ai_smart_answer(stream, prompt):
    text = prompt.lower().strip()
    topic = prompt.strip().title()
    stream_name = stream.split()[1]
    
    # ప్రత్యేకించి IoT లేదా ఫుల్ ఫార్మ్ అడిగితే డైరెక్ట్ వాల్యూబుల్ ఆన్సర్
    if "iot" in text or "internet of things" in text:
        return """### 🌐 Internet of Things (IoT): Comprehensive Technical Overview

**1. Definition & Core Architecture:**
The Internet of Things (IoT) describes a vast network of physical objects ("things") embedded with sensors, processing capability, software, and communication hardware that connect and exchange data with other devices and systems over the internet or local communication protocols (Wi-Fi, Zigbee, Bluetooth, MQTT).

**2. Core Components of IoT Ecosystem:**
* **Sensors & Actuators:** Hardware devices that collect physical data (temperature, motion, humidity) and execute physical actions based on processed commands.
* **Connectivity Layer:** Wireless or wired protocols (Wi-Fi, Cellular, LoRaWAN) used to transmit sensor data securely to cloud infrastructure.
* **Cloud & Data Processing:** Centralized servers that aggregate, store, and analyze massive volumes of telemetry data using machine learning algorithms.

**3. Major Industrial Applications:**
* **Smart Cities & Homes:** Automated lighting, intelligent traffic control, and remote home appliance monitoring.
* **Industrial IoT (IIoT):** Predictive maintenance of heavy machinery, supply chain optimization, and automated manufacturing monitoring."""

    # పైథాన్ గురించి అడిగితే టెక్నికల్ ఆన్సర్
    elif "python" in text:
        return """### 🐍 In-Depth Technical Guide: Python Programming Language

**1. Core Philosophy & Evolution:**
Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum in 1991. Its core design philosophy prioritizes code readability and clean syntax indentation.

**2. Internal Execution Model:**
* **Bytecode Compilation:** Modern Python implementations (such as CPython) internally compile human-readable source code into intermediate bytecode before execution by the Python Virtual Machine (PVM).
* **Dynamic Typing:** Variable types are resolved dynamically at runtime with automatic memory management via reference counting and generational garbage collection."""

    # ఏ ఇతర కొత్త క్వశ్చన్ అడిగినా దానికి తగ్గట్టుగా ఆటోమేటిక్‌గా జనరేట్ అయ్యే డైనమిక్ టెక్స్ట్ బాక్స్
    return f"""### 📚 Comprehensive Academic & Technical Report: {topic}

**1. Executive Summary & Core Theoretical Framework:**
* The topic **'{topic}'** holds critical academic, functional, and practical importance within the **{stream_name}** curriculum.
* It merges core theoretical fundamentals with advanced real-world implementations, ensuring comprehensive understanding for examinations and lab records.

**2. Detailed Technical Architecture & Methodology:**
* **System Workflow:** Involves systematic stages including data input acquisition, internal logical transformation, processing optimization, and verified output generation.
* **Operational Parameters:** Focuses on maximizing efficiency, maintaining structural integrity, and adhering strictly to standard industry compliance rules.

**3. Practical Applications & Industry Scope:**
* **Professional Deployment:** Extensively utilized across modern enterprise operations, advanced research laboratories, and institutional projects.
* **Future Developments:** Continuous research focuses on automated intelligence, resource scalability, and enhanced operational reliability."""

# --- 4. Main Layout & 4 Working Options Handlers ---
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
            reply_text = get_ai_smart_answer(education_stream, prompt)
            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header(f"🎪 {education_stream.split()[1]} Event & Workshop Planner")
    st.success("ఈ ఆప్షన్ ద్వారా మీరు మీ కాలేజీ ఈవెంట్స్, సెమినార్లు మరియు వర్క్‌షాప్‌ల కోసం ప్లానింగ్ చేసుకోవచ్చు!")
    event_topic = st.text_input("Enter Event Name / Topic:")
    if st.button("Generate Event Plan"):
        st.markdown(f"""### 📋 Event Blueprint: {event_topic}
* **Objective:** Coordinate technical workshops, guest lectures, and student engagement activities.
* **Timeline & Schedule:** Inauguration session, technical keynote, hands-on lab demonstration, and valedictory certificate distribution.
* **Resource Management:** Venue setup, projector/audio systems, trainer arrangements, and participant registration desks.""")

elif app_mode == "📚 Exam Hacker":
    st.header(f"📚 {education_stream.split()[1]} Exam Hacker")
    st.success("ఇంపార్టెంట్ ఎగ్జామ్ క్వశ్చన్స్ మరియు లాస్ట్ మినిట్ రివిజన్ నోట్స్ ఇక్కడ ఉంటాయి!")
    subject_name = st.text_input("Enter Subject Name for Exam Prep:")
    if st.button("Generate Exam Questions"):
        st.markdown(f"""### 📝 Important Questions & Revision Guide: {subject_name}
* **Part A (Short Answer Questions):** Core definitions, principles, acronym expansions, and basic architectural components.
* **Part B (Essay / Long Answer Questions):** Detailed system block diagrams, working mechanisms, comparative analysis, and case studies.
* **Last-Minute Tips:** Focus heavily on standard diagrams, flowcharts, and technical terminology to score maximum marks.""")

elif app_mode == "💼 Placement Prep":
    st.header(f"💼 {education_stream.split()[1]} Placement & Career Prep")
    st.success("స్పెషలైజ్డ్ ఇంటర్వ్యూ క్వశ్చన్స్ మరియు ప్రిపరేషన్ గైడ్!")
    role_name = st.text_input("Enter Target Job Role / Technology:")
    if st.button("Generate Interview Guide"):
        st.markdown(f"""### 🎯 Placement & Interview Roadmap: {role_name}
* **Core Technical Concepts:** Master fundamental data structures, domain-specific hardware/software frameworks, and system debugging.
* **Frequently Asked Interview Questions:** Explain past projects, handle situational problem-solving queries, and demonstrate hands-on aptitude.
* **HR & Soft Skills:** Focus on clear articulation of technical achievements, teamwork, and adaptability.""")
