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
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()
    st.info("Made for Engineering Students")

# --- ఆప్షన్ 1: ప్రాజెక్ట్ & ల్యాబ్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    st.markdown("EEE సర్క్యూట్స్, కాంపోనెంట్స్ లేదా కోడింగ్ ఎర్రర్స్ డౌట్స్ అడగండి!")

    # 💡 ట్యాబ్స్ ఉపయోగించడం వల్ల కెమెరా ఆటోమేటిక్‌గా ఆన్ అవ్వదు!
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
        st.write("కెమెరాతో ఫోటో తీయడానికి కింద ఆప్షన్ వాడండి:")
        camera_photo = st.camera_input("ఫోటో తీయండి")
        if camera_photo:
            img_to_send = Image.open(camera_photo)
            st.image(img_to_send, caption="తీసిన ఫోటో", width=300)

    # Chat History Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("బడ్డీ ఆలోచిస్తోంది... ⏳"):
            try:
                smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
                
                # ఫోటో ఉంటే ఫోటో + టెక్స్ట్ పంపుతాం
                if img_to_send is not None:
                    response = model.generate_content([smart_prompt, img_to_send])
                else:
                    response = model.generate_content(smart_prompt)

                if response and hasattr(response, 'text'):
                    st.chat_message("assistant").write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("రెస్పాన్స్ సరిగ్గా రాలేదు. దయచేసి మళ్ళీ ప్రయత్నించండి.")
            except Exception as e:
                st.error(f"ఎర్రర్ వచ్చింది బాస్: {e}")

# --- ఇతర ఫీచర్లు ---
elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
