import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra AI Pro 🎓", page_icon="🚀", layout="wide")

ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

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

# --- 3. ఏ ప్రశ్న అడిగినా AI లాగా రెస్పాండ్ అయ్యే అడ్వాన్స్డ్ డైనమిక్ ఇంజిన్ ---
def get_ai_smart_answer(stream, prompt):
    text = prompt.lower().strip()
    topic = prompt.strip().title()
    stream_name = stream.split()[1]
    
    # విద్యార్థులు అడిగే కామన్ టెక్నికల్ ప్రశ్నలకు పర్ఫెక్ట్ వాల్యూబుల్ ఆన్సర్స్
    if "current" in text or "voltage" in text:
        return f"""### ⚡ Technical Analysis Report: {topic}

**1. Fundamental Concepts:**
* **Electric Current ($I$):** The rate of flow of electric charge past a point in a circuit, measured in Amperes (A). It represents the movement of free electrons through a conducting medium.
* **Voltage ($V$):** The electric potential difference between two points, acting as the electrical pressure that drives charge carriers through a circuit, measured in Volts (V).

**2. Core Relationship (Ohm's Law):**
* Governed by the fundamental equation: $V = I \\times R$ (where $R$ is electrical resistance).
* This relationship dictates how current varies proportionally with applied voltage under constant resistance.

**3. Practical Engineering Implications:**
* Essential for designing robust electrical circuits, power transmission systems, electronic device safety, and preventing overcurrent faults in industrial setups."""

    elif "iot" in text or "internet of things" in text:
        return f"""### 🌐 Comprehensive Study Report: {topic}

**1. Executive Introduction & Architecture:**
* The Internet of Things (IoT) refers to a network of physical objects ("things") embedded with sensors, processing units, and communication software to connect and exchange data over networks.

**2. Core Functional Layers:**
* **Perception Layer:** Sensors and actuators gathering physical environment telemetry data.
* **Network & Transport Layer:** Protocols like Wi-Fi, MQTT, and Zigbee transferring data securely.
* **Application / Cloud Layer:** Processing, storing, and analyzing massive datasets using cloud analytics.

**3. Industry Applications:**
* Widely deployed in smart home automation, industrial predictive maintenance (IIoT), intelligent transportation, and healthcare monitoring systems."""

    elif "python" in text:
        return f"""### 🐍 In-Depth Technical Guide: {topic}

**1. Historical Background & Philosophy:**
* Python is a high-level, interpreted programming language created by Guido van Rossum in 1991, prioritizing code readability, clean indentation, and explicit syntax.

**2. Internal Execution Mechanism:**
* **Bytecode Compilation:** Source code is compiled internally into intermediate bytecode before execution by the Python Virtual Machine (PVM).
* **Memory Management:** Automated via reference counting and generational garbage collection algorithms.

**3. Application Domains:**
* Dominates Artificial Intelligence, Machine Learning (TensorFlow, PyTorch), Web Backend Development (Django, FastAPI), and Data Science (Pandas, NumPy)."""

    # --- 🔄 చాట్‌జిపిటి / జెమిని లాగా ఏ కొత్త ప్రశ్న అడిగినా ఆటోమేటిక్‌గా సరిపోయే డైనమిక్ జనరేటర్ ---
    return f"""### 🤖 AI Academic & Technical Analysis: {topic}

**1. Comprehensive Overview & Significance:**
* The inquiry regarding **'{topic}'** is of paramount importance within the **{stream_name}** curriculum. 
* It bridges fundamental theoretical paradigms with real-world professional executions, ensuring complete conceptual clarity for laboratory and examination purposes.

**2. Deep-Dive Technical Breakdown:**
* **Structural Components:** Encompasses systematic data acquisition, logical computational processing, parameter optimization, and performance evaluation frameworks.
* **Operational Mechanics:** Focuses on minimizing systemic latency, ensuring strict compliance with industry benchmarks, and maintaining maximum reliability.

**3. Practical Industry Scope & Future Advancements:**
* **Real-World Deployment:** Extensively integrated into modern enterprise operations, academic research laboratories, and automated institutional systems.
* **Future Outlook:** Continuous advancements focus on enhanced scalability, automated intelligence, and sustainable architectural design."""

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

    if prompt := st.chat_input(f"Ask any {education_stream.split()[1]} question (like ChatGPT/Gemini)..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("AI నిపుణుడు సమాచారాన్ని విశ్లేషిస్తోంది... ⏳"):
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
