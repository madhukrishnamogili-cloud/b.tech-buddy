import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="My Smart App", page_icon="🚀", layout="wide")

# 1. ఇక్కడ మీ API కీ మరియు అడ్మిన్ ఈమెయిల్ ఇవ్వండి
GOOGLE_API_KEY = "AQ.Ab8RN6L8o3LNHF0t02xQz640oWR4bcoQt6dJyPkv_HsbOmrRzQ"
ADMIN_EMAIL = "madhukrishnamogiili@gmail.com" 

# --- 🚀 One-Time Login (Persistent) లాజిక్ ---
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

# --- 📱 మెయిన్ యాప్ ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    pass

with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
    
    # 👑 అడ్మిన్ యాక్సెస్ 
    if st.session_state.user_email == ADMIN_EMAIL:
        with st.expander("⚙️ Admin Settings (Only for you)"):
            new_name = st.text_input("Change App Name:", st.session_state.app_name)
            new_logo = st.text_input("Change Logo URL:", st.session_state.app_logo)
            if st.button("Save Changes"):
                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo
                st.rerun()
                
    st.divider()
    # ఇక్కడ Event Planner యాడ్ చేశాను
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.query_params.clear()
        st.rerun()

# --- ఆప్షన్ 1: ప్రాజెక్ట్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 Welcome to {st.session_state.app_name}")
    
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except Exception as e:
        pass
    
    selected_model = "models/gemini-1.5-flash"
    if available_models:
        default_idx = available_models.index("models/gemini-1.5-flash") if "models/gemini-1.5-flash" in available_models else 0
        selected_model = st.selectbox("🧠 బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models, index=default_idx)
    
    model = genai.GenerativeModel(selected_model)

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
        
        with st.spinner("ఆలోచిస్తోంది... ⏳"):
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

# --- ఆప్షన్ 2 & 3 ---
elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("Coming soon!")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement Prep")
    st.info("Coming soon!")

# --- ఆప్షన్ 4: ఈవెంట్ ప్లానర్ (కొత్త ఫీచర్) ---
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.markdown("వర్క్‌షాప్స్ కోసం ప్రమోషనల్ స్క్రిప్ట్స్, పోస్టర్ డిజైన్ ప్రాంప్ట్స్ ఇక్కడ క్రియేట్ చేసుకోండి.")
    
    with st.form("event_form"):
        col1, col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Workshop Name (ఉదా: PLC Automation Workshop)")
            trainer_name = st.text_input("Trainer/Guest Name (ఉదా: Himanshu Kumar)")
        with col2:
            event_date = st.text_input("Dates (ఉదా: Aug 17 & 18)")
            target_audience = st.text_input("Target Audience (ఉదా: EEE Final Year Students)")
            
        submit_btn = st.form_submit_button("Generate Promo Ideas 🚀")
        
    if submit_btn and event_name:
        with st.spinner("ఐడియాస్ రెడీ చేస్తున్నాను... ⏳"):
            try:
                ep_model = genai.GenerativeModel("gemini-1.5-flash")
                ep_prompt = f"Create a short, energetic promotional script in Telugu for a college workshop named '{event_name}' conducted by '{trainer_name}' on '{event_date}' for '{target_audience}'. Also, provide 2 highly detailed image generation prompts (specifying cinematic lighting, 16:9 aspect ratio, and camera angles) to design a poster for this event."
                ep_response = ep_model.generate_content(ep_prompt)
                st.success("ఐడియాస్ రెడీ!")
                st.write(ep_response.text)
            except Exception as e:
                st.error("ఎర్రర్ వచ్చింది బాస్, పైన బ్రెయిన్ కనెక్ట్ అయ్యిందో లేదో చూడండి.")
