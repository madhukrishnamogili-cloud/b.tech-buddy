import streamlit as st
from google import genai
from PIL import Image
import time

# ============================================================
# TECH MITHRA AI PRO - COMPLETE SINGLE FILE APP
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "Tech Mithra AI Pro 🎓"
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "logged_in": False,
    "user_email": "",
    "messages": [],
    "event_result": "",
    "image_prompt_result": "",
    "exam_result": "",
    "placement_result": "",
    "last_model": "None"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GEMINI API KEY
# Add in Streamlit Secrets:
# GEMINI_API_KEY = "your_api_key_here"
# ============================================================

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        return key.strip()
    except Exception:
        return ""


# ============================================================
# GEMINI CLIENT
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
# AI MODELS WITH FALLBACK
# ============================================================

MODEL_LIST = [
    "gemini-3.6-flash",
]


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def ask_ai(question, instruction, image=None):

    client = get_client()

    if client is None:
        return """
### ❌ Gemini API Key Not Configured

Please add your API key in Streamlit Secrets.

Example:

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
"""

    last_error = ""

    for model in MODEL_LIST:

        for attempt in range(2):

            try:

                if image is not None:

                    contents = [
                        instruction,
                        f"User Question: {question}",
                        image
                    ]

                else:

                    contents = f"""
{instruction}

User Question:
{question}
"""

                response = client.models.generate_content(
                    model=model,
                    contents=contents
                )

                if hasattr(response, "text"):

                    if response.text:

                        st.session_state.last_model = model

                        return response.text

            except Exception as e:

                last_error = str(e)

                if attempt == 0:
                    time.sleep(1)

    return f"""
### ❌ AI Service Error

The AI could not answer right now.

Error:

{last_error}

Please check your API key, internet connection,
API quota, and Gemini model availability.
"""


# ============================================================
# LOGIN CREDENTIALS
# Optional Streamlit Secrets:
# APP_EMAIL = "your@email.com"
# APP_PASSWORD = "yourpassword"
# ============================================================

def get_login_credentials():

    try:

        email = st.secrets.get(
            "APP_EMAIL",
            ""
        )

        password = st.secrets.get(
            "APP_PASSWORD",
            ""
        )

        return email.strip(), password.strip()

    except Exception:

        return "", ""


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div style="text-align:center; padding-top:50px;">
            <h1>🚀 Tech Mithra AI Pro</h1>
            <h3>🔐 Student Login</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        email = st.text_input(
            "📧 Email Address"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            correct_email, correct_password = (
                get_login_credentials()
            )

            # Secure configured login
            if correct_email and correct_password:

                if (
                    email.strip().lower()
                    == correct_email.lower()
                    and password == correct_password
                ):

                    st.session_state.logged_in = True
                    st.session_state.user_email = email.strip()

                    st.success(
                        "✅ Login Successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid Email or Password."
                    )

            # Development fallback login
            else:

                if email.strip() and password.strip():

                    st.session_state.logged_in = True
                    st.session_state.user_email = email.strip()

                    st.success(
                        "✅ Login Successful!"
                    )

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

    try:

        st.image(
            LOGO_URL,
            width=100
        )

    except Exception:

        st.write("🚀")

    st.title(APP_NAME)

    st.caption(
        f"👤 Logged in: {st.session_state.user_email}"
    )

    st.divider()

    st.subheader("🧠 AI Brain")

    ai_mode = st.selectbox(
        "Select AI Mode",
        [
            "🚀 Auto AI",
            "⚡ Fast AI"
        ]
    )

    st.divider()

    education_stream = st.selectbox(
        "📚 Select Stream",
        [
            "⚡ Engineering (B.Tech / EEE / CSE)",
            "💊 Pharmacy (B.Pharm / Pharm.D)",
            "🩺 Nursing (B.Sc / GNM)",
            "📈 MBA (Management)"
        ]
    )

    st.divider()

    app_mode = st.radio(
        "🚀 Select Feature",
        [
            "🤖 Project & Lab Guide",
            "🎪 Event Planner",
            "📚 Exam Hacker",
            "💼 Placement Prep"
        ]
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.messages = []
        st.rerun()


# ============================================================
# MAIN APP HEADER
# ============================================================

st.title("🚀 Tech Mithra AI Pro")

st.caption(
    f"📚 Stream: {education_stream}"
)

st.caption(
    f"🧠 AI Mode: {ai_mode}"
)


# ============================================================
# PROJECT AND LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        "🤖 Project & Lab Guide"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Ask AI",
            "🖼️ Upload Photo",
            "📸 Camera"
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

        question = st.chat_input(
            "Ask any question..."
        )

        if question:

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
                    "🧠 AI is thinking..."
                ):

                    instruction = f"""
You are Tech Mithra AI Pro,
an intelligent educational AI assistant.

Student Stream:
{education_stream}

Follow these rules:

1. Understand the exact question.
2. Give the direct answer first.
3. Answer accurately.
4. Use simple language.
5. Telugu question -> Telugu answer.
6. English question -> English answer.
7. For technical questions explain:
   - Definition
   - Working principle
   - Important points
   - Applications
8. For exam questions give exam-friendly answers.
9. Do not provide unrelated information.
"""

                    answer = ask_ai(
                        question,
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
    # IMAGE UPLOAD
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "🖼️ Upload Question / Notes / Diagram"
        )

        uploaded_file = st.file_uploader(
            "Upload Image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

        if uploaded_file:

            try:

                uploaded_image = Image.open(
                    uploaded_file
                )

                st.image(
                    uploaded_image,
                    caption="Uploaded Image",
                    use_container_width=True
                )

                image_question = st.text_input(
                    "Ask about this image"
                )

                if st.button(
                    "🤖 Analyze Image",
                    use_container_width=True
                ):

                    if not image_question.strip():

                        image_question = """
Read the image carefully.
If it contains questions, answer them.
If it contains answers, check whether
they are right or wrong.
"""

                    with st.spinner(
                        "🧠 Analyzing image..."
                    ):

                        instruction = f"""
You are an educational
image-analysis AI assistant.

Student Stream:
{education_stream}

Analyze the uploaded image carefully.

If it contains:

- Questions: give correct answers.
- Student answers: check right or wrong.
- Circuit diagrams: explain components and working.
- Technical diagrams: explain clearly.
- Notes: explain and summarize.

Do not invent text that is not visible.
"""

                        answer = ask_ai(
                            image_question,
                            instruction,
                            uploaded_image
                        )

                        st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Image Error: {e}"
                )

    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "📸 Take Question Photo"
        )

        camera_photo = st.camera_input(
            "Take a Photo"
        )

        if camera_photo:

            try:

                camera_image = Image.open(
                    camera_photo
                )

                st.image(
                    camera_image,
                    caption="Captured Image",
                    use_container_width=True
                )

                camera_question = st.text_input(
                    "Ask about this photo",
                    key="camera_question"
                )

                if st.button(
                    "🤖 Analyze Photo",
                    use_container_width=True
                ):

                    if not camera_question.strip():

                        camera_question = """
Read the question in this image
and give the correct answer.
"""

                    with st.spinner(
                        "🧠 Reading image..."
                    ):

                        instruction = f"""
You are an expert academic assistant.

Student Stream:
{education_stream}

Analyze the image carefully.

Read visible questions accurately.

Give correct exam-friendly answers.

If multiple questions are present,
answer them one by one.
"""

                        answer = ask_ai(
                            camera_question,
                            instruction,
                            camera_image
                        )

                        st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Camera Error: {e}"
                )


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 Event & Workshop Planner"
    )

    event_name = st.text_input(
        "🎯 Event Name",
        placeholder="Example: PLC Workshop 2026"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Technical Workshop",
            "Seminar",
            "Hackathon",
            "Project Expo",
            "Guest Lecture",
            "College Fest",
            "Cultural Event",
            "Sports Event"
        ]
    )

    audience = st.text_input(
        "👥 Target Audience"
    )

    location = st.text_input(
        "📍 Event Location"
    )

    if st.button(
        "📋 Generate Event Plan",
        use_container_width=True
    ):

        if event_name.strip():

            event_question = f"""
Event Name: {event_name}

Event Type: {event_type}

Target Audience: {audience}

Location: {location}
"""

            event_instruction = """
You are a professional college event planner.

Create a complete event plan.

Include:

1. Event Overview
2. Objectives
3. Target Audience
4. Venue Requirements
5. Equipment Required
6. Organizing Team
7. Team Responsibilities
8. Complete Event Schedule
9. Budget Categories
10. Promotion Plan
11. Registration Plan
12. Event-Day Checklist
13. Safety Guidelines
14. Expected Outcome
"""

            with st.spinner(
                "🧠 Creating Event Plan..."
            ):

                st.session_state.event_result = ask_ai(
                    event_question,
                    event_instruction
                )

        else:

            st.warning(
                "Please enter Event Name."
            )

    if st.session_state.event_result:

        st.subheader(
            "📋 Generated Event Plan"
        )

        st.markdown(
            st.session_state.event_result
        )

    st.divider()

    st.subheader(
        "🎨 AI Event Image Prompt Generator"
    )

    image_style = st.selectbox(
        "Image Style",
        [
            "Realistic Photography",
            "Cinematic",
            "Professional College Event",
            "Modern Poster",
            "Futuristic",
            "Social Media Banner"
        ]
    )

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        [
            "1:1 Instagram Post",
            "4:5 Instagram Portrait",
            "9:16 Instagram Story",
            "16:9 YouTube Thumbnail"
        ]
    )

    if st.button(
        "✨ Generate Image Prompt",
        use_container_width=True
    ):

        if event_name.strip():

            prompt_question = f"""
Event Name: {event_name}

Event Type: {event_type}

Target Audience: {audience}

Location: {location}

Image Style: {image_style}

Aspect Ratio: {aspect_ratio}
"""

            prompt_instruction = """
You are an expert AI image prompt engineer.

Create a detailed text-to-image prompt.

Include:

- Main event subject
- Students and participants
- Venue environment
- Stage setup
- Decorations
- Lighting
- Camera angle
- Composition
- Professional realistic details
- High quality

Return only the final
image-generation prompt.
"""

            with st.spinner(
                "🎨 Generating Image Prompt..."
            ):

                st.session_state.image_prompt_result = ask_ai(
                    prompt_question,
                    prompt_instruction
                )

        else:

            st.warning(
                "Please enter Event Name first."
            )

    if st.session_state.image_prompt_result:

        st.text_area(
            "🎨 Generated AI Image Prompt",
            value=st.session_state.image_prompt_result,
            height=300
        )


# ============================================================
# EXAM HACKER
# ============================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 Exam Hacker"
    )

    subject_or_question = st.text_input(
        "📖 Enter Subject / Question",
        placeholder="Example: What is an Electric Vehicle?"
    )

    answer_type = st.selectbox(
        "Select Answer Type",
        [
            "Direct Answer",
            "2 Marks Answer",
            "5 Marks Answer",
            "10 Marks Answer",
            "Long Answer",
            "Important Questions",
            "Revision Notes",
            "MCQs"
        ]
    )

    if st.button(
        "📝 Generate Exam Answer",
        use_container_width=True
    ):

        if subject_or_question.strip():

            exam_instruction = f"""
You are an expert university exam assistant.

Student Stream:
{education_stream}

Required Answer Type:
{answer_type}

Rules:

1. Answer the exact question.
2. Give technically correct information.
3. Use simple language.
4. Use headings and bullet points.
5. Make the answer suitable for exams.
6. For long answers provide
   detailed explanation.
7. Telugu question -> Telugu answer.
8. English question -> English answer.
"""

            with st.spinner(
                "🧠 Preparing Answer..."
            ):

                st.session_state.exam_result = ask_ai(
                    subject_or_question,
                    exam_instruction
                )

        else:

            st.warning(
                "Please enter a question."
            )

    if st.session_state.exam_result:

        st.subheader(
            "📝 AI Exam Answer"
        )

        st.markdown(
            st.session_state.exam_result
        )


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 Placement & Career Preparation"
    )

    job_role = st.text_input(
        "🎯 Target Job Role",
        placeholder="Example: Electrical Engineer"
    )

    company_name = st.text_input(
        "🏢 Target Company (Optional)",
        placeholder="Example: Kia India"
    )

    experience_level = st.selectbox(
        "Experience Level",
        [
            "Fresher",
            "Final Year Student",
            "Internship Candidate"
        ]
    )

    if st.button(
        "💼 Generate Placement Guide",
        use_container_width=True
    ):

        if job_role.strip():

            placement_question = f"""
Target Job Role:
{job_role}

Target Company:
{company_name}

Experience Level:
{experience_level}

Student Stream:
{education_stream}
"""

            placement_instruction = """
You are an expert placement
and career mentor.

Create a complete placement
preparation guide.

Include:

1. Job Role Overview
2. Required Technical Skills
3. Required Soft Skills
4. Important Technical Topics
5. Technical Interview Questions
6. Sample Answers
7. HR Interview Questions
8. Self Introduction Example
9. Resume Tips
10. Project Explanation Tips
11. Interview Tips
12. 7-Day Preparation Plan
"""

            with st.spinner(
                "🧠 Preparing Placement Guide..."
            ):

                st.session_state.placement_result = ask_ai(
                    placement_question,
                    placement_instruction
                )

        else:

            st.warning(
                "Please enter Target Job Role."
            )

    if st.session_state.placement_result:

        st.subheader(
            "🎯 Placement Preparation Guide"
        )

        st.markdown(
            st.session_state.placement_result
        )


# ============================================================
# SYSTEM STATUS
# ============================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    if get_api_key():

        st.success(
            "🟢 Gemini API Connected"
        )

    else:

        st.warning(
            "🟡 API Key Not Configured"
        )

with col2:

    st.info(
        f"🧠 AI Mode: {ai_mode}"
    )

with col3:

    st.info(
        f"🤖 Model: {st.session_state.last_model}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h3>🚀 Tech Mithra AI Pro</h3>
        <p>🧠 Smart AI Academic Assistant</p>
        <p>
            🤖 Project & Lab Guide |
            🖼️ Image Analysis |
            🎪 Event Planner |
            📚 Exam Hacker |
            💼 Placement Prep
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
