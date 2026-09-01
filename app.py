import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Tech Mithra 🎓", page_icon="🚀", layout="wide")

# 1. 🔑 మీ జెమినీ ఏపీఐ కీ ఇక్కడ ఇవ్వండి (లేదా అడ్మిన్ సెట్టింగ్స్ లో మార్చుకోండి)
DEFAULT_API_KEY = "AQ.Ab8RN6JykM1zJkSLPdeI-6wBttjtSwexPHQyQZKAjYhMPfWPwg"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- మెమరీ (Session State) ---
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_API_KEY
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra 🎓"
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
            new_key = st.text_input("API Key:", st.session_state.api_key, type="password")
            
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

# --- 🛡️ ఏపీఐ కాన్ఫిగరేషన్ ---
try:
    current_key = st.session_state.api_key
    if current_key and current_key != "ఇక్కడ_మీ_API_KEY_పేస్ట్_చేయండి":
        genai.configure(api_key=current_key)
except Exception as e:
    pass

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide")
    
    available_models = [
        "models/gemini-2.5-flash",
        "models/gemini-2.5-pro",
        "models/gemini-2.5-flash-preview-tts",
        "models/gemini-2.5-pro-preview-tts",
        "models/gemma-4-26b-a4b-it",
        "models/gemma-4-31b-it",
        "models/gemini-flash-latest",
        "models/gemini-flash-lite-latest",
        "models/gemini-pro-latest"
    ] 
    
    selected_model = st.selectbox("🧠 బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models, index=0) 

    tab1, tab2, tab3 = st.tabs(["💬 Text Only", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab1:
        st.info("💡 ఏదైనా టెక్నికల్ డౌట్ లేదా ప్రశ్న టైప్ చేయండి.")
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
            reply_text = ""
            try:
                # జెమినీ లైవ్ మోడల్ కాల్
                model = genai.GenerativeModel(selected_model)
                current_parts = [prompt]
                if img_to_send is not None:
                    current_parts.append(img_to_send)
                response = model.generate_content(current_parts)
                if response and hasattr(response, 'text'):
                    reply_text = response.text
            except Exception as e:
                reply_text = f"⚠️ ఏపీఐ కనెక్షన్ ఎర్రర్: దయచేసి మీ అడ్మిన్ సెట్టింగ్స్‌లో సరైన ఏపీఐ కీ ఇవ్వండి. (ఎర్రర్: {e})"

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈవెంట్స్ మరియు వర్క్‌షాప్స్ ప్లాన్ చేసుకోవడానికి ఇది ఉపయోగపడుతుంది.")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("ఎగ్జామ్ ప్రిపరేషన్ మరియు ఇంపార్టెంట్ టాపిక్స్.")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("ఇంటర్వ్యూ క్వశ్చన్స్ మరియు ప్రిపరేషన్ గైడ్.")
