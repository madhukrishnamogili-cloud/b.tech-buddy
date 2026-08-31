import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ఇక్కడ మీ కీ పర్మనెంట్ గా ఇచ్చేయండి! (డబుల్ కోట్స్ మధ్యలో)
GOOGLE_API_KEY = "AQ.Ab8RN6Kl2MXEXcOEY_sHI9-RQNKh5VrUx6N9P10Cox09OYu5Hw"

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

# కీ సెటప్ & బ్రెయిన్ కనెక్షన్
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("బాస్, పైన కోడ్‌లో API Key కరెక్ట్‌గా ఇచ్చారో లేదో చెక్ చేసుకోండి!")

# ఎడమవైపు సైడ్‌బార్
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("Auto-Login & Camera Mode 📸")
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()
    st.info("Made for Engineering Students")

# --- ఆప్షన్ 1: ప్రాజెక్ట్ గైడ్ (విత్ కెమెరా & ఫోటో అప్‌లోడ్) ---
if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    st.caption("🟢 Connected to Brain: Google Gemini 1.5 Flash") 
    st.markdown("EEE సర్క్యూట్స్, కాంపోనెంట్స్ లేదా కోడింగ్ ఎర్రర్స్ ఫోటో తీసి అడగండి!")
    
    # ఫోటో అప్‌లోడ్ & కెమెరా ఆప్షన్స్
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("🖼️ అప్‌లోడ్ ఫోటో", type=["jpg", "jpeg", "png"])
    with col2:
        camera_photo = st.camera_input("📸 టేక్ ఫోటో (కెమెరా)")

    img_to_send = None
    if uploaded_file:
        img_to_send = Image.open(uploaded_file)
        st.image(img_to_send, caption="మీరు అప్‌లోడ్ చేసిన ఫోటో", width=300)
    elif camera_photo:
        img_to_send = Image.open(camera_photo)
        st.image(img_to_send, caption="మీరు తీసిన ఫోటో", width=300)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
            
            # ఫోటో ఉంటే ఫోటోతో సహా గూగుల్ కి పంపుతాం
            if img_to_send:
                response = model.generate_content([smart_prompt, img_to_send])
            else:
                response = model.generate_content(smart_prompt)
            
            st.chat_message("assistant").write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"ఎర్రర్ ఇదీ బాస్: {e}")

# --- ఆప్షన్ 2: నోట్స్ ---
elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

# --- ఆప్షన్ 3: ప్లేస్‌మెంట్స్ ---
elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

# --- ఆప్షన్ 4: ఈవెంట్ ప్లానర్ ---
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
