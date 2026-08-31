import streamlit as st
from PIL import Image

st.set_page_config(page_title="Tech Mithra", page_icon="🎓", layout="wide")

# --- 💾 సెషన్ స్టేట్ (మెమరీ) సెటప్ ---
if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra 🎓"
if "app_logo" not in st.session_state:
    st.session_state.app_logo = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 🚀 One-Time Login ---
if "user" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.user_email = st.query_params["user"]
else:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

if not st.session_state.logged_in:
    st.markdown(f"<h1 style='text-align: center;'>🔐 Login to {st.session_state.app_name}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email_input = st.text_input("📧 Email Address")
        password_input = st.text_input("🔑 Password", type="password")
        if st.button("🚀 Login", use_container_width=True):
            if email_input and password_input:
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.query_params["user"] = email_input 
                st.rerun()
    st.stop()

# ⬅️ సైడ్‌బార్
with st.sidebar:
    st.image(st.session_state.app_logo, width=100)
    st.title(st.session_state.app_name)
                
    st.divider()
    app_mode = st.radio("Select Feature:", ["🤖 Project & Lab Guide", "🎪 Event Planner", "📚 Exam Hacker"])
    st.divider()
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.query_params.clear()
        st.rerun()

# 🧠 ఆఫ్‌లైన్ స్మార్ట్ బ్రెయిన్ లాజిక్ (No API Required)
def get_offline_response(user_text):
    text = user_text.lower()
    if "plc" in text or "automation" in text:
        return "PLC (Programmable Logic Controller) అనేది ఇండస్ట్రియల్ ఆటోమేషన్ లో వాడే పవర్‌ఫుల్ మైక్రోకంప్యూటర్. దీన్ని లాడర్ లాజిక్ (Ladder Logic) ఉపయోగించి ప్రోగ్రామ్ చేస్తారు. ఇది సెన్సార్స్ నుంచి డేటా తీసుకుని మోటార్స్, వాల్వ్స్ ని కంట్రోల్ చేస్తుంది."
    elif "arduino" in text or "led" in text:
        return "Arduino లో LED బ్లింక్ చేయడానికి చాలా సింపుల్ కోడ్ ఉంటుంది:\n```cpp\nvoid setup() {\n  pinMode(LED_BUILTIN, OUTPUT);\n}\nvoid loop() {\n  digitalWrite(LED_BUILTIN, HIGH);\n  delay(1000);\n  digitalWrite(LED_BUILTIN, LOW);\n  delay(1000);\n}\n```"
    elif "iot" in text or "protocol" in text:
        return "IoT (Internet of Things) లో డివైజెస్ మాట్లాడుకోవడానికి ఒక ప్రోటోకాల్ స్టాక్ ఉంటుంది. అందులో MQTT, HTTP, CoAP లాంటివి వాడతాం. ఇవి డేటాని ఫాస్ట్ గా క్లౌడ్ కి పంపుతాయి."
    elif "converter" in text or "ac" in text or "dc" in text:
        return "ఎలక్ట్రిక్ వెహికల్ (EV) ఛార్జర్లలో వాడే 3-Phase Totem-Pole AC-DC కన్వర్టర్స్ చాలా ఎఫిషియంట్ గా పనిచేస్తాయి. ఇవి పవర్ ఫ్యాక్టర్ ని కరెక్ట్ చేస్తూ వోల్టేజ్ ని స్టెబుల్ గా ఉంచుతాయి."
    else:
        return f"బాస్, మీరు '{user_text}' గురించి అడిగారు. నా ఆఫ్‌లైన్ మోడ్‌లో దీనికి సంబంధించిన బేసిక్ డేటా మాత్రమే ఉంది. సిస్టమ్ అప్‌గ్రేడ్ అవ్వగానే పూర్తి డీటెయిల్స్ ఇస్తాను!"

# --- ఆప్షన్ 1: ప్రాజెక్ట్ గైడ్ ---
if app_mode == "🤖 Project & Lab Guide":
    st.header(f"🤖 {st.session_state.app_name} Lab Guide (Offline Mode)")
    st.success("✅ యాప్ ఎలాంటి API కీ లేకుండా 100% సేఫ్ గా రన్ అవుతోంది!")
    
    tab1, tab2 = st.tabs(["💬 Text Only", "🖼️ Upload Photo"])
    
    with tab2:
        uploaded_file = st.file_uploader("గ్యాలరీ నుంచి ఫోటో అప్‌లోడ్ చేయండి", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(Image.open(uploaded_file), caption="అప్‌లోడ్ చేసిన ఫోటో", width=300)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask your EEE / Automation doubt..."):
        st.chat_message("user").write(prompt)
        
        with st.spinner("ఆలోచిస్తోంది... ⏳"):
            reply_text = get_offline_response(prompt)
            st.chat_message("assistant").write(reply_text)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

elif app_mode == "🎪 Event Planner":
    st.header("🎪 Technical Event & Workshop Planner")
    st.markdown("వర్క్‌షాప్స్ (ఉదాహరణకు: PLC ట్రైనింగ్) ప్లాన్ చేయడానికి ఇది రెడీగా ఉంది!")
    if st.button("Generate Demo Script"):
         st.write("స్క్రిప్ట్: నమస్కారం మిత్రులారా! మన కాలేజీలో జరగబోయే ఈ అద్భుతమైన టెక్నికల్ వర్క్‌షాప్‌కి మీకందరికీ స్వాగతం. ఈ రెండు రోజులు ప్రాక్టికల్ నాలెడ్జ్ తో పాటు సర్టిఫికేషన్ కూడా ఉంటుంది. డోంట్ మిస్!")

elif app_mode == "📚 Exam Hacker":
    st.header("📚 Exam Hacker")
    st.info("నోట్స్ అప్‌లోడ్ ఫీచర్ త్వరలో వస్తుంది!")
