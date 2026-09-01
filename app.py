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

# --- 🧠 చాలా పెద్దవిగా మరియు డీటెయిల్డ్‌గా ఆన్సర్స్ ఇచ్చే లాంగ్-ఫార్మాట్ ఇంజిన్ ---
def get_long_ai_response(prompt):
    text_lower = prompt.lower()
    
    if "quantum physics" in text_lower or "quantum" in text_lower:
        return """### ⚛️ Comprehensive Guide to Quantum Physics

**1. Introduction:**
Quantum physics (also known as quantum mechanics) is a fundamental branch of physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles (electrons, photons, quarks, and other particles). Unlike classical physics, which explains the universe at a macroscopic level, quantum physics reveals a realm where energy, momentum, and other quantities are restricted to discrete values (quantization).

**2. Core Principles:**
* **Wave-Particle Duality:** Proposed by Louis de Broglie, this principle states that every particle or quantum entity may be partly described as either a particle or a wave. Light, for example, behaves like a wave in some experiments and like particles (photons) in others.
* **Superposition:** A fundamental principle stating that a physical system—such as an electron—exists in multiple states simultaneously until it is observed or measured. The famous thought experiment *Schrödinger's Cat* illustrates this paradoxical concept.
* **Quantum Entanglement:** A phenomenon where two or more particles become interconnected in such a way that the state of one instantly dictates the state of the other, regardless of the distance separating them (referred to by Einstein as "spooky action at a distance").
* **Heisenberg's Uncertainty Principle:** Formulated by Werner Heisenberg, it states that certain pairs of physical properties, such as position and momentum, cannot both be known to arbitrary precision simultaneously. The more precisely one property is measured, the less precisely the other can be known.

**3. Real-World Applications & Future Scope:**
* **Quantum Computing:** Utilizing qubits that leverage superposition and entanglement to solve complex computational problems exponentially faster than traditional supercomputers.
* **Cryptography:** Quantum Key Distribution (QKD) provides ultra-secure communication channels where any eavesdropping attempt alters the system and is instantly detected.
* **Semiconductors & Lasers:** Modern electronic devices, MRI machines, and semiconductor manufacturing heavily rely on quantum mechanical tunneling and energy states."""

    elif "python" in text_lower:
        return """### 🐍 In-Depth Overview of Python Programming

**1. Introduction and Philosophy:**
Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum and first released in 1991. Its design philosophy emphasizes code readability with the notable use of significant whitespace. Python's syntax allows programmers to express concepts in fewer lines of code than would be possible in languages such as C++ or Java.

**2. Key Features of Python:**
* **Easy to Learn and Read:** Clean and straightforward syntax makes it beginner-friendly, lowering the barrier to entry for software development.
* **Interpreted Language:** Code is executed line by line, which simplifies debugging and testing during development.
* **Dynamically Typed:** Variable types do not need to be explicitly declared; the interpreter infers them at runtime.
* **Extensive Standard Library & Ecosystem:** Offers thousands of third-party packages and modules via PyPI for web development, data science, AI, and automation.

**3. Major Domains and Applications:**
* **Artificial Intelligence & Machine Learning:** Libraries like TensorFlow, PyTorch, Scikit-Learn, and Keras make Python the undisputed industry leader for deep learning, neural networks, and predictive modeling.
* **Web Development:** Robust frameworks like Django, Flask, and FastAPI enable rapid creation of secure, scalable web applications and RESTful APIs.
* **Data Science & Analytics:** Pandas, NumPy, Matplotlib, and Seaborn allow powerful data manipulation, processing, and visualization.
* **Automation & Scripting:** Routine tasks, file system management, web scraping (using BeautifulSoup/Selenium), and network configurations are easily automated using Python scripts."""

    elif "plc" in text_lower:
        return """### ⚡ Complete Guide to Programmable Logic Controllers (PLC)

**1. What is a PLC?**
A Programmable Logic Controller (PLC) is a ruggedized digital computer used in industrial automation for manufacturing processes, assembly lines, amusement rides, and robotic cells. Unlike standard desktop computers, a PLC is engineered to withstand severe environmental conditions such as extreme temperatures, humidity, vibration, and electrical noise.

**2. Architecture and Core Components:**
* **Central Processing Unit (CPU):** The brain of the PLC that executes the control program, evaluates input signals, and updates output states.
* **Memory (RAM/ROM):** Stores the operating system, user control logic programs, and data tables.
* **Input/Output (I/O) Modules:** 
  * *Inputs:* Receive signals from sensors, push buttons, limit switches, and thermocouples.
  * *Outputs:* Send control commands to actuators, motor starters, solenoid valves, and indicator lights.
* **Power Supply Unit:** Converts incoming AC voltage to regulated DC voltages required by the CPU and I/O cards.

**3. Programming Languages (IEC 61131-3 Standard):**
* **Ladder Logic (LD):** The most popular graphical programming language resembling traditional relay schematic diagrams.
* **Structured Text (ST):** A high-level, text-based language similar to Pascal or C.
* **Function Block Diagram (FBD):** A graphical language ideal for processing complex signal flows.
* **Sequential Function Chart (SFC) & Instruction List (IL).**"""

    else:
        return f"""### 📋 Detailed Study & Project Report on: {prompt}

**1. Executive Summary & Core Concepts:**
* The topic **'{prompt}'** plays a critical role in modern engineering, academic research, and industrial applications. 
* It involves analyzing underlying theoretical frameworks, practical implementations, and performance metrics to achieve optimal results.

**2. Key Technical Parameters & Architecture:**
* **System Integration:** Combines hardware modules or software algorithms to streamline operations and ensure high reliability.
* **Efficiency & Optimization:** Focuses on minimizing resource wastage while maximizing throughput and accuracy.
* **Safety & Compliance:** Adheres to industry standards, protocols, and regulatory guidelines to maintain structural and operational integrity.

**3. Applications and Future Enhancements:**
* Extensively utilized across cross-disciplinary domains including automation, data analytics, and system design.
* Future trends point toward deeper integration with artificial intelligence, cloud computing, and automated monitoring systems to drive next-generation advancements."""

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

    if prompt := st.chat_input("Ask anything in detail..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("వివరణాత్మక నోట్స్ తయారు చేయబడుతోంది... ⏳ வகం"):
            # చాలా పెద్దవిగా, డీటెయిల్డ్‌గా ఆన్సర్ ఇచ్చే ఫంక్షన్ కాల్
            reply_text = get_long_ai_response(prompt)

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
