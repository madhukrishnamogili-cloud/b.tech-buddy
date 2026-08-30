import streamlit as st
import google.generativeai as genai

# పేజీ డిజైన్
st.set_page_config(page_title="B.Tech Buddy", page_icon="🎓", layout="wide")

# ఎడమవైపు సైడ్‌బార్ మెనూ
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("B.Tech Buddy 🎓")
    st.caption("All-in-one Campus AI ⚡")
    st.divider()
    
    # కీ అడిగే బాక్స్
    google_key = st.text_input("🔑 Paste your Google API Key (AIza...):", type="password")
    st.divider()
    
    # మీరు అడిగిన 4 ఆప్షన్స్ ఇక్కడే ఉన్నాయి!
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "📚 Exam Hacker (Notes)", "💼 Placement Prep", "🎪 Event Planner"])
    st.divider()
    st.info("Made for Engineering Students")

# --- ఆప్షన్ 1: అసలైన బడ్డీ (వర్కింగ్) ---
if app_mode == "🤖 Project & Lab Guide":
    st.header("🤖 Smart Project & Lab Guide")

    if not google_key:
        st.warning("👈 బాస్! ముందుగా ఎడమవైపు ఉన్న బాక్స్‌లో మీ Google API Key ఇచ్చి Enter కొట్టండి.")
        st.stop()

    try:
        genai.configure(api_key=google_key)
        
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
                
        if not available_models:
            st.error("బాస్! మీ కీ కి ఎలాంటి బ్రెయిన్స్ లింక్ అవ్వలేదు.")
            st.stop()
            
        # బ్రెయిన్ సెలెక్షన్ డ్రాప్‌డౌన్
        selected_model = st.selectbox("🧠 మీ ఇష్టం వచ్చిన బ్రెయిన్ సెలెక్ట్ చేసుకోండి (flash మోడల్స్ బెస్ట్):", available_models)
        
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

# --- ఆప్షన్ 2: నోట్స్ ఫీచర్ ---
elif app_mode == "📚 Exam Hacker (Notes)":
    st.header("📚 Exam Hacker: Smart Notes")
    st.info("ఈ ఫీచర్ త్వరలో వస్తుంది బాస్! ఎగ్జామ్స్ ముందు సిలబస్ ని షార్ట్ నోట్స్ గా మార్చే ట్రిక్ ఇక్కడ యాడ్ చేద్దాం.")

# --- ఆప్షన్ 3: ప్లేస్‌మెంట్స్ ---
elif app_mode == "💼 Placement Prep":
    st.header("💼 Placement & Interview Prep")
    st.info("ఈ ఫీచర్ డెవలప్‌మెంట్‌లో ఉంది. త్వరలో రెజ్యూమె బిల్డింగ్ అండ్ ఇంటర్వ్యూ టిప్స్ వస్తాయి!")

# --- ఆప్షన్ 4: ఈవెంట్ ప్లానర్ ---
elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.info("ఈ ఫీచర్ ఇంకా డెవలప్‌మెంట్‌లో ఉంది బాస్! ఫ్యూచర్ లో మీరు సాయి స్ఫూర్తి ఇన్‌స్టిట్యూట్‌లో హిమాన్షు కుమార్ గారితో PLC వర్క్‌షాప్ లాంటి ఈవెంట్స్ ఆర్గనైజ్ చేసేటప్పుడు, కావాల్సిన పోస్టర్ డిజైన్స్, ప్రమోషనల్ వీడియో స్క్రిప్ట్స్ అన్నీ ఈ బడ్డీనే ఆటోమేటిక్‌గా ప్లాన్ చేసి ఇస్తుంది.")
