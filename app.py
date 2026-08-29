import streamlit as st
from groq import Groq

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

# కొత్త Llama-3 బ్రెయిన్ కనెక్షన్
try:
    GROQ_API_KEY = st.secrets["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"]
    client = Groq(api_key=GROQ_API_KEY)
except KeyError:
    st.error("బాస్! Streamlit Secrets లో GROQ_API_KEY పెట్టడం మర్చిపోయారు. ఒకసారి చెక్ చేయండి.")
    st.stop()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("All-in-one Campus AI")
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()

if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    st.caption("🟢 Connected to Brain: Llama-3 (Groq)") 
    st.markdown("EEE కోడింగ్ ఎర్రర్స్ నుంచి, IoT, ఎలక్ట్రానిక్స్ & సర్క్యూట్ డౌట్స్ వరకు ఏదైనా అడగండి.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            smart_prompt = prompt + " (Reply in English. Keep it simple and easy to understand for an engineering student.)"
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": smart_prompt}],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"అసలు ఎర్రర్ ఇదీ బాస్: {e}")

elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
