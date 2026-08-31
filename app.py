import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ఇక్కడ మీ కీ పర్మనెంట్ గా ఇచ్చేయండి! (AIza... తో మొదలయ్యేది)
GOOGLE_API_KEY = "AQ.Ab8RN6Jy4r-iCHqbNbl-5TmQOoDwK2Hdm8Pu6xgH1F1exsG-Nw"

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("Pro Mode: Camera & AI Select 🚀")
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()
    st.info("Made for Engineering Students")

if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # బ్రెయిన్ సెలెక్ట్ చేసుకునే ఆప్షన్ మళ్ళీ తెచ్చాం!
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
                
        if not available_models:
            st.error("బాస్! మీ కీ కి ఎలాంటి బ్రెయిన్స్ లింక్ అవ్వలేదు.")
            st.stop()
            
        selected_model = st.selectbox("🧠 మీ ఇష్టం వచ్చిన బ్రెయిన్ సెలెక్ట్ చేసుకోండి (flash మోడల్స్ బెస్ట్):", available_models)
        model = genai.GenerativeModel(selected_model)
        
        st.markdown("EEE సర్క్యూట్స్, కాంపోనెంట్స్ లేదా కోడింగ్ ఎర్రర్స్ ఫోటో తీసి అడగండి!")
        
        # కెమెరా & ఫోటో ఆప్షన్స్
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

        # చాటింగ్ ఫీచర్
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask your technical doubt..."):
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
            
            if img_to_send:
                response = model.generate_content([smart_prompt, img_to_send])
            else:
                response = model.generate_content(smart_prompt)
            
            st.chat_message("assistant").write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"ఎర్రర్ ఇదీ బాస్: పైన కీ కరెక్ట్ గా ఇచ్చారో లేదో చూడండి. ({e})")

elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
