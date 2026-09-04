# ============================================================
# TECH MITHRA AI PRO - COMPLETE app.py
# NO STREAM SELECT | FAST AI ANSWERS
#
# requirements.txt:
# streamlit
# google-genai
# Pillow
#
# Streamlit Secrets:
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
#
# Run:
# streamlit run app.py
# ============================================================

import streamlit as st
from google import genai
from PIL import Image
import io
import textwrap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# APP SETTINGS
# ============================================================

APP_NAME = "🚀 Tech Mithra AI Pro"

# Fast models
MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
]


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client(api_key):
    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# ============================================================
# FAST AI FUNCTION
# ============================================================

def ask_ai(question, instruction="", image=None):

    api_key = get_api_key()

    if not api_key:
        return None

    client = get_client(api_key)

    if client is None:
        return None

    prompt = f"""
{instruction}

User question:
{question}

IMPORTANT:
- Answer directly.
- If the question is short, give a short answer.
- Do not unnecessarily give a very long answer.
- Use simple and clear English.
- Give accurate information.
"""

    contents = prompt

    if image is not None:
        contents = [prompt, image]

    for model_name in MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )

            if response and getattr(response, "text", None):
                return response.text.strip()

        except Exception:
            continue

    return None


# ============================================================
# LOCAL FAST FALLBACK
# ============================================================

def local_answer(question):

    q = question.lower().strip()

    if q in ["hi", "hello", "hey"]:
        return "Hello! 👋 How can I help you?"

    if "what is ev" in q or "what is electric vehicle" in q:
        return """
### 🚗 What is an EV?

EV stands for **Electric Vehicle**.

An Electric Vehicle uses an electric motor and battery power instead of a petrol or diesel engine.

**Examples:** Electric cars, bikes and buses.
"""

    if "what is python" in q:
        return """
### 🐍 What is Python?

Python is a high-level, easy-to-learn programming language.

It is used for:
- AI
- Web development
- Data science
- Automation
"""

    if "what is iot" in q:
        return """
### 🌐 What is IoT?

IoT stands for **Internet of Things**.

It connects physical devices to the internet so they can collect and exchange data.

**Examples:** Smart homes, smart watches and smart agriculture.
"""

    if "what is ethics" in q:
        return """
### What is Ethics?

Ethics refers to moral principles that guide a person's behaviour and decisions.

It helps us understand what is right and wrong.
"""

    return f"""
### Answer

**{question}** is an important topic.

Please check your Gemini API key and internet connection for a complete AI-generated answer.
"""


# ============================================================
# MAIN CHAT ANSWER
# ============================================================

def get_answer(question, image=None):

    instruction = """
You are Tech Mithra AI Pro, a helpful AI assistant like ChatGPT.

Answer any general, academic, technical, educational or career question.

For small questions:
Give a fast and concise answer.

For questions asking for explanation:
Give a clear explanation with headings and bullet points.

For exam questions:
Give definition, explanation, key points and conclusion.

Be friendly, accurate and easy to understand.
"""

    answer = ask_ai(
        question,
        instruction,
        image
    )

    if answer:
        return answer

    return local_answer(question)


# ============================================================
# EVENT PLANNER
# ============================================================

def generate_event_plan(event_name, event_type, audience):

    prompt = f"""
Create a complete and practical event plan.

Event Name: {event_name}
Event Type: {event_type}
Target Audience: {audience}
"""

    instruction = """
You are an expert college event planner.

Create a clear event plan including:

1. Event Objective
2. Event Description
3. Target Audience
4. Required Resources
5. Team Responsibilities
6. Complete Event Schedule
7. Budget Categories
8. Promotion Plan
9. Expected Outcomes

Keep it practical.
"""

    answer = ask_ai(
        prompt,
        instruction
    )

    if answer:
        return answer

    return f"""
# 📋 Event Plan: {event_name}

## Event Type
{event_type}

## Target Audience
{audience}

## Objective
To provide knowledge, learning and practical exposure to participants.

## Suggested Schedule

- 09:00 AM – Registration
- 09:30 AM – Inauguration
- 10:00 AM – Main Session
- 11:30 AM – Break
- 12:00 PM – Practical Session
- 01:30 PM – Lunch
- 02:30 PM – Interactive Session
- 04:00 PM – Feedback
- 04:30 PM – Certificate Distribution

## Requirements
- Venue
- Projector
- Laptop
- Internet
- Volunteers
- Registration Desk
- Certificates

## Promotion
- WhatsApp
- Instagram
- College Notice Board
- Classroom Announcements
"""


# ============================================================
# IMAGE PROMPT
# ============================================================

def generate_image_prompt(event_name, event_type, audience):

    prompt = f"""
Create one detailed AI image generation prompt for a college event poster.

Event Name: {event_name}
Event Type: {event_type}
Audience: {audience}
"""

    instruction = """
You are an expert AI image prompt writer.

Generate only one professional and detailed image prompt.
"""

    answer = ask_ai(
        prompt,
        instruction
    )

    if answer:
        return answer

    return f"""
Create a professional modern college event poster for "{event_name}",
event type "{event_type}", target audience "{audience}",
modern academic atmosphere, students, technology theme,
professional typography space, cinematic lighting,
high quality, realistic, 4K, vertical poster design.
"""


# ============================================================
# LOGIN
# ============================================================

try:
    saved_user = st.query_params.get("user", "")

    if saved_user and not st.session_state.logged_in:
        st.session_state.logged_in = True
        st.session_state.user_email = saved_user

except Exception:
    pass


if not st.session_state.logged_in:

    st.title("🚀 Tech Mithra AI Pro")

    st.subheader("🔐 Login")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email = st.text_input("📧 Email Address")

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if email.strip() and password.strip():

                st.session_state.logged_in = True

                st.session_state.user_email = email.strip()

                try:
                    st.query_params["user"] = email.strip()
                except Exception:
                    pass

                st.rerun()

            else:

                st.error(
                    "Please enter Email and Password."
                )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(APP_NAME)

    st.caption(
        f"Logged in: {st.session_state.user_email}"
    )

    st.divider()

    app_mode = st.radio(
        "Select Feature",
        [
            "🤖 AI Chat",
            "🎪 Event Planner",
            "📚 Exam Preparation",
            "💼 Placement Prep"
        ]
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.messages = []

        try:
            st.query_params.clear()
        except Exception:
            pass

        st.rerun()


# ============================================================
# AI CHAT
# ============================================================

if app_mode == "🤖 AI Chat":

    st.title("🤖 Tech Mithra AI")

    st.caption(
        "Ask any question and get a fast answer."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Ask Question",
            "🖼️ Upload Photo",
            "📸 Camera"
        ]
    )

    question = ""
    selected_image = None

    with tab1:

        question = st.text_input(
            "Ask anything",
            placeholder="Example: What is an Electric Vehicle?"
        )

    with tab2:

        uploaded_file = st.file_uploader(
            "Upload Image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:

            selected_image = Image.open(
                uploaded_file
            )

            st.image(
                selected_image,
                width=350
            )

            question = st.text_input(
                "Ask about this image",
                key="upload_question"
            )

    with tab3:

        camera_file = st.camera_input(
            "Take a Photo"
        )

        if camera_file:

            selected_image = Image.open(
                camera_file
            )

            st.image(
                selected_image,
                width=350
            )

            question = st.text_input(
                "Ask about this photo",
                key="camera_question"
            )

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    if st.button(
        "🚀 Get Answer",
        use_container_width=True
    ):

        if question.strip():

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):

                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner(
                    "Thinking..."
                ):

                    answer = get_answer(
                        question,
                        selected_image
                    )

                    st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        else:

            st.warning(
                "Please enter a question."
            )

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.title("🎪 Event Planner")

    event_name = st.text_input(
        "Event Name",
        placeholder="Example: PLC Workshop"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Technical Workshop",
            "Seminar",
            "Guest Lecture",
            "Hackathon",
            "College Fest",
            "Cultural Event",
            "Project Exhibition"
        ]
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="Example: Engineering Students"
    )

    col1, col2 = st.columns(2)

    with col1:

        generate_plan = st.button(
            "📋 Generate Event Plan",
            use_container_width=True
        )

    with col2:

        generate_prompt = st.button(
            "🎨 Generate Image Prompt",
            use_container_width=True
        )

    if generate_plan:

        if event_name.strip():

            with st.spinner(
                "Creating event plan..."
            ):

                result = generate_event_plan(
                    event_name,
                    event_type,
                    audience
                )

            st.markdown(result)

        else:

            st.warning(
                "Please enter an event name."
            )

    if generate_prompt:

        if event_name.strip():

            with st.spinner(
                "Creating image prompt..."
            ):

                result = generate_image_prompt(
                    event_name,
                    event_type,
                    audience
                )

            st.code(result)

        else:

            st.warning(
                "Please enter an event name."
            )


# ============================================================
# EXAM PREPARATION
# ============================================================

elif app_mode == "📚 Exam Preparation":

    st.title("📚 Exam Preparation")

    subject = st.text_input(
        "Subject Name"
    )

    topic = st.text_input(
        "Topic"
    )

    answer_type = st.selectbox(
        "Answer Type",
        [
            "2 Marks Answer",
            "5 Marks Answer",
            "10 Marks Answer",
            "Detailed Explanation"
        ]
    )

    if st.button(
        "📝 Generate Answer",
        use_container_width=True
    ):

        if subject.strip() and topic.strip():

            prompt = f"""
Subject: {subject}
Topic: {topic}
Required Answer: {answer_type}
"""

            instruction = """
You are an expert exam assistant.

Prepare an accurate and exam-ready answer.

For short answers be concise.
For long answers use headings and important points.
"""

            with st.spinner(
                "Preparing answer..."
            ):

                result = ask_ai(
                    prompt,
                    instruction
                )

            if not result:

                result = local_answer(topic)

            st.markdown(result)

        else:

            st.warning(
                "Enter subject and topic."
            )


# ============================================================
# PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.title("💼 Placement Preparation")

    role = st.text_input(
        "Target Job Role / Technology",
        placeholder="Example: Electrical Engineer"
    )

    if st.button(
        "🎯 Generate Placement Guide",
        use_container_width=True
    ):

        if role.strip():

            prompt = f"""
Target Role: {role}
"""

            instruction = """
You are an expert placement mentor.

Give:
1. Required skills
2. Important topics
3. Technical interview questions
4. HR questions
5. Preparation roadmap

Keep it practical and easy to understand.
"""

            with st.spinner(
                "Preparing guide..."
            ):

                result = ask_ai(
                    prompt,
                    instruction
                )

            if not result:

                result = f"""
# 🎯 Placement Guide: {role}

## Required Skills
- Technical fundamentals
- Communication
- Problem solving
- Teamwork

## Interview Questions
1. Tell me about yourself.
2. Explain your project.
3. What are your strengths?
4. Why should we hire you?

## Preparation
Practice technical concepts and interview questions regularly.
"""

            st.markdown(result)

        else:

            st.warning(
                "Please enter a job role."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
<center>
<b>🚀 Tech Mithra AI Pro</b><br>
Ask Anything | Fast AI Answers | Event Planner |
Exam Preparation | Placement Prep
</center>
""",
    unsafe_allow_html=True
)
