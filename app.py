import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ఇక్కడ మీ AIza... కీ పర్మనెంట్ గా ఇవ్వండి
GOOGLE_API_KEY = "AQ.Ab8RN6Jy4r-iCHqbNbl-5TmQOoDwK2Hdm8Pu6xgH1F1exsG-Nw"

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

# API Configuration
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("బాస్, API Key కరెక్ట్‌గా ఉందో లేదో చెక్ చేయండి!")

# ఎడమవైపు సైడ్‌బార్
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("Smart AI Assistant 🚀")
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Note…
[07:51, 8/31/2026] ᴍᴀᴅʜᴜ ᴋʀɪsʜɴᴀ 👑: import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ఇక్కడ మీ AIza... కీ పర్మనెంట్ గా ఇవ్వండి
GOOGLE_API_KEY = "ఇక్కడ_మీ_API_KEY_పేస్ట్_చేయండి"

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("బాస్, API Key కరెక్ట్‌గా ఉందో లేదో చెక్ చేయండి!")

# ఎడమవైపు సైడ్‌బార్
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("Memory & Brain Select 🧠")
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    
    st.divider()
    # --- బ్రెయిన్ సెలెక్ట్ డ్రాప్‌డౌన్ మళ్ళీ తెచ్చాం ---
    st.markdown("### 🧠 Select Brain")
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except:
        pass
    
    selected_model = "models/gemini-1.5-flash"
    if available_models:
        # డీఫాల్ట్ గా 1.5-flash ఉండేలా సెట్టింగ్
        default_idx = available_models.index("models/gemini-1.5-flash") if "models/gemini-1.5-flash" in available_models else 0
        selected_model = st.selectbox("Choose AI Model:", available_models, index=default_idx)
    
    model = genai.GenerativeModel(selected_model)
    
    st.divider()
    # పాత చాట్ తుడిపేయడానికి క్లియర్ బటన్
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & ల్యాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    st.markdown("EEE సర్క్యూట్స్, కాంపోనెంట్స్ ఫోటో తీసి అడగండి. నేను పాత ప్రశ్నలు కూడా గుర్తుపెట్టుకుంటాను!")

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

    # చాట్ హిస్టరీ (మెమరీ) సెటప్
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # పాత మెసేజ్‌లు స్క్రీన్ మీద చూపించడానికి
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # కొత్త ప్రశ్న అడగడం
    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        
        with st.spinner("బడ్డీ ఆలోచిస్తోంది... ⏳"):
            try:
                smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
                
                # --- కంటిన్యూస్ చాట్ లాజిక్ ఇక్కడే ఉంది ---
                gemini_history = []
                for msg in st.session_state.messages:
                    # గూగుల్ కి అర్థం అయ్యేలా పాత చాట్ ని ఫార్మాట్ చేస్తున్నాం
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg["content"]]})
                
                # కొత్త ప్రశ్న మరియు ఫొటో (ఉంటే) యాడ్ చేయడం
                current_parts = [smart_prompt]
                if img_to_send is not None:
                    current_parts.append(img_to_send)
                    
                gemini_history.append({"role": "user", "parts": current_parts})
                
                # పాత మెమరీ + కొత్త ప్రశ్న అంతా కలిపి బ్రెయిన్ కి పంపుతున్నాం
                response = model.generate_content(gemini_history)

                if response and hasattr(response, 'text'):
                    st.chat_message("assistant").write(response.text)
                    # UI హిస్టరీ లో సేవ్ చేయడం
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("రెస్పాన్స్ సరిగ్గా రాలేదు. దయచేసి మళ్ళీ ప్రయత్నించండి.")
            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది బాస్: {e}")

# --- మిగతా ఫీచర్లు ---
elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
