import streamlit as st
import google.generativeai as genai

# యాప్ డిజైన్ సెట్టింగ్స్
st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

# ఇక్కడ మీ API కీ వేయండి
GOOGLE_API_KEY = "AQ.Ab8RN6L0c4Cts6nWD4wV7Q5NyzuVVe-5jSl6J34Am18XkTxJDQ"
genai.configure(api_key=GOOGLE_API_KEY)

# గూగుల్ చెప్పిన లేటెస్ట్ బ్రెయిన్ మోడల్ ఇదే!
model = genai.GenerativeModel('gemini-3.6-flash')

# ఎడమ వైపున సైడ్‌బార్ మెనూ
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("All-in-one Campus AI")
    st.divider()
    app_mode = st.radio("Select Feature:", 
                        ["🤖 Project & Lab Guide", 
                         "📚 Exam Hacker (Notes)", 
                         "💼 Placement Prep", 
                         "🎪 Event Planner"])
    st.divider()
    st.info("Made for Engineering Students")

# 1. ప్రాజెక్ట్ & ల్యాబ్ గైడ్
if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")
    
    st.caption("🟢 Connected to Brain: gemini-3.6-flash") 
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
            response = model.generate_content(smart_prompt)
            st.chat_message("assistant").write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"అసలు ఎర్రర్ ఇదీ బాస్: {e}")

# 2. ఎగ్జామ్ హ్యాకర్ 
elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

# 3. ప్లేస్‌మెంట్స్ ప్రిపరేషన్ 
elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")

# 4. ఈవెంట్ & వర్క్‌షాప్ ప్లానర్ 
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది బాస్!")