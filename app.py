import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("Auto-Brain Detection Mode ⚡")
    st.divider()
    
    google_key = st.text_input("🔑 Paste your Google API Key (AIza...):", type="password")
    
    st.divider()
    st.info("Made for Engineering Students")

st.header("🤖 Smart Project & Lab Guide")

if not google_key:
    st.warning("👈 బాస్! ముందుగా ఎడమవైపు ఉన్న బాక్స్‌లో మీ Google API Key (AIza...) పేస్ట్ చేసి Enter కొట్టండి.")
    st.stop()

try:
    genai.configure(api_key=google_key)
    
    # 🧠 మ్యాజిక్ ఇక్కడే ఉంది: మీ కీ కి ఏ బ్రెయిన్స్ ఉన్నాయో కోడ్ అదే వెతుకుతుంది
    available_brains = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_brains:
        st.error("బాస్! మీ API కీ కి ఏ బ్రెయిన్ యాక్సెస్ లేదు. దయచేసి కొత్త కీ జనరేట్ చేసుకోండి.")
        st.stop()
        
    # ఉన్నవాటిలో ఫాస్ట్ అండ్ బెస్ట్ బ్రెయిన్ ని సెలెక్ట్ చేస్తుంది
    best_brain = available_brains[0]
    for brain in available_brains:
        if "flash" in brain:
            best_brain = brain
            break
        elif "pro" in brain:
            best_brain = brain
            
    model = genai.GenerativeModel(best_brain)
    
    st.caption(f"🟢 Connected to Brain: {best_brain}") 
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
