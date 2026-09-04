# ============================================================
# TECH MITHRA AI PRO - COMPLETE STREAMLIT APP
# Save this complete code as: app.py
#
# requirements.txt:
# streamlit
# google-genai
# pillow
#
# Streamlit Secrets:
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
# APP_PASSWORD = "123456"
# ============================================================

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import time


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APP SETTINGS
# ============================================================

APP_NAME = "🚀 Tech Mithra AI Pro"
APP_TAGLINE = "AI Academic Assistant | Project Guide | Event Planner | Exam Preparation | Placement Preparation"

DEFAULT_PASSWORD = "123456"

TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    opacity: 0.75;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    min-height: 45px;
    font-size: 16px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GET API KEY
# ============================================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""


def get_app_password():
    try:
        return st.secrets["APP_PASSWORD"]
    except Exception:
        return DEFAULT_PASSWORD


# ============================================================
# CREATE GEMINI CLIENT
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
# INITIALIZE SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "login_checked" not in st.session_state:
    st.session_state.login_checked = False


# ============================================================
# ONE TIME LOGIN USING QUERY PARAMETER
# ============================================================

if not st.session_state.login_checked:
    try:
        if st.query_params.get("login") == "true":
            saved_email = st.query_params.get("user")

            if saved_email:
                st.session_state.logged_in = True
                st.session_state.user_email = saved_email

        st.session_state.login_checked = True

    except Exception:
        pass



# ============================================================
# AI RESPONSE FUNCTION
# ============================================================

def get_ai_response(question, mode="general", image=None):

    api_key = get_api_key()

    if not api_key:
        return (
            "❌ Gemini API key is not configured.\n\n"
            "Add GEMINI_API_KEY in Streamlit Secrets."
        )

    client = get_client(api_key)

    if client is None:
        return "❌ Unable to initialize the AI service."

    question = question.strip()

    if not question:
        return "Please enter a question."

    # --------------------------------------------------------
    # PROJECT & LAB GUIDE
    # --------------------------------------------------------

    if mode == "project":

        instruction = f"""
You are Tech Mithra AI Pro, a fast and helpful academic AI assistant.

Answer the student's question directly and accurately.

Question:
{question}

Rules:
- Give the answer immediately.
- Use simple English.
- For short questions, give a short answer.
- For academic questions, explain clearly.
- Use headings and bullet points only when useful.
- Do not add unnecessary introductions.
- If asked for 2 marks, give a short answer.
- If asked for 5 marks, give a proper 5-mark answer.
- If asked for a long answer, provide detailed explanation.
- If an image is attached, analyze the image and answer the question.
"""

    # --------------------------------------------------------
    # EXAM HACKER
    # --------------------------------------------------------

    elif mode == "exam":

        instruction = f"""
You are Tech Mithra AI Pro for exam preparation.

Create an accurate academic answer.

Question:
{question}

Rules:
- Use simple English.
- Give direct answers.
- Include important definitions.
- Add key points.
- Use headings where necessary.
- Make answers suitable for college exams.
- Avoid unnecessary long introductions.
"""

    # --------------------------------------------------------
    # PLACEMENT PREPARATION
    # --------------------------------------------------------

    elif mode == "placement":

        instruction = f"""
You are Tech Mithra AI Pro for placement and interview preparation.

Answer this request:

{question}

Rules:
- Give practical interview-focused answers.
- Include important questions and answers if useful.
- Use simple English.
- Keep the answer clear and professional.
- Give direct answers first.
"""

    # --------------------------------------------------------
    # EVENT PLANNER
    # --------------------------------------------------------

    elif mode == "event":

        instruction = f"""
You are Tech Mithra AI Pro Event Planner.

Create a complete and practical event plan.

Request:
{question}

Include:
1. Event objective
2. Event overview
3. Target audience
4. Required resources
5. Team responsibilities
6. Event schedule
7. Budget suggestions
8. Promotion ideas
9. Registration plan
10. Certificates and feedback
11. Closing summary

Use clear and simple English.
Make the answer practical for a college event.
"""

    else:

        instruction = f"""
You are Tech Mithra AI Pro.

Answer this question clearly:

{question}

Rules:
- Give a direct answer first.
- Use simple English.
- Be accurate.
- Keep small answers short.
"""

    try:

        contents = [instruction]

        if image is not None:
            contents.append(image)

        response = client.models.generate_content(

            model=TEXT_MODEL,

            contents=contents,

            config=types.GenerateContentConfig(

                temperature=0.4,

                max_output_tokens=1200,

                thinking_config=types.ThinkingConfig(
                    thinking_budget=0
                )

            )
        )

        if response and response.text:
            return response.text.strip()

        return "⚠️ AI could not generate an answer. Please try again."

    except Exception as e:

        error_text = str(e).lower()

        # ----------------------------------------------------
        # FALLBACK MODEL FOR TEMPORARY SERVER ISSUES
        # ----------------------------------------------------

        try:

            fallback_response = client.models.generate_content(

                model="gemini-3.7-flash",

                contents=[instruction] if image is None else [instruction, image],

                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=1000
                )
            )

            if fallback_response and fallback_response.text:
                return fallback_response.text.strip()

        except Exception:
            pass

        if "api key" in error_text or "api_key" in error_text:
            return (
                "❌ API Key Error.\n\n"
                "Please check GEMINI_API_KEY in Streamlit Secrets."
            )

        if "429" in error_text:
            return (
                "⚠️ Too many requests are being made.\n\n"
                "Please wait a few seconds and try again."
            )

        if "503" in error_text or "unavailable" in error_text:
            return (
                "⚠️ AI service is temporarily busy.\n\n"
                "Please try again in a few seconds."
            )

        if "404" in error_text or "not_found" in error_text:
            return (
                "⚠️ AI model is currently unavailable.\n\n"
                "Please check the installed Google GenAI SDK version."
            )

        return (
            "⚠️ AI service is temporarily unavailable.\n\n"
            "Please try again."
        )


# ============================================================
# IMAGE PROMPT GENERATOR
# ============================================================

def generate_image_prompt(event_name, event_type, audience):

    return f"""
Create a professional and realistic promotional poster for a college event.

Event Name: {event_name}
Event Type: {event_type}
Target Audience: {audience}

Design requirements:
- Modern professional design
- High quality
- College and technology atmosphere
- Attractive composition
- Clean typography space
- Cinematic lighting
- Professional event promotion style
- Suitable for Instagram and social media
- Do not add unnecessary text
"""


# ============================================================
# TEXT TO IMAGE GENERATOR
# ============================================================

def generate_event_image(prompt, aspect_ratio="1:1"):

    api_key = get_api_key()

    if not api_key:
        return None, "❌ GEMINI_API_KEY is not configured."

    client = get_client(api_key)

    if client is None:
        return None, "❌ Unable to initialize AI image service."

    try:

        response = client.models.generate_content(

            model=IMAGE_MODEL,

            contents=prompt,

            config=types.GenerateContentConfig(

                response_format={
                    "image": {
                        "aspect_ratio": aspect_ratio
                    }
                }

            )
        )

        if response and response.candidates:

            for candidate in response.candidates:

                if candidate.content and candidate.content.parts:

                    for part in candidate.content.parts:

                        if hasattr(part, "inline_data") and part.inline_data:

                            image_bytes = part.inline_data.data

                            generated_image = Image.open(
                                io.BytesIO(image_bytes)
                            )

                            return generated_image, None

        return None, "⚠️ Image could not be generated."

    except Exception as e:

        error_text = str(e).lower()

        if "429" in error_text:
            return None, "⚠️ Image generation limit reached. Please try later."

        if "503" in error_text:
            return None, "⚠️ Image AI service is busy. Please try again."

        return None, "⚠️ Image generation is temporarily unavailable."


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(APP_NAME)

    st.caption("Your Personal AI Study Assistant")

    st.divider()

    app_mode = st.radio(

        "Select Feature",

        [
            "🤖 Project & Lab Guide",
            "🎪 Event Planner",
            "📚 Exam Hacker",
            "💼 Placement Prep"
        ]

    )

    st.divider()

    st.write("👤 Logged in as:")
    st.caption(st.session_state.user_email)

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.messages = []
        st.session_state.login_checked = False

        st.query_params.clear()

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    f"<div class='main-title'>{APP_NAME}</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='subtitle'>{APP_TAGLINE}</div>",
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header("🤖 Project & Lab Guide")

    tab1, tab2, tab3 = st.tabs(

        [
            "💬 Text Chat",
            "🖼️ Upload Photo",
            "📸 Camera Photo"
        ]

    )

    # --------------------------------------------------------
    # TEXT CHAT
    # --------------------------------------------------------

    with tab1:

        st.caption(
            "Ask any academic, technical or general question."
        )

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_question = st.chat_input(
            "Ask any question..."
        )

        if user_question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_question
                }
            )

            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    answer = get_ai_response(
                        user_question,
                        mode="project"
                    )

                st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    # --------------------------------------------------------
    # UPLOAD PHOTO
    # --------------------------------------------------------

    with tab2:

        uploaded_photo = st.file_uploader(

            "Upload question paper, diagram, circuit or academic photo",

            type=["jpg", "jpeg", "png"]

        )

        photo_question = st.text_input(
            "Ask a question about this image"
        )

        if uploaded_photo:

            image = Image.open(uploaded_photo)

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

            if st.button(
                "🤖 Analyze Uploaded Image",
                key="upload_analyze"
            ):

                question = photo_question

                if not question:
                    question = (
                        "Analyze this image and explain "
                        "the important information."
                    )

                with st.spinner("Analyzing image..."):

                    answer = get_ai_response(
                        question,
                        mode="project",
                        image=image
                    )

                st.markdown("### 🤖 AI Answer")
                st.markdown(answer)

    # --------------------------------------------------------
    # CAMERA PHOTO
    # --------------------------------------------------------

    with tab3:

        camera_photo = st.camera_input(
            "Take a photo"
        )

        camera_question = st.text_input(
            "Ask a question about camera photo",
            key="camera_question"
        )

        if camera_photo:

            image = Image.open(camera_photo)

            st.image(
                image,
                caption="Camera Image",
                use_container_width=True
            )

            if st.button(
                "🤖 Analyze Camera Photo",
                key="camera_analyze"
            ):

                question = camera_question

                if not question:
                    question = (
                        "Analyze this image and explain "
                        "the important information."
                    )

                with st.spinner("Analyzing image..."):

                    answer = get_ai_response(
                        question,
                        mode="project",
                        image=image
                    )

                st.markdown("### 🤖 AI Answer")
                st.markdown(answer)


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.header("🎪 AI Event & Workshop Planner")

    st.caption(
        "Create complete event plans, promotional prompts and event images."
    )

    event_name = st.text_input(
        "Event Name",
        placeholder="Example: PLC Workshop"
    )

    event_type = st.selectbox(

        "Event Type",

        [
            "Technical Workshop",
            "Seminar",
            "College Fest",
            "Guest Lecture",
            "Hackathon",
            "Project Expo",
            "Cultural Event",
            "Sports Event",
            "Other"
        ]

    )

    target_audience = st.text_input(
        "Target Audience",
        placeholder="Example: Final Year EEE Students"
    )

    st.divider()

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # EVENT PLAN
    # --------------------------------------------------------

    with col1:

        if st.button(
            "📋 Generate Event Plan",
            use_container_width=True
        ):

            if not event_name.strip():

                st.warning(
                    "Please enter an event name."
                )

            else:

                event_request = f"""
Event Name: {event_name}
Event Type: {event_type}
Target Audience: {target_audience}

Create a complete professional college event plan.
"""

                with st.spinner(
                    "Creating event plan..."
                ):

                    event_answer = get_ai_response(
                        event_request,
                        mode="event"
                    )

                st.markdown(
                    "## 📋 Complete Event Plan"
                )

                st.markdown(event_answer)

    # --------------------------------------------------------
    # IMAGE PROMPT
    # --------------------------------------------------------

    with col2:

        if st.button(
            "📝 Generate Photo Prompt",
            use_container_width=True
        ):

            if not event_name.strip():

                st.warning(
                    "Please enter an event name."
                )

            else:

                prompt = generate_image_prompt(
                    event_name,
                    event_type,
                    target_audience
                )

                st.markdown(
                    "## 🖼️ AI Image Prompt"
                )

                st.code(
                    prompt,
                    language=None
                )

    st.divider()

    # --------------------------------------------------------
    # TEXT TO IMAGE
    # --------------------------------------------------------

    st.subheader("🎨 Text to Image")

    image_prompt = st.text_area(

        "Enter Image Prompt",

        value=generate_image_prompt(
            event_name if event_name else "College Technical Event",
            event_type,
            target_audience if target_audience else "College Students"
        ),

        height=180

    )

    aspect_ratio = st.selectbox(

        "Select Image Size",

        [
            "1:1",
            "16:9",
            "9:16"
        ]

    )

    if st.button(
        "🎨 Generate Event Image",
        use_container_width=True
    ):

        if not image_prompt.strip():

            st.warning(
                "Please enter an image prompt."
            )

        else:

            with st.spinner(
                "Generating image..."
            ):

                generated_image, image_error = generate_event_image(
                    image_prompt,
                    aspect_ratio
                )

            if image_error:

                st.error(image_error)

            elif generated_image:

                st.success(
                    "Image generated successfully!"
                )

                st.image(
                    generated_image,
                    use_container_width=True
                )


# ============================================================
# EXAM HACKER
# ============================================================

elif app_mode == "📚 Exam Hacker":

    st.header("📚 AI Exam Preparation")

    subject_name = st.text_input(
        "Subject Name",
        placeholder="Example: Fundamentals of Management"
    )

    topic_name = st.text_input(
        "Topic / Chapter",
        placeholder="Example: Levels of Management"
    )

    answer_type = st.selectbox(

        "Select Type",

        [
            "2 Marks Answer",
            "5 Marks Answer",
            "10 Marks Answer",
            "Long Answer",
            "Important Questions",
            "Short Notes",
            "Last Minute Revision"
        ]

    )

    if st.button(
        "📝 Generate",
        use_container_width=False
    ):

        if not subject_name.strip() or not topic_name.strip():

            st.warning(
                "Please enter subject name and topic."
            )

        else:

            exam_request = f"""
Subject: {subject_name}
Topic: {topic_name}
Required Answer Type: {answer_type}

Generate an exam-ready academic answer.
"""

            with st.spinner(
                "Preparing answer..."
            ):

                exam_answer = get_ai_response(
                    exam_request,
                    mode="exam"
                )

            st.markdown("## 📝 AI Exam Answer")

            st.markdown(exam_answer)


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.header("💼 AI Placement & Career Preparation")

    role_name = st.text_input(
        "Target Job Role / Technology",
        placeholder="Example: Electrical Engineer / Python Developer"
    )

    preparation_type = st.selectbox(

        "Select Preparation",

        [
            "Interview Questions",
            "Technical Questions",
            "HR Questions",
            "Resume Guidance",
            "Career Roadmap",
            "Company Preparation",
            "Mock Interview"
        ]

    )

    if st.button(
        "🎯 Generate Placement Guide",
        use_container_width=True
    ):

        if not role_name.strip():

            st.warning(
                "Please enter a target job role or technology."
            )

        else:

            placement_request = f"""
Target Role / Technology: {role_name}
Preparation Type: {preparation_type}

Create a complete placement preparation guide.
"""

            with st.spinner(
                "Preparing placement guide..."
            ):

                placement_answer = get_ai_response(
                    placement_request,
                    mode="placement"
                )

            st.markdown(
                "## 🎯 Placement Preparation Guide"
            )

            st.markdown(
                placement_answer
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; opacity:0.7;">
    🚀 <b>Tech Mithra AI Pro</b><br>
    AI Academic Assistant • Project Guide • Event Planner • Exam Preparation • Placement Preparation
    </div>
    """,
    unsafe_allow_html=True
)
