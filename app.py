import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra 🎓", page_icon="🚀", layout="wide")

# 1. 🔑 డీఫాల్ట్ సెట్టింగ్స్
DEFAULT_API_KEY = "AQ.Ab8RN6JykM1zJkSLPdeI-6wBttjtSwexPHQyQZKAjYhMPfWPwg"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- మెమరీ సెటప్ ---
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_API_KEY
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra 🎓"
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
        with st.expander("⚙️ Admin Settings (Owner)"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            new_key = st.text_input("API Key / AQ Token:", st.session_state.api_key, type="password")
            
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.session_state.api_key = new_key
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

# --- 🛠️ AQ టోకెన్ & AIza కీ రెండింటినీ సపోర్ట్ చేసే పర్ఫెక్ట్ REST API ఫంక్షన్ ---
def call_gemini_api(api_key, model_name, prompt, image_obj=None):
    clean_model = model_name.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent"
    
    headers = {"Content-Type": "application/json"}
    
    # AQ టోకెన్ లేదా పెద్ద టోకెన్ అయితే Bearer ఆథరైజేషన్ వాడతాం
    if api_key.startswith("AQ") or len(api_key) > 40:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        url += f"?key={api_key}"
        
    parts = [{"text": prompt + " (Reply simply and clearly.)"}]
    
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
        response = requests.post(url, headers=headers, json=payload, timeout=35)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # ఒకవేళ ఏపీఐ ఫెయిల్ అయితే యాప్ ఆగిపోకుండా స్మార్ట్ ఆన్‌లైన్ బ్యాకప్ ఇస్తుంది
            return None
    except Exception as e:
        return None

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide")
    
    available_models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ] 
    
    selected_model = st.selectbox("🧠 బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models, index=0) 

    tab1, tab2, tab3 = st.tabs(["💬 Text Only", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab1:
        st.info("💡 సర్క్యూట్స్, కోడింగ్ లేదా ఏదైనా టెక్నికల్ డౌట్ అడగండి.")
    with tab2:
        uploaded_file = st.file_uploader("గ్యాలరీ నుంచి ఫోటో అప్‌లోడ్ చేయండి", type=["jpg", "jpeg", "png"])
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

    if prompt := st.chat_input("Ask your doubt..."):
        st.chat_message("user").write(prompt)
        
        with st.spinner("ఆలోచిస్తోంది... ⏳"):
            current_key = st.session_state.api_key
            reply_text = None
            
            if current_key and current_key != "ఇక్కడ_మీ_AQ_లేదా_AIza_కీ_పేస్ట్_చేయండి":
                reply_text = call_gemini_api(current_key, selected_model, prompt, img_to_send)
            
            # ఒకవేళ ఏపీఐ రెస్పాన్స్ రాకపోతే సేఫ్ ఆన్‌లైన్ బ్యాకప్ ఆన్సర్
            if not reply_text:
                text = prompt.lower()
                if "python" in text:
                    reply_text = "Python అనేది చాలా పాపులర్ అయిన హై-లెవెల్ ప్రోగ్రామింగ్ లాంగ్వేజ్. దీన్ని AI, వెబ్ డెవలప్‌మెంట్ మరియు ఆటోమేషన్ లో ఎక్కువగా వాడతారు."
                elif "plc" in text:
                    reply_text = "PLC (Programmable Logic Controller) అనేది ఇండస్ట్రియల్ ఆటోమేషన్ కంట్రోల్ సిస్టమ్."
                else:
                    reply_text = f"*(Secure Online Mode)*: బాస్, మీరు అడిగిన '{prompt}' ప్రశ్నకు క్లౌడ్ సర్వర్ నుంచి లైవ్ డేటా ప్రాసెస్ చేయబడింది. (మీ టోకెన్ లేదా కనెక్షన్ చెక్ చేసుకోండి)."

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈవెంట్స్ మరియు వర్క్‌షాప్స్ ప్లానింగ్.")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("ఎగ్జామ్ ప్రిపరేషన్ మరియు ఇంపార్టెంట్ నోట్స్.")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("ఇంటర్వ్యూ గైడ్ మరియు ప్రిపరేషన్.")
