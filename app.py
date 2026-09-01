import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra AI 🎓", page_icon="🚀", layout="wide")

# 1. 🔑 మీ AQ టోకెన్ ఇక్కడ ఇవ్వండి
DEFAULT_AQ_TOKEN = "AQ.Ab8RN6KrgG_0pF8ATLEw5QHMrgXLEr7LD_9FYw_rcgFcqBSXHw"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- మెమరీ సెటప్ ---
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_AQ_TOKEN
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra AI 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 🚀 వన్-టైమ్ లాగిన్ (Persistent Login) ---
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

# --- ⚙️ సైడ్‌బార్ & అడ్మిన్ సెట్టింగ్స్ ---
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings (AQ Support)"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            new_token = st.text_input("AQ Token / Bearer Token:", st.session_state.api_key, type="password")
            
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

# --- 🛠️ AQ టోకెన్ కోసం పర్ఫెక్ట్ అండ్ డైరెక్ట్ জెమినీ రెస్ట్ API ఫంక్షన్ ---
def call_gemini_with_aq_token(token, model_name, prompt, image_obj=None):
    clean_model = model_name.replace("models/", "")
    
    # నేరుగా స్టాండర్డ్ జెమినీ వన్-బీటా ఎండ్‌పాయింట్ వాడతాం (ఇది AQ బేరర్ టోకెన్లను సపోర్ట్ చేస్తుంది)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
        
    parts = [{"text": prompt}]
    
    if image_obj is not None:
        buffered = BytesIO()
        image_obj.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": img_str
            }
        })
        
    payload = {"contents": [{"parts": parts}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ API ఎర్రర్ ({response.status_code}): {response.text}\n\n*(గమనిక: మీ AQ టోకెన్ గడువు ముగిసి ఉండవచ్చు. దయచేసి కొత్త టోకెన్ జనరేట్ చేసి ఇవ్వండి.)*"
    except Exception as e:
        return f"⚠️ కనెక్షన్ ఎర్రర్: {e}"

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide")
    
    available_models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-flash"
    ] 
    
    selected_model = st.selectbox("🧠 బ్రెయిన్ మోడల్ సెలెక్ట్ చేసుకోండి:", available_models, index=0) 

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
        
        with st.spinner("లైవ్ ఏఐ రెస్పాన్స్ తెస్తోంది... ⏳"):
            current_token = st.session_state.api_key
            
            if not current_token or current_token == "ఇక్కడ_మీ_AQ_టోకెన్_పేస్ట్_చేయండి":
                reply_text = "⚠️ దయచేసి అడ్మిన్ సెట్టింగ్స్‌లో మీ AQ Token ఇవ్వండి."
            else:
                reply_text = call_gemini_with_aq_token(current_token, selected_model, prompt, img_to_send)

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈవెంట్ ప్లానింగ్ మరియు వర్క్‌షాప్ స్క్రిప్ట్స్ కోసం.")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("ఎగ్జామ్ ప్రిపరేషన్ మరియు ఇంపార్టెంట్ నోట్స్.")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("ఇంటర్వ్యూ గైడ్ మరియు ప్రిపరేషన్.")
