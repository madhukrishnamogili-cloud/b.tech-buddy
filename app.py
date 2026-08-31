import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="My Smart App", page_icon="🚀", layout="wide")

# 1. 🔑 మీ డీటెయిల్స్ 
DEFAULT_API_KEY = "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"
ADMIN_EMAIL = "madhukrishnamogili@gmail.com" 

# --- సెషన్ స్టేట్ సెటప్ ---
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_API_KEY
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
if "api_status" not in st.session_state:
    st.session_state.api_status = "working" # working or demo

# --- 🚀 One-Time Login ---
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
            if email_input != "" and password_input != "":
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.query_params["user"] = email_input 
                st.rerun()
    st.stop()

# ⬅️ సైడ్‌బార్ & అడ్మిన్ సెట్టింగ్స్
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
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "🎪 Event Planner"])
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.query_params.clear()
        st.rerun()

# --- 🛡️ ఎప్పటికీ క్రాష్ అవ్వని API వాలిడేషన్ ---
current_key = st.session_state.api_key

try:
    if not current_key or current_key == "ఇక్కడ_మీ_API_KEY_పేస్ట్_చేయండి" or current_key.startswith("AQ"):
        raise ValueError("Invalid Key")
        
    genai.configure(api_key=current_key)
    list(genai.list_models()) # Test
    st.session_state.api_status = "working"
except:
    st.session_state.api_status = "demo"
    st.warning("⚠️ గూగుల్ API కీ కనెక్ట్ అవ్వలేదు. యాప్ 'Demo Mode' లో రన్ అవుతోంది! క్రాష్ కాకుండా నేను డమ్మీ ఆన్సర్స్ ఇస్తాను.")

# --- ఆప్షన్ 1: ప్రాజెక్ట్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide")
    
    available_models = ["models/gemini-1.5-flash-latest", "models/gemini-2.5-flash", "demo-model-offline"] 
    selected_model = st.selectbox("🧠 బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models, index=0) 
    
    tab1, tab2, tab3 = st.tabs(["💬 Text Only", "🖼️ Upload Photo", "📸 Take Camera Photo"])
    img_to_send = None

    with tab2:
        uploaded_file = st.file_uploader("గ్యాలరీ నుంచి ఫోటో అప్‌లోడ్ చేయండి", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_to_send = Image.open(uploaded_file)
            st.image(img_to_send, caption="అప్‌లోడ్ చేసిన ఫోటో", width=300)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your doubt..."):
        st.chat_message("user").write(prompt)
        
        with st.spinner("ఆలోచిస్తోంది... ⏳"):
            # ఇక్కడే అసలైన మ్యాజిక్: API లేకపోయినా రిప్లై ఇస్తుంది!
            if st.session_state.api_status == "working":
                try:
                    model = genai.GenerativeModel(selected_model)
                    response = model.generate_content(prompt)
                    reply_text = response.text
                except Exception as e:
                    reply_text = f"సర్వర్ బిజీ బాస్! ఎర్రర్: {e}"
            else:
                # డెమో మోడ్ ఆన్సర్స్
                reply_text = f"*(Demo Mode)*: బాస్, మీరు '{prompt}' అని అడిగారు. ప్రస్తుతానికి నా API కీ పనిచేయట్లేదు కాబట్టి నేను ఆఫ్‌లైన్‌లో ఉన్నాను. కీ అప్‌డేట్ చేయగానే మీకు పర్ఫెక్ట్ ఆన్సర్ ఇస్తాను!"

            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ కూడా డెమో మోడ్ లో యాక్టివ్ గా ఉంటుంది!")
