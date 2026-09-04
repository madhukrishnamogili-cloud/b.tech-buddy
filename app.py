import streamlit as st
import os
import base64
from google import genai
from google.genai import types
from PIL import Image


# ============================================================
# TECH MITHRA AI PRO - COMPLETE STREAMLIT APP
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

TEXT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]

IMAGE_MODELS = [
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image"
]


# ============================================================
# GET SECRETS SAFELY
# ============================================================

def get_secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.getenv(name, default)


GEMINI_API_KEY = get_secret("GEMINI_API_KEY", "")
APP_PASSWORD = get_secret("APP_PASSWORD", "")


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

if "last_generated_prompt" not in st.session_state:
    st.session_state.last_generated_prompt = ""


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_client():
    if not GEMINI_API_KEY:
        return None

    try:
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        return None


# ============================================================
# GENERATE TEXT WITH AUTOMATIC MODEL FALLBACK
# ============================================================

def generate_ai_text(question, system_instruction="You are a helpful AI assistant."):
    client = get_client()

    if client is None:
        return (
            "❌ **Gemini API Key is not configured.**\n\n"
            "Add your API key in Streamlit Secrets:\n\n"
            "`GEMINI_API_KEY = \"YOUR_API_KEY\"`"
        )

    last_error = ""

    for model_name in TEXT_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )

            if response and response.text:
                return response.text

        except Exception as e:
            last_error = str(e)

    return (
        "❌ **AI Error**\n\n"
        f"Could not generate a response.\n\n"
        f"Details: `{last_error}`\n\n"
        "Please check:\n"
        "- Your Gemini API key\n"
        "- Streamlit Secrets\n"
        "- API quota\n"
        "- Internet connection"
    )


# ============================================================
# IMAGE ANALYSIS
# ============================================================

def analyze_image(question, image):
    client = get_client()

    if client is None:
        return "❌ Gemini API key is not configured."

    last_error = ""

    for model_name in TEXT_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    question,
                    image
                ],
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are an expert academic and technical assistant. "
                        "Analyze the uploaded image carefully and answer the user's "
                        "question accurately. If it contains an exam question, "
                        "provide the correct answer with a clear explanation."
                    )
                )
            )

            if response and response.text:
                return response.text

        except Exception as e:
            last_error = str(e)

    return f"❌ Image analysis failed: {last_error}"


# ============================================================
# GENERATE IMAGE
# ============================================================

def generate_image(prompt, aspect_ratio="1:1"):
    client = get_client()

    if client is None:
        return None, "❌ Gemini API key is not configured."

    last_error = ""

    for model_name in IMAGE_MODELS:
        try:
            interaction = client.interactions.create(
                model=model_name,
                input=prompt,
                response_format={
                    "type": "image",
                    "mime_type": "image/png",
                    "aspect_ratio": aspect_ratio,
                    "image_size": "1K"
                }
            )

            if interaction.output_image and interaction.output_image.data:
                image_bytes = base64.b64decode(
                    interaction.output_image.data
                )
                return image_bytes, ""

        except Exception as e:
            last_error = str(e)

    return None, f"❌ Image generation failed: {last_error}"


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("🔐 Tech Mithra AI Pro Login")

    st.write(
        "Login once and continue using all AI features during your session."
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email_input = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email"
        )

        password_input = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if not email_input or not password_input:

                st.error(
                    "Please enter both email and password."
                )

            elif APP_PASSWORD and password_input != APP_PASSWORD:

                st.error("Incorrect password.")

            else:

                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.rerun()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI Pro")

    st.success(
        f"Logged in as:\n\n{st.session_state.user_email}"
    )

    st.divider()

    education_stream = st.selectbox(
        "📚 Select Stream",
        [
            "Engineering (B.Tech / EEE / CSE)",
            "Pharmacy (B.Pharm / Pharm.D)",
            "Nursing (B.Sc / GNM)",
            "MBA (Management)",
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

    st.caption("AI Model System")

    st.write("Text AI:")
    st.code(TEXT_MODELS[0])

    st.write("Image AI:")
    st.code(IMAGE_MODELS[0])

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
# STREAM NAME
# ============================================================

stream_name = education_stream


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.title("🤖 Project & Lab Guide")

    st.write(
        "Ask any academic, technical, engineering or general question."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Text Chat",
            "🖼️ Upload Photo",
            "📸 Camera Photo"
        ]
    )


    # ========================================================
    # TEXT CHAT
    # ========================================================

    with tab1:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

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

            academic_instruction = f"""
You are Tech Mithra AI Pro, an intelligent academic and technical assistant.

The student belongs to:
{stream_name}

Answer the question accurately.

Rules:
1. First give a direct answer or definition.
2. Explain in simple English.
3. Use headings and bullet points.
4. For academic questions, provide exam-friendly answers.
5. For engineering questions, explain working principles and applications.
6. For programming questions, provide correct code when appropriate.
7. For long-answer questions, give detailed explanations.
8. Do not invent facts.
"""

            with st.chat_message("assistant"):

                with st.spinner(
                    "🤖 Tech Mithra AI is thinking..."
                ):

                    answer = generate_ai_text(
                        prompt,
                        academic_instruction
                    )

                    st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


    # ========================================================
    # UPLOAD PHOTO
    # ========================================================

    with tab2:

        st.subheader("🖼️ Upload Question or Lab Image")

        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

            image_question = st.text_input(
                "Ask a question about this image",
                placeholder="Example: Give the correct answer to this question"
            )

            if st.button(
                "🤖 Analyze Uploaded Image",
                key="analyze_upload"
            ):

                question = image_question

                if not question:
                    question = (
                        "Analyze this image and provide the correct "
                        "answer with a detailed explanation."
                    )

                with st.spinner(
                    "🤖 Analyzing image..."
                ):

                    result = analyze_image(
                        question,
                        image
                    )

                    st.markdown(result)


    # ========================================================
    # CAMERA PHOTO
    # ========================================================

    with tab3:

        st.subheader("📸 Take a Photo")

        camera_photo = st.camera_input(
            "Take a photo of your question"
        )

        if camera_photo:

            camera_image = Image.open(
                camera_photo
            )

            st.image(
                camera_image,
                caption="Captured Image",
                use_container_width=True
            )

            camera_question = st.text_input(
                "Ask about the camera image",
                placeholder="Example: Solve this question"
            )

            if st.button(
                "🤖 Analyze Camera Image",
                key="analyze_camera"
            ):

                question = camera_question

                if not question:
                    question = (
                        "Read the question in this image and "
                        "provide the correct answer with explanation."
                    )

                with st.spinner(
                    "🤖 AI is analyzing..."
                ):

                    result = analyze_image(
                        question,
                        camera_image
                    )

                    st.markdown(result)


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.title("🎪 AI Event & Workshop Planner")

    st.write(
        "Generate event plans, schedules, posters and AI image prompts."
    )

    event_name = st.text_input(
        "🎯 Event Name / Topic",
        placeholder="Example: PLC Workshop 2026"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Technical Workshop",
            "College Event",
            "Seminar",
            "Guest Lecture",
            "Hackathon",
            "Cultural Event",
            "Project Exhibition",
            "Other"
        ]
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="Example: B.Tech EEE Students"
    )

    col1, col2 = st.columns(2)


    # ========================================================
    # EVENT PLAN
    # ========================================================

    with col1:

        if st.button(
            "📋 Generate Complete Event Plan",
            use_container_width=True
        ):

            if not event_name:

                st.warning(
                    "Please enter an event name."
                )

            else:

                prompt = f"""
Create a complete professional event plan.

Event Name: {event_name}
Event Type: {event_type}
Target Audience: {audience}
Education Stream: {stream_name}

Include:

1. Event introduction
2. Event objectives
3. Required resources
4. Organizing committee
5. Detailed schedule
6. Registration plan
7. Venue setup
8. Technical requirements
9. Budget categories
10. Promotion strategy
11. Certificates
12. Safety and management plan
13. Expected outcomes

Use professional headings and bullet points.
"""

                with st.spinner(
                    "🎪 Creating event plan..."
                ):

                    answer = generate_ai_text(
                        prompt,
                        "You are an expert college event planner."
                    )

                    st.markdown(answer)


    # ========================================================
    # IMAGE PROMPT
    # ========================================================

    with col2:

        if st.button(
            "🖼️ Generate Poster Image Prompt",
            use_container_width=True
        ):

            if not event_name:

                st.warning(
                    "Please enter an event name."
                )

            else:

                prompt_request = f"""
Create a highly detailed AI image generation prompt for a professional college event poster.

Event Name: {event_name}
Event Type: {event_type}
Audience: {audience}

The prompt should include:
- Professional modern college design
- Event-related visual elements
- Space for event title
- Space for date and venue
- Cinematic lighting
- High quality
- Social media poster style
"""

                with st.spinner(
                    "✍️ Generating image prompt..."
                ):

                    generated_prompt = generate_ai_text(
                        prompt_request,
                        "You are an expert AI image prompt engineer."
                    )

                    st.session_state.last_generated_prompt = (
                        generated_prompt
                    )

                    st.markdown(
                        "### 🎨 Generated Image Prompt"
                    )

                    st.code(
                        generated_prompt
                    )


    # ========================================================
    # TEXT TO IMAGE
    # ========================================================

    st.divider()

    st.subheader("🎨 Text to Image Generator")

    default_prompt = (
        st.session_state.last_generated_prompt
        if st.session_state.last_generated_prompt
        else ""
    )

    image_prompt = st.text_area(
        "Enter Image Prompt",
        value=default_prompt,
        height=180,
        placeholder=(
            "Example: A professional college technical "
            "workshop poster, futuristic technology theme..."
        )
    )

    aspect_ratio = st.selectbox(
        "Image Aspect Ratio",
        [
            "1:1",
            "16:9",
            "9:16"
        ]
    )

    if st.button(
        "✨ Generate AI Image",
        use_container_width=True
    ):

        if not image_prompt:

            st.warning(
                "Please enter an image prompt."
            )

        else:

            with st.spinner(
                "🎨 Generating AI image..."
            ):

                image_bytes, error = generate_image(
                    image_prompt,
                    aspect_ratio
                )

                if image_bytes:

                    st.image(
                        image_bytes,
                        caption="Generated by Tech Mithra AI",
                        use_container_width=True
                    )

                    st.download_button(
                        "⬇️ Download Image",
                        data=image_bytes,
                        file_name="tech_mithra_ai_image.png",
                        mime="image/png"
                    )

                else:

                    st.error(error)


# ============================================================
# EXAM PREPARATION
# ============================================================

elif app_mode == "📚 Exam Preparation":

    st.title("📚 AI Exam Preparation")

    st.write(
        "Generate important questions, answers and revision notes."
    )

    subject_name = st.text_input(
        "📖 Enter Subject Name",
        placeholder="Example: Electrical Machines"
    )

    exam_topic = st.text_input(
        "🎯 Enter Chapter / Topic (Optional)",
        placeholder="Example: Transformers"
    )

    exam_type = st.selectbox(
        "Select Preparation Type",
        [
            "Important Questions",
            "Short Answers",
            "5 Marks Answers",
            "10 Marks Answers",
            "Long Answers",
            "Last Minute Revision Notes"
        ]
    )

    if st.button(
        "📝 Generate Exam Preparation",
        use_container_width=True
    ):

        if not subject_name:

            st.warning(
                "Please enter the subject name."
            )

        else:

            prompt = f"""
Create exam preparation material.

Education Stream:
{stream_name}

Subject:
{subject_name}

Topic:
{exam_topic}

Preparation Type:
{exam_type}

Make the content accurate and exam-friendly.

Use:
- Clear headings
- Important definitions
- Bullet points
- Simple explanations
- Relevant examples
- Key points for revision
"""

            with st.spinner(
                "📚 Preparing exam material..."
            ):

                answer = generate_ai_text(
                    prompt,
                    "You are an expert academic tutor."
                )

                st.markdown(answer)


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif app_mode == "💼 Placement Preparation":

    st.title("💼 AI Placement & Career Preparation")

    st.write(
        "Prepare for technical interviews, HR interviews and placements."
    )

    company_name = st.text_input(
        "🏢 Target Company (Optional)",
        placeholder="Example: TCS, Infosys, Kia"
    )

    job_role = st.text_input(
        "🎯 Target Job Role",
        placeholder="Example: Electrical Engineer"
    )

    preparation_type = st.selectbox(
        "Preparation Type",
        [
            "Technical Interview Questions",
            "HR Interview Questions",
            "Aptitude Preparation",
            "Resume Preparation",
            "Project Explanation",
            "Complete Placement Roadmap"
        ]
    )

    if st.button(
        "🚀 Generate Placement Guide",
        use_container_width=True
    ):

        if not job_role:

            st.warning(
                "Please enter your target job role."
            )

        else:

            prompt = f"""
Create a professional placement preparation guide.

Student Stream:
{stream_name}

Target Company:
{company_name}

Target Job Role:
{job_role}

Preparation Type:
{preparation_type}

Include relevant:
- Interview questions
- Model answers
- Technical concepts
- HR questions
- Project discussion tips
- Skills to learn
- Preparation roadmap

Make it clear and suitable for students.
"""

            with st.spinner(
                "💼 Preparing placement guide..."
            ):

                answer = generate_ai_text(
                    prompt,
                    "You are an expert placement trainer and career mentor."
                )

                st.markdown(answer)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <h3>🚀 Tech Mithra AI Pro</h3>
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
