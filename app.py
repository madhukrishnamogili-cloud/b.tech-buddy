import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("All-in-one Campus AI")
    st.divider()
    
    # గూగుల్ కీ కోసం డైరెక్ట్ బాక్స్! 
    google_key = st.text_input("🔑 Paste your Google API Key (AIza...):", type="password")
    
    st.divider()
    st.info("Made for Engineering Students")

st.header("🤖 Smart Project & Lab Guide")

# కీ ఇవ్వకపోతే వార్నింగ్
if not google_key:
    st.warning("👈 బాస్! ముందుగా ఎడమవైపు ఉన్న బాక్స్‌లో మీ Google API Key (AIza... తో మొదలయ్యేది) పేస్ట్ చేసి Enter కొట్టండి.")
    st.stop()

# కీ ఇస్తే బ్రెయిన్ ఆక్టివేట్ అవుతుంది
try:
    genai.configure(api_key=google_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.caption("🟢 Connected to Brain: Google Gemini 1.5 Flash") 
    st.markdown("EEE కోడింగ్ ఎర్రర్స్ నుంచి, Arduino, PLC ప్రోగ్రామ్స్ & సర్క్యూట్ డౌట్స్ వరకు ఏదైనా అడగండి.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # బడ్డీ ఆన్సర్ జనరేట్ చేస్తుంది
        smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
        response = model.generate_content(smart_prompt)
        
        st.chat_message("assistant").write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
except Exception as e:
    st.error(f"ఎర్రర్ ఇదీ బాస్: {e}")
