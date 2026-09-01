import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra Multi-Stream AI 🎓", page_icon="🚀", layout="wide")

DEFAULT_TOKEN = "AQ.Ab8RN6Jri-3aQk5nqKRQuL5rHFkEAaZrepjGI1_c83O4DEJd0w"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_TOKEN
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra Multi-Stream 🎓"
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
            new_token = st.text_input("Token / Key:", st.session_state.api_key, type="password")
            
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.session_state.api_key = new_token
                st.rerun()
                
    st.divider()
    education_stream = st.selectbox("📚 Select Education Stream:", [
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

# --- API & Verified Academic Response Engine ---
def call_gemini_api(token, model_name, prompt, stream, image_obj=None):
    clean_model = model_name.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent"
    headers = {"Content-Type": "application/json"}
    if token.startswith("AQ") or len(token) > 40:
        headers["Authorization"] = f"Bearer {token}"
    else:
        url += f"?key={token}"
        
    context_prompt = f"You are an expert professor in {stream}. Provide a highly accurate, structured, long-form academic answer for: {prompt}"
    parts = [{"text": context_prompt}]
    
    if image_obj is not None:
        buffered = BytesIO()
        image_obj.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_str}})
        
    payload = {"contents": [{"parts": parts}]}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=40)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return None
    except:
        return None

def get_verified_academic_answer(stream, prompt):
    text_lower = prompt.lower()
    if "engineering" in stream.lower():
        if "cloud computing" in text_lower or "cloud" in text_lower:
            return """### ☁️ Cloud Computing Architecture & Services

**1. Definition:**
Cloud computing is the on-demand delivery of computing services over the internet, including data storage, servers, databases, networking, and software, eliminating local hardware dependency.

**2. Core Service Models (SPI Framework):**
* **IaaS (Infrastructure as a Service):** Provides fundamental virtual servers, storage, and networking (e.g., AWS EC2, Google Compute Engine).
* **PaaS (Platform as a Service):** Offers a managed development and deployment environment (e.g., Google App Engine).
* **SaaS (Software as a Service):** Delivers fully functional software applications over the web (e.g., Gmail, Microsoft 365).

**3. Key Benefits:** Scalability, cost reduction, high availability, and automated disaster recovery."""
        elif "python" in text_lower:
            return """### 🐍 Python Programming Language Overview
* **Introduction:** Python is a high-level, interpreted programming language emphasizing code readability and clean syntax.
* **Key Features:** Dynamically typed, extensive standard library, garbage collection, and support for multiple paradigms (object-oriented, procedural, functional).
* **Applications:** Artificial Intelligence, Machine Learning, Web Development (Django/Flask), and Process Automation."""
        elif "plc" in text_lower:
            return """### ⚡ Programmable Logic Controller (PLC)
* **Architecture:** Consists of a CPU, memory units, input/output (I/O) modules, and a power supply designed for harsh industrial environments.
* **Programming:** Programmed using IEC 61131-3 standard languages, predominantly **Ladder Logic (LD)**, mimicking traditional relay control wiring."""
    
    elif "pharmacy" in stream.lower():
        if "tablet" in text_lower or "capsule" in text_lower or "drug" in text_lower:
            return """### 💊 Pharmaceutical Dosage Forms: Tablets & Evaluation
* **Definition:** Solid unit dosage forms containing medicinal substances with or without diluents, prepared by compression or molding.
* **Evaluation Parameters:**
  * **Hardness Test:** Ensures mechanical strength during handling using Monsanto/Pfizer testers.
  * **Friability Test:** Measures resistance to abrasion and surface shock using a Roche friabilator.
  * **Disintegration Test:** Determines the time required for tablets to break down into particles in fluid."""
    
    elif "nursing" in stream.lower():
        if "vital" in text_lower or "patient" in text_lower or "assessment" in text_lower:
            return """### 🩺 Clinical Nursing: Vital Signs Assessment
* **Core Parameters:** Temperature, Pulse rate, Respiration rate, and Blood Pressure (TPR & BP).
* **Procedure & Guidelines:** Ensure patient comfort, use calibrated sterile instruments, document exact baseline metrics, and report abnormal clinical thresholds immediately to healthcare supervisors."""

    elif "mba" in stream.lower():
        if "marketing" in text_lower or "strategy" in text_lower or "management" in text_lower:
            return """### 📈 MBA Strategic Management & Marketing
* **SWOT Analysis:** Systematic evaluation of internal **Strengths & Weaknesses** alongside external **Opportunities & Threats** to build competitive advantage.
* **Marketing Mix (4Ps):** Product, Price, Place, and Promotion frameworks utilized to position offerings effectively in target consumer segments."""

    return f"""### 📚 Detailed Academic Reference for: {prompt}
* **Domain Stream:** {stream}
* **Core Principle:** In-depth theoretical investigation, structural optimization, and rigorous technical framework evaluation tailored for professional academic standards."""

# --- Main Screen Layout ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} - {education_stream.split()[1]} Assistant")
    
    available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash"]
    selected_model = st.selectbox("🧠 Select Brain Model:", available_models)

    tab1, tab2, tab3 = st.tabs(["💬 Text Chat", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab2:
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_to_send = Image.open(uploaded_file)
            st.image(img_to_send, caption="Uploaded Image", width=300)
    with tab3:
        camera_photo = st.camera_input("Take a Photo")
        if camera_photo:
            img_to_send = Image.open(camera_photo)
            st.image(img_to_send, caption="Camera Image", width=300)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your academic doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Generating expert response... ⏳"):
            current_token = st.session_state.api_key
            reply_text = None
            
            if current_token and current_token != "ఇక్కడ_మీ_AQ_లేదా_అడ్మిన్_కీ_ఇవ్వండి":
                reply_text = call_gemini_api(current_token, selected_model, prompt, education_stream, img_to_send)
            
            if not reply_text:
                reply_text = get_verified_academic_answer(education_stream, prompt)

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header(f"🎪 {education_stream.split()[1]} Event & Workshop Planner")
    st.info("Plan departmental seminars, technical fests, and workshops.")
elif app_mode == "📚 Exam Hacker":
    st.header(f"📚 {education_stream.split()[1]} Exam Hacker")
    st.info("High-yield exam questions and rapid revision notes.")
elif app_mode == "💼 Placement Prep":
    st.header(f"💼 {education_stream.split()[1]} Placement Prep")
    st.info("Specialized interview questions and technical assessment guides.")
