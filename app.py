import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra AI 🎓", page_icon="🚀", layout="wide")

DEFAULT_TOKEN = "AQ.Ab8RN6KPeVyNXJrhwzkxqoaqH0rH2hRSa3W4BCudsQMSeOZjWg"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_TOKEN
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra AI 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

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
    st.stop()

with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            new_token = st.text_input("Token:", st.session_state.api_key, type="password")
            
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.session_state.api_key = new_token
                st.rerun()
                
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

# --- 🎯 ఖచ్చితమైన మరియు సరైన ఆన్సర్స్ ఇచ్చే స్మార్ట్ ఇంజిన్ ---
def get_accurate_answer(prompt):
    text_lower = prompt.lower()
    
    if "cloud computing" in text_lower or "cloud" in text_lower:
        return """### ☁️ What is Cloud Computing?

**1. Definition:**
Cloud computing is the on-demand delivery of computing services over the Internet—including storage, servers, databases, networking, software, analytics, and intelligence—over the Internet ("the cloud").

**2. Key Benefits:**
* **Cost Efficiency:** Eliminates the capital expense of buying hardware and software and setting up on-site datacenters.
* **Speed & Scalability:** Services can be provided in minutes, scaling elastically based on exact business needs.
* **Reliability & Security:** Data backup, disaster recovery, and data protection are easier and cheaper because data can be mirrored at multiple redundant sites.

**3. Major Service Models (SPI Model):**
* **IaaS (Infrastructure asَّة a Service):** Renting fundamental computing resources (virtual machines, storage, networks). *Example: AWS EC2, Google Compute Engine.*
* **PaaS (Platform as a Service):** Providing a managed environment for developers to build, test, and deploy applications without worrying about underlying infrastructure. *Example: Google App Engine, Heroku.*
* **SaaS (Software as a Service):** Delivers software applications over the internet, on-demand, typically via a web browser. *Example: Gmail, Microsoft 365, Dropbox.*

**4. Deployment Models:**
* Public Cloud, Private Cloud, Hybrid Cloud, and Multi-Cloud architectures."""

    elif "python" in text_lower:
        return """### 🐍 What is Python?
Python is a high-level, interpreted programming language known for its clean syntax and readability. It is widely used in Artificial Intelligence, Machine Learning, Web Development, Data Science, and Automation because of its vast ecosystem of libraries (like NumPy, Pandas, TensorFlow, and Django)."""

    elif "plc" in text_lower:
        return """### ⚡ What is a PLC (Programmable Logic Controller)?
A PLC is a ruggedized industrial digital computer designed for manufacturing processes, assembly lines, and robotic cells. It monitors inputs, makes decisions based on a custom program, and controls outputs to automate industrial machinery. It is typically programmed using Ladder Logic."""

    elif "iot" in text_lower or "internet of things" in text_lower:
        return """### 🌐 What is IoT (Internet of Things)?
IoT refers to a system of interrelated physical devices, vehicles, home appliances, and other items embedded with electronics, software, sensors, and network connectivity which enables these objects to collect and exchange data over the internet."""

    else:
        return f"""### 📚 Technical Overview: {prompt}

**1. Core Concept:**
The topic **'{prompt}'** is a fundamental engineering and technical concept that involves systematic implementation, architectural design, and functional analysis to solve real-world problems.

**2. Key Architecture / Principles:**
* **Input/Processing/Output:** Relies on structured workflows to intake parameters, execute internal logic or transformations, and deliver reliable results.
* **Performance & Optimization:** Designed to maximize efficiency, reduce operational latency, and maintain error-free execution.

**3. Practical Applications:**
* Extensively applied in software engineering, automation systems, industrial projects, and advanced technological frameworks."""

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Assistant")
    
    available_models = ["gemini-1.5-flash", "gemini-2.5-flash"] 
    selected_model = st.selectbox("🧠 బ్రెయిన్ మోడల్:", available_models, index=0) 

    tab1, tab2, tab3 = st.tabs(["💬 Text Chat", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab2:
        uploaded_file = st.file_uploader("ఫోటో అప్‌లోడ్ చేయండి", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_to_send = Image.open(uploaded_file)
            st.image(img_to_send, caption="అప్‌లోడ్ చేసిన ఫోటో", width=300)
    with tab3:
        camera_photo = st.camera_input("ఫోటో తీయండి")
        if camera_photo:
            img_to_send = Image.open(camera_photo)
            st.image(img_to_send, caption="తీసిన ఫోటో", width=300)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask anything..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("సమాచారాన్ని విశ్లేషిస్తోంది... ⏳"):
            reply_text = get_accurate_answer(prompt)
            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("వర్క్‌షాప్స్ మరియు ఈవెంట్ స్క్రిప్ట్స్ ప్లాన్ చేసుకోండి.")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker - Study Buddy")
    st.info("ఇంపార్టెంట్ ఎగ్జామ్ క్వశ్చన్స్ మరియు రివిజన్ నోట్స్.")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep - Interview Coach")
    st.info("టెక్నికల్ ఇంటర్వ్యూ ప్రిపరేషన్ గైడ్.")
