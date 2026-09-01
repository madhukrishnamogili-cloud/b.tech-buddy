import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Tech Mithra AI 🎓", page_icon="🚀", layout="wide")

# 1. 🔑 డిఫాల్ట్ సెట్టింగ్స్
DEFAULT_API_KEY = "AQ.Ab8RN6JoMlJ37PuLg3trHWk23E4_WXE4kF07cHvYf6ieA3E-Tg"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- మెమరీ సెటప్ ---
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_API_KEY
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

# --- 🛠️ ChatGPT లాంటి డైరెక్ట్ లైవ్ రెస్పాన్స్ కోసం REST API ఫంక్షన్ ---
def call_chatgpt_style_api(api_key, model_name, prompt, image_obj=None):
    clean_model = model_name.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent"
    
    headers = {"Content-Type": "application/json"}
    
    # AQ టోకెన్ లేదా పెద్ద టోకెన్ అయితే Bearer టోకెన్ వాడతాం
    if api_key.startswith("AQ") or len(api_key) > 40:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        url += f"?key={api_key}"
        
    parts = [{"text": prompt}]
    
    # ఫోటో లేదా కెమెరా ఇమేజ్ ఉంటే దాన్ని కూడా కలిపి పంపుతాం
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
        response = requests.post(url, headers=headers, json=payload, timeout=40)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ API ఎర్రర్ ({response.status_code}): దయచేసి మీ అడ్మిన్ సెట్టింగ్స్‌లో సరైన కీ లేదా వర్కింగ్ టోకెన్ ఇవ్వండి."
    except Exception as e:
        return f"⚠️ నెట్‌వర్క్ కనెక్షన్ ఎర్రర్: {e}"

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ (ChatGPT Interface) ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} AI Assistant")
    
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

    # చాట్ హిస్టరీ మెమరీ
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # చాట్‌జిపిటి లాగే ఏ ప్రశ్న అడిగినా లైవ్‌లో ఆన్సర్ ఇస్తుంది
    if prompt := st.chat_input("Ask anything (ChatGPT style)..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("AI ఆలోచిస్తోంది... ⏳"):
            current_key = st.session_state.api_key
            if not current_key or current_key == "ఇక్కడ_మీ_AQ_లేదా_AIza_కీ_పేస్ట్_చేయండి":
                reply_text = "⚠️ దయచేసి అడ్మిన్ సెట్టింగ్స్‌లో మీ API Key లేదా AQ Token ఇవ్వండి."
            else:
                # డైరెక్ట్ లైవ్ ఏఐ కాల్
                reply_text = call_chatgpt_style_api(current_key, selected_model, prompt, img_to_send)

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    prompt_event = st.text_input("ఈవెంట్ లేదా వర్క్‌షాప్ గురించి వివరాలు ఇవ్వండి:")
    if prompt_event:
        with st.spinner("ప్లానింగ్ జరుగుతోంది..."):
            current_key = st.session_state.api_key
            res = call_chatgpt_style_api(current_key, "gemini-1.5-flash", f"Plan an event script/details for: {prompt_event}")
            st.write(res)

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker - AI Study Buddy")
    prompt_exam = st.text_input("ఏ సబ్జెక్ట్ లేదా టాపిక్ పై నోట్స్ కావాలి?")
    if prompt_exam:
        with st.spinner("నోట్స్ తయారు చేయబడుతోంది..."):
            current_key = st.session_state.api_key
            res = call_chatgpt_style_api(current_key, "gemini-1.5-flash", f"Provide detailed exam study notes and important points for: {prompt_exam}")
            st.write(res)

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep - Interview Coach")
    prompt_prep = st.text_input("ఏ రోల్ లేదా టెక్నాలజీకి ఇంటర్వ్యూ ప్రిపేర్ అవ్వాలి?")
    if prompt_prep:
        with st.spinner("ఇంటర్వ్యూ క్వశ్చన్స్ సిద్ధం అవుతున్నాయి..."):
            current_key = st.session_state.api_key
            res = call_chatgpt_style_api(current_key, "gemini-1.5-flash", f"Provide top interview questions and answers for: {prompt_prep}")
            st.write(res)
