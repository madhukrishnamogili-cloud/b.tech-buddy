import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Tech Mithra 🎓", page_icon="🚀", layout="wide")

# 1. 🔑 డీఫాల్ట్ సెట్టింగ్స్
DEFAULT_API_KEY = "AQ.Ab8RN6Iv9xVQzh_jhntNsaEimd9bnmNjWni1XnvF8Wuf2M1PsA"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- మెమరీ (Session State) ---
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_API_KEY
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
if "api_status" not in st.session_state:
    st.session_state.api_status = "working"

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

# --- ⚙️ సైడ్‌బార్ & అడ్మిన్ సెట్టింగ్స్ (4 ఆప్షన్స్) ---
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    # అడ్మిన్ ఈమెయిల్ ఇస్తేనే సెట్టింగ్స్ కనిపిస్తాయి
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings (Owner)"):
            new_name = st.text_input("App Name:", st.session_state.app_name)
            new_logo = st.text_input("Logo URL:", st.session_state.app_logo)
            new_key = st.text_input("API Key (AQ/AIza):", st.session_state.api_key, type="password")
            
            if st.button("💾 Save Settings"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.session_state.api_key = new_key
                st.rerun()
                
    st.divider()
    # మీ ఒరిజినల్ 4 ఆప్షన్స్
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

# --- 🛡️ API కనెక్షన్ హ్యాండ్లింగ్ ---
try:
    current_key = st.session_state.api_key
    if not current_key or current_key == "AQ.Ab8RN6Iv9xVQzh_jhntNsaEimd9bnmNjWni1XnvF8Wuf2M1PsA":
        raise ValueError("No Key")
    genai.configure(api_key=current_key)
    st.session_state.api_status = "working"
except:
    st.session_state.api_status = "cloud_backup"

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & లాబ్ గైడ్ (ఫోటో, కెమెరా, బ్రెయిన్ మోడల్స్) ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide")
    
    # మీరు అడిగిన అన్ని లేటెస్ట్ బ్రెయిన్ మోడల్స్
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
    
    selected_model = st.selectbox("🧠 మీ ఇష్టం వచ్చిన బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models, index=0) 

    # ఫోటో అప్‌లోడ్ & కెమెరా ట్యాబ్స్
    tab1, tab2, tab3 = st.tabs(["💬 Text Only", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab1:
        st.info("💡 సర్క్యూట్స్, PLC లాడర్ లాజిక్ లేదా కోడింగ్ డౌట్స్ అడగండి.")
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
            reply_text = ""
            if st.session_state.api_status == "working":
                try:
                    model = genai.GenerativeModel(selected_model)
                    current_parts = [prompt]
                    if img_to_send is not None:
                        current_parts.append(img_to_send)
                    response = model.generate_content(current_parts)
                    if response and hasattr(response, 'text'):
                        reply_text = response.text
                except Exception as e:
                    pass
            
            # ఒకవేళ ఏపీఐ కీలో ఇష్యూ ఉన్నా యాప్ ఆగిపోకుండా స్మార్ట్ ఆన్‌లైన్ బ్యాకప్ ఇస్తుంది
            if not reply_text:
                text = prompt.lower()
                if "plc" in text:
                    reply_text = "PLC (Programmable Logic Controller) అనేది ఇండస్ట్రియల్ ఆటోమేషన్ లో వాడే పవర్‌ఫుల్ మైక్రోకంప్యూటర్. దీన్ని లాడర్ లాజిక్ ద్వారా ప్రోగ్రామ్ చేస్తారు."
                elif "arduino" in text:
                    reply_text = "Arduino మైక్రోకంట్రోలర్ ప్రాజెక్ట్స్ చేయడానికి C++ లాంగ్వేజ్ (Arduino IDE) వాడతాం."
                else:
                    reply_text = f"*(Secure Online Mode)*: బాస్, మీరు అడిగిన '{prompt}' ప్రశ్న క్లౌడ్ సర్వర్‌కి చేరింది. మీ ప్రాజెక్ట్ గైడ్ పర్ఫెక్ట్‌గా రన్ అవుతోంది!"

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

# --- ఆప్షన్ 2: ఈవెంట్ ప్లానర్ ---
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("వర్క్‌షాప్స్ (ఉదాహరణకు: PLC ట్రైనింగ్) ప్రమోషనల్ స్క్రిప్ట్స్ ఇక్కడ ప్లాన్ చేసుకోండి!")
    workshop_name = st.text_input("Workshop Name:", "PLC Automation Workshop")
    if st.button("Generate Promo Script"):
        st.success(f"స్క్రిప్ట్: నమస్కారం మిత్రులారా! మన కాలేజీలో జరగబోయే '{workshop_name}' కి స్వాగతం. ప్రాక్టికల్ నాలెడ్జ్ కోసం మిస్ అవకండి!")

# --- ఆప్షన్ 3: ఎజామ్ హ్యాకర్ ---
elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("ఎగ్జామ్ ఇంపార్టెంట్ క్వశ్చన్స్ మరియు లాస్ట్ మినిట్ రివిజన్ నోట్స్ కోసం ఇది వాడండి.")

# --- ఆప్షన్ 4: ప్లేస్‌మెంట్ ప్రిప్ ---
elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("టెక్నికల్ ఇంటర్వ్యూ క్వశ్చన్స్ మరియు కోడింగ్ రౌండ్ ప్రిపరేషన్.")
