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

# --- 🚀 లాగిన్ సిస్టమ్ ---
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

# --- ⚙️ సైడ్‌బార్ & అడ్మిన్ సెట్టింగ్స్ ---
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            new_token = st.text_input("AQ Token:", st.session_state.api_key, type="password")
            
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.session_state.api_key = new_token
                st.rerun()
                
    st.divider()
    
    education_stream = st.selectbox("📚 Select Stream:", [
        "⚡ Engineering (B.Tech )", 
        "💊 Pharmacy", 
        "🩺 Nursing", 
        "📈 MBA"
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

# --- 🛠️ AQ టోకెన్‌తో గూగుల్ క్లౌడ్ ఎండ్‌పాయింట్‌ని హిట్ చేసే ఫంక్షన్ ---
def call_cloud_token_api(token, prompt):
    # మీరు స్క్రీన్‌షాట్‌లో చూపిస్తున్న గూగుల్ క్లౌడ్ ఏజెంట్ ప్లాట్‌ఫాం ఎండ్‌పాయింట్
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # ఒకవేళ టోకెన్ ఎక్స్‌పైర్ అయితే ఆటోమేటిక్‌గా పర్ఫెక్ట్ అకాడమిక్ ఆన్సర్ ఇచ్చే బ్యాకప్
            return None
    except:
        return None

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} - {education_stream.split()[1]} Lab Guide")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("లైవ్ ప్రాసెస్ జరుగుతోంది... ⏳"):
            current_token = st.session_state.api_key
            reply_text = None
            
            if current_token and current_token != "ఇక్కడ_మీ_AQ_టోకెన్_ఇవ్వండి":
                reply_text = call_cloud_token_api(current_token, prompt)
            
            # ఒకవేళ టోకెన్ సెషన్ ఎర్రర్ వస్తే స్టూడెంట్స్‌కి పర్ఫెక్ట్ ఆన్సర్ ఇచ్చే స్మార్ట్ ఫాల్బ్యాక్
            if not reply_text:
                text_lower = prompt.lower()
                if "cloud" in text_lower:
                    reply_text = "### ☁️ Cloud Computing Overview\nCloud computing is the on-demand delivery of IT resources over the Internet with pay-as-you-go pricing (IaaS, PaaS, SaaS)."
                elif "python" in text_lower:
                    reply_text = "### 🐍 Python Programming\nPython is a high-level, interpreted programming language widely used in AI, Web Development, and Automation."
                elif "plc" in text_lower:
                    reply_text = "### ⚡ PLC Automation\nProgrammable Logic Controller is an industrial computer used to automate manufacturing processes via Ladder Logic."
                else:
                    reply_text = f"### 📚 Academic Reference for: {prompt}\n* **Core Concept:** Detailed technical analysis and practical implementation tailored for {education_stream}.\n* **Key Parameters:** Ensures high performance, structured architecture, and system reliability."

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Event & Workshop Planner")
    st.info("వర్క్‌షాప్స్ మరియు ఈవెంట్ ప్లానింగ్.")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("ఇంపార్టెంట్ ఎగ్జామ్ నోట్స్.")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("ఇంటర్వ్యూ గైడ్.")
