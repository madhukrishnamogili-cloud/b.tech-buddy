import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="My Smart App", page_icon="🚀", layout="wide")

# 1. 🔑 మీ డీటెయిల్స్ ఇక్కడ పక్కాగా ఇవ్వండి
GOOGLE_API_KEY = "AQ.Ab8RN6IDawkH4l8a-tNnkZEA_VTyDBHuAJL2IzMv21ChTQjuqw"
ADMIN_EMAIL = "madhukkrishnamogilii@gmail.com" 

# --- 🚀 One-Time Login (Persistent) ---
if "user" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.user_email = st.query_params["user"]
else:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 🔐 లాగిన్ పేజీ ---
if not st.session_state.logged_in:
    st.markdown(f"<h1 style='text-align: center;'>🔐 Login to {st.session_state.app_name}</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email_input = st.text_input("📧 Email Address")
        password_input = st.text_input("🔑 Password", type="password")
        
        if st.button("🚀 Login", use_container_width=True):
            if email_input != "" and password_input != "":
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.query_params["user"] = email_input 
                st.rerun()
            else:
                st.error("బాస్, ఈమెయిల్ మరియు పాస్‌వర్డ్ కచ్చితంగా ఇవ్వాలి!")
    st.stop()

# --- 📱 మెయిన్ యాప్ ప్రారంభం ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("API Key కనెక్ట్ అవ్వలేదు బాస్!")

# ⬅️ సైడ్‌బార్ & ⚙️ అడ్మిన్ సెట్టింగ్స్
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings (Only for you)"):
            st.info("యాప్ ఓనర్ సెట్టింగ్స్")
            new_name = st.text_input("Change App Name:", st.session_state.app_name)
            new_logo = st.text_input("Change Logo URL:", st.session_state.app_logo)
            if st.button("Save Changes"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.rerun()
                
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "🎪 Event Planner", "📚 Exam Hacker", "💼 Placement Prep"])
    st.divider()
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.query_params.clear()
        st.rerun()

# --- ఆప్షన్ 1: ప్రాజెక్ట్ గైడ్ & 🧠 బ్రెయిన్ ఆప్షన్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide")
    
    # 🧠 మీరు పంపిన ఫోటోలోని మోడల్స్ లిస్ట్
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
    
    selected_model = st.selectbox("🧠 మీ ఇష్టం వచ్చిన బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models, index=6) # డీఫాల్ట్ గా flash-latest సెట్ చేశాను
    model = genai.GenerativeModel(selected_model)

    st.markdown("కాంపోనెంట్స్ ఫోటో తీసి అడగండి.")

    tab1, tab2, tab3 = st.tabs(["💬 Text Only", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab1:
        st.info("💡 కేవలం ప్రశ్న టైప్ చేసి డౌట్ అడగడానికి ఇది వాడండి.")
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
        
        with st.spinner(f"{selected_model} ఆలోచిస్తోంది... ⏳"):
            try:
                smart_prompt = prompt + " (Reply in English. Keep it simple.)"
                gemini_history = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg["content"]]})
                
                current_parts = [smart_prompt]
                if img_to_send is not None:
                    current_parts.append(img_to_send)
                    
                gemini_history.append({"role": "user", "parts": current_parts})
                
                response = model.generate_content(gemini_history)

                if response and hasattr(response, 'text'):
                    st.chat_message("assistant").write(response.text)
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది బాస్: {e}")

# --- ఆప్షన్ 2: ఈవెంట్ ప్లానర్ ---
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("వర్క్‌షాప్స్ కోసం ఐడియాస్ ఇక్కడ ప్లాన్ చేసుకోండి!")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("Coming soon!")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("Coming soon!")
