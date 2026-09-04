import streamlit as st
import os
import base64
from google import genai
from PIL import Image


# ============================================================
# TECH MITHRA AI PRO - COMPLETE APP
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "🚀 Tech Mithra AI Pro"

# ONLY NEW MODELS - NO gemini-2.5-flash
TEXT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]

IMAGE_MODEL = "gemini-3.1-flash-image"


# ============================================================
# GET API KEY
# ============================================================

def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY", "")


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

def get_client():
    api_key = get_api_key()

    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# ============================================================
# GENERATE TEXT WITH MODEL FALLBACK
# ============================================================

def ask_ai(question, instruction="You are a helpful AI assistant."):

    client = get_client()

    if client is None:
        return (
            "❌ API Key not found.\n\n"
            "Add GEMINI_API_KEY in Streamlit Secrets."
        )

    errors = []

    full_prompt = f"""
{instruction}

User Question:
{question}
"""

    for model_name in TEXT_MODELS:

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )

            if response and response.text:
                return response.text

        except Exception as e:
            errors.append(
                f"{model_name}: {str(e)}"
            )

    return (
        "❌ AI service is temporarily unavailable.\n\n"
        "Models tried:\n"
        + "\n".join(errors)
    )


# ============================================================
# ANALYZE IMAGE
# ============================================================

def analyze_image(question, image):

    client = get_client()

    if client is None:
        return "❌ API Key not found."

    errors = []

    for model_name in TEXT_MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=[
                    question,
                    image
                ]
            )

            if response and response.text:
                return response.text

        except Exception as e:
            errors.append(
                f"{model_name}: {str(e)}"
            )

    return (
        "❌ Image analysis failed.\n\n"
        + "\n".join(errors)
    )


# ============================================================
# GENERATE IMAGE
# ============================================================

def generate_ai_image(prompt):

    client = get_client()

    if client is None:
        return None, "API Key not found."

    try:

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt
        )

        for part in response.parts:

            if part.inline_data is not None:

                image_data = part.inline_data.data

                if isinstance(image_data, str):
                    image_data = base64.b64decode(
                        image_data
                    )

                return image_data, None

            try:
                image = part.as_image()

                if image is not None:

                    from io import BytesIO

                    buffer = BytesIO()

                    image.save(
                        buffer,
                        format="PNG"
                    )

                    return (
                        buffer.getvalue(),
                        None
                    )

            except Exception:
                pass

        return None, "No image was returned."

    except Exception as e:

        return None, str(e)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "app_name" not in st.session_state:
    st.session_state.app_name = APP_NAME


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("🔐 Tech Mithra AI Pro")

    st.subheader("Login")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        email = st.text_input(
            "📧 Email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if email and password:

                st.session_state.logged_in = True
                st.session_state.user_email = email

                st.rerun()

            else:

                st.error(
                    "Enter Email and Password."
                )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI Pro")

    st.success(
        f"Logged in as:\n\n"
        f"{st.session_state.user_email}"
    )

    st.divider()

    education_stream = st.selectbox(
        "📚 Select Stream",
        [
            "Engineering",
            "Pharmacy",
            "Nursing",
            "MBA",
            "General Learning"
        ]
    )

    st.divider()

    app_mode = st.radio(
        "Select Feature",
        [
            "🤖 Project & Lab Guide",
            "🎪 Event Planner",
            "📚 Exam Preparation",
            "💼 Placement Preparation"
        ]
    )

    st.divider()

    st.caption("Active AI Models")

    st.code("Text: gemini-3.8-flash")

    st.code(
        "Image: gemini-3.1-flash-image"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.messages = []

        st.rerun()


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.title("🤖 Project & Lab Guide")

    st.write(
        "Ask any academic, technical or general question."
    )

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

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        prompt = st.chat_input(
            "Ask any question..."
        )

        if prompt:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):

                st.markdown(prompt)

            instruction = f"""
You are Tech Mithra AI Pro.

You are an expert academic and technical AI assistant.

Student Stream:
{education_stream}

Rules:

1. Answer accurately.
2. Start with a direct definition.
3. Use simple English.
4. Use headings.
5. Use bullet points when useful.
6. Give exam-friendly answers.
7. Explain technical concepts clearly.
8. For programming questions provide correct code.
"""

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "🤖 AI is thinking..."
                ):

                    answer = ask_ai(
                        prompt,
                        instruction
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

        st.subheader(
            "🖼️ Upload Question Image"
        )

        uploaded_file = st.file_uploader(
            "Upload Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        if uploaded_file:

            image = Image.open(
                uploaded_file
            )

            st.image(
                image,
                use_container_width=True
            )

            question = st.text_input(
                "Question about this image",
                placeholder=(
                    "Example: Give the correct answer"
                )
            )

            if st.button(
                "🤖 Analyze Image"
            ):

                if not question:

                    question = """
Analyze this image carefully.
Read any question present in the image.
Give the correct answer with explanation.
"""

                with st.spinner(
                    "Analyzing image..."
                ):

                    result = analyze_image(
                        question,
                        image
                    )

                    st.markdown(result)


    # --------------------------------------------------------
    # CAMERA PHOTO
    # --------------------------------------------------------

    with tab3:

        camera_photo = st.camera_input(
            "Take a photo"
        )

        if camera_photo:

            image = Image.open(
                camera_photo
            )

            st.image(
                image,
                use_container_width=True
            )

            question = st.text_input(
                "Ask about this photo",
                placeholder="Solve this question"
            )

            if st.button(
                "🤖 Analyze Camera Photo"
            ):

                if not question:

                    question = """
Read the question from this image.
Give the correct answer.
Explain clearly.
"""

                with st.spinner(
                    "AI is analyzing..."
                ):

                    result = analyze_image(
                        question,
                        image
                    )

                    st.markdown(result)


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.title(
        "🎪 AI Event Planner"
    )

    event_name = st.text_input(
        "Event Name"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Technical Workshop",
            "Seminar",
            "Hackathon",
            "College Event",
            "Project Exhibition",
            "Cultural Event"
        ]
    )

    audience = st.text_input(
        "Target Audience"
    )


    # --------------------------------------------------------
    # EVENT PLAN
    # --------------------------------------------------------

    if st.button(
        "📋 Generate Event Plan"
    ):

        if not event_name:

            st.warning(
                "Enter Event Name."
            )

        else:

            prompt = f"""
Create a complete professional event plan.

Event Name: {event_name}

Event Type: {event_type}

Audience: {audience}

Include:

1. Introduction
2. Objectives
3. Event schedule
4. Required resources
5. Organizing team
6. Venue arrangement
7. Promotion plan
8. Registration
9. Certificates
10. Expected outcomes
"""

            with st.spinner(
                "Creating event plan..."
            ):

                result = ask_ai(
                    prompt,
                    "You are an expert college event planner."
                )

                st.markdown(result)


    st.divider()


    # --------------------------------------------------------
    # IMAGE PROMPT
    # --------------------------------------------------------

    st.subheader(
        "🎨 AI Poster Prompt Generator"
    )

    if st.button(
        "✍️ Generate Poster Prompt"
    ):

        if not event_name:

            st.warning(
                "Enter Event Name."
            )

        else:

            prompt = f"""
Create a detailed AI image generation prompt.

Event Name: {event_name}

Event Type: {event_type}

Audience: {audience}

Create a professional,
modern,
cinematic college event poster.

Leave clean space for:

Event Title
Date
Time
Venue

Use high-quality design.
"""

            with st.spinner(
                "Creating prompt..."
            ):

                result = ask_ai(
                    prompt,
                    "You are an expert AI image prompt engineer."
                )

                st.code(result)


    st.divider()


    # --------------------------------------------------------
    # TEXT TO IMAGE
    # --------------------------------------------------------

    st.subheader(
        "🖼️ Text to Image"
    )

    image_prompt = st.text_area(
        "Enter Image Prompt",
        height=150,
        placeholder=(
            "Example: Professional futuristic "
            "college technical workshop poster"
        )
    )

    if st.button(
        "✨ Generate Image",
        use_container_width=True
    ):

        if not image_prompt:

            st.warning(
                "Enter an image prompt."
            )

        else:

            with st.spinner(
                "Generating AI image..."
            ):

                image_bytes, error = (
                    generate_ai_image(
                        image_prompt
                    )
                )

                if image_bytes:

                    st.image(
                        image_bytes,
                        use_container_width=True
                    )

                    st.download_button(
                        "⬇️ Download Image",
                        data=image_bytes,
                        file_name=(
                            "tech_mithra_image.png"
                        ),
                        mime="image/png"
                    )

                else:

                    st.error(
                        f"Image Error: {error}"
                    )


# ============================================================
# EXAM PREPARATION
# ============================================================

elif app_mode == "📚 Exam Preparation":

    st.title(
        "📚 AI Exam Preparation"
    )

    subject = st.text_input(
        "Subject Name"
    )

    topic = st.text_input(
        "Topic / Chapter"
    )

    answer_type = st.selectbox(
        "Select Type",
        [
            "Important Questions",
            "Short Answers",
            "5 Marks Answers",
            "10 Marks Answers",
            "Long Answers",
            "Revision Notes"
        ]
    )

    if st.button(
        "📝 Generate"
    ):

        if not subject:

            st.warning(
                "Enter Subject Name."
            )

        else:

            prompt = f"""
Create exam preparation material.

Stream:
{education_stream}

Subject:
{subject}

Topic:
{topic}

Type:
{answer_type}

Make the answer accurate,
easy to understand,
and exam-friendly.
"""

            with st.spinner(
                "Preparing..."
            ):

                result = ask_ai(
                    prompt,
                    "You are an expert academic tutor."
                )

                st.markdown(result)


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif app_mode == "💼 Placement Preparation":

    st.title(
        "💼 AI Placement Preparation"
    )

    company = st.text_input(
        "Target Company"
    )

    role = st.text_input(
        "Target Job Role"
    )

    preparation = st.selectbox(
        "Preparation Type",
        [
            "Technical Interview",
            "HR Interview",
            "Aptitude",
            "Resume",
            "Project Explanation",
            "Complete Placement Roadmap"
        ]
    )

    if st.button(
        "🚀 Generate Placement Guide"
    ):

        if not role:

            st.warning(
                "Enter Job Role."
            )

        else:

            prompt = f"""
Create a placement preparation guide.

Student Stream:
{education_stream}

Target Company:
{company}

Job Role:
{role}

Preparation Type:
{preparation}

Include relevant questions,
answers,
important skills,
and a preparation roadmap.
"""

            with st.spinner(
                "Preparing placement guide..."
            ):

                result = ask_ai(
                    prompt,
                    "You are an expert career mentor."
                )

                st.markdown(result)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <h2>🚀 Tech Mithra AI Pro</h2>
        <p>
        AI Academic Assistant |
        Project Guide |
        Event Planner |
        Exam Preparation |
        Placement Preparation
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
