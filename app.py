import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("Dropdown Brain Mode 🚀")
    st.divider()
    
    google_key = st.text_input("🔑 Paste your Google API Key (AIza...):", type="password")
    st.divider()

st.header("🤖 Smart Project & Lab Guide")

if not google_key:
    st.warning("👈 బాస్! ముందుగా ఎడమవైపు ఉన్న బాక్స్‌లో మీ Google API Key ఇచ్చి Enter కొట్టండి.")
    st.stop()

try:
    genai.configure(api_key=google_key)
    
    # గూగుల్ దగ్గర ఉన్న బ్రెయిన్స్ అన్నీ లాక్కొచ్చే లాజిక్
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            
    if not available_models:
        st.error("బాస్! మీ కీ కి ఎలాంటి బ్రెయిన్స్ లింక్ అవ్వలేదు. దయచేసి కొత్త కీ తీసుకోండి.")
        st.stop()
        
    # స్క్రీన్ మీద బ్రెయిన్స్ లిస్ట్ చూపిస్తుంది, మీరు సెలెక్ట్ చేసుకోవచ్చు!
    selected_model = st.selectbox("🧠 మీ ఇష్టం వచ్చిన బ్రెయిన్ సెలెక్ట్ చేసుకోండి:", available_models)
    
    model = genai.GenerativeModel(selected_model)
    st.markdown("EEE కోడింగ్ ఎర్రర్స్ నుంచి, Arduino, PLC ప్రోగ్రామ్స్ & సర్క్యూట్ డౌట్స్ వరకు ఏదైనా అడగండి.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
        response = model.generate_content(smart_prompt)
        
        st.chat_message("assistant").write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
except Exception as e:
    st.error(f"ఎర్రర్ ఇదీ బాస్: {e}")
