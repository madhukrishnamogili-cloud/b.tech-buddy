import streamlit as st
from groq import Groq

# యాప్ డిజైన్ సెట్టింగ్స్
st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

# ఎడమ వైపున సైడ్‌బార్ మెనూ
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("All-in-one Campus AI")
    st.divider()
    
    # డైరెక్ట్ గా కీ అడిగే కొత్త బాక్స్!
    api_key_input = st.text_input("🔑 Enter Groq API Key:", type="password")
    st.caption("Get free key from console.groq.com")
    
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()
    st.info("Made for Engineering Students")

# 1. ప్రాజెక్ట్ & ల్యాబ్ గైడ్
if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    
    # కీ ఇవ్వకపోతే యాప్ ఆగిపోయి వార్నింగ్ ఇస్తుంది
    if not api_key_input:
        st.warning("👈 బాస్! ముందుగా ఎడమవైపు ఉన్న బాక్స్‌లో మీ Groq API Key ని పేస్ట్ చేయండి.")
        st.stop()
        
    try:
        # మీరు ఇచ్చిన కీ తో బ్రెయిన్ కనెక్ట్ అవుతుంది
        client = Groq(api_key=api_key_input)
        st.caption("🟢 Connected to Brain: Llama-3 (Groq)") 
        st.markdown("EEE కోడింగ్ ఎర్రర్స్ నుంచి, IoT, ఎలక్ట్రానిక్స్ & సర్క్యూట్ డౌట్స్ వరకు ఏదైనా అడగండి.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask your technical doubt..."):
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": smart_prompt}],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    except Exception as e:
        st.error(f"మీరు ఇచ్చిన కీ తప్పు బాస్! ఎర్రర్: {e}")

# మిగతా ఫీచర్స్
elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
