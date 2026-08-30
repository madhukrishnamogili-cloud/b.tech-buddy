import streamlit as st
from groq import Groq

st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓")

with st.sidebar:
    st.title("B.Tech Buddy 🎓")
    st.caption("No Settings, No Secrets!")
    st.divider()
    
    # ఇక్కడే డైరెక్ట్ గా కీ ఇచ్చేయొచ్చు
    user_key = st.text_input("🔑 Paste your Groq API Key here:", type="password")
    
    st.divider()
    app_mode = st.radio("Menu:", ["🤖 Project Guide", "📚 Notes"])

if app_mode == "🤖 Project Guide":
    st.header("🤖 Smart Project & Lab Guide")
    
    if not user_key:
        st.warning("👈 బాస్! ముందుగా ఎడమవైపు ఉన్న బాక్స్‌లో మీ Groq API Key ని పేస్ట్ చేసి Enter కొట్టండి.")
        st.stop()
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])
        
    if prompt := st.chat_input("Ask your technical doubt..."):
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        try:
            # లేటెస్ట్ బ్రెయిన్ కనెక్షన్ 
            client = Groq(api_key=user_key)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt + " (Reply in English. Keep it simple for an engineering student.)"}]
            )
            ans = response.choices[0].message.content
            st.chat_message("assistant").write(ans)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"ఎర్రర్ ఇదీ బాస్: {e}")

else:
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")
