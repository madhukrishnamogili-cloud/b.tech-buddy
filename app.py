import io
import time
import streamlit as st
from PIL import Image
from google import genai


# ============================================================
# TECH MITHRA AI PRO - COMPLETE APP
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

# Fast text models with fallback support
TEXT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
]

# Image generation model
IMAGE_MODEL = "gemini-3.1-flash-image"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    background-color: white;
    z-index: 999;
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
        return None


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client(api_key):

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_error" not in st.session_state:
    st.session_state.api_error = ""


# ============================================================
# AI RESPONSE FUNCTION
# ============================================================

def get_ai_response(
    question,
    mode="general",
    image=None
):

    api_key = get_api_key()

    if not api_key:

        return (
            "❌ Gemini API Key not found.\n\n"
            "Please add GEMINI_API_KEY in Streamlit Secrets."
        )

    if not question:

        return "Please enter a question."

    try:

        client = get_client(api_key)

    except Exception as e:

        return (
            "❌ Unable to connect to Gemini API.\n\n"
            f"Error: {str(e)}"
        )


    # ========================================================
    # SYSTEM INSTRUCTIONS
    # ========================================================

    if mode == "project":

        prompt = f"""
You are Tech Mithra AI Pro, an intelligent academic assistant.

User Question:
{question}

Instructions:
- Answer accurately and directly.
- Use simple English.
- For small questions, give a fast and short answer.
- For academic questions, explain clearly.
- For 2 marks questions, give a short answer.
- For 5 marks questions, give a medium detailed answer.
- For 10 marks questions, give a detailed answer.
- Use headings and bullet points when useful.
- Do not give unnecessary information.
"""

    elif mode == "exam":

        prompt = f"""
You are an expert college exam preparation assistant.

Subject and Question:
{question}

Instructions:
- Give an accurate academic answer.
- Use simple English.
- Make the answer suitable for exams.
- Use definition, explanation and examples when needed.
- Follow the requested marks format.
"""

    elif mode == "event":

        prompt = f"""
You are a professional college event and workshop planner.

Create an event plan using the following information:

{question}

Include:

1. Event Name
2. Event Objective
3. Event Description
4. Target Audience
5. Event Schedule
6. Venue Requirements
7. Required Resources
8. Team Responsibilities
9. Budget Suggestions
10. Promotion Plan
11. Registration Process
12. Certificates
13. Feedback Process
14. Conclusion

Use practical and simple English.
"""

    elif mode == "placement":

        prompt = f"""
You are an expert placement and career preparation assistant.

User Request:
{question}

Provide practical and professional guidance.

When useful include:
- Important concepts
- Interview questions
- Sample answers
- Technical preparation
- HR preparation
- Career suggestions

Use simple English.
"""

    else:

        prompt = f"""
You are Tech Mithra AI Pro.

Answer this question accurately:

{question}

Use simple English.
Answer directly.
"""


    # ========================================================
    # TRY MULTIPLE MODELS
    # ========================================================

    errors = []

    for model_name in TEXT_MODELS:

        try:

            contents = []

            if image is not None:

                contents.append(image)
                contents.append(prompt)

            else:

                contents = prompt


            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )


            if response:

                response_text = getattr(
                    response,
                    "text",
                    None
                )

                if response_text:

                    return response_text.strip()


        except Exception as e:

            error_message = str(e)

            errors.append(
                f"{model_name}: {error_message}"
            )

            error_lower = error_message.lower()

            # Invalid model - try next model
            if (
                "404" in error_lower
                or "not found" in error_lower
                or "model" in error_lower
            ):
                continue

            # Server busy - wait and try next model
            if (
                "503" in error_lower
                or "unavailable" in error_lower
            ):
                time.sleep(1)
                continue

            # Rate limit
            if (
                "429" in error_lower
                or "quota" in error_lower
            ):
                return (
                    "⚠️ AI request limit reached. "
                    "Please wait a moment and try again."
                )

            # Invalid API key
            if (
                "api key" in error_lower
                or "invalid key" in error_lower
            ):
                return (
                    "❌ Invalid Gemini API Key. "
                    "Please check Streamlit Secrets."
                )

            continue


    return (
        "⚠️ AI service is temporarily unavailable.\n\n"
        "Please try again after a few seconds."
    )


# ============================================================
# GENERATE EVENT IMAGE PROMPT
# ============================================================

def create_event_image_prompt(
    event_name,
    event_type,
    target_audience
):

    return f"""
Create a professional and realistic promotional poster.

Event Name: {event_name}

Event Type: {event_type}

Target Audience: {target_audience}

Style:
Modern college event poster,
professional design,
technology and education atmosphere,
cinematic lighting,
high quality,
clean composition,
attractive visual design,
space for title and event details,
social media promotional poster,
realistic and premium appearance.
"""


# ============================================================
# TEXT TO IMAGE FUNCTION
# ============================================================

def generate_event_image(prompt):

    api_key = get_api_key()

    if not api_key:

        return (
            None,
            "❌ Gemini API Key not found."
        )

    try:

        client = get_client(api_key)

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt
        )


        if not response:

            return (
                None,
                "⚠️ No image response received."
            )


        candidates = getattr(
            response,
            "candidates",
            None
        )


        if not candidates:

            return (
                None,
                "⚠️ Image could not be generated."
            )


        for candidate in candidates:

            content = getattr(
                candidate,
                "content",
                None
            )

            if not content:
                continue


            parts = getattr(
                content,
                "parts",
                []
            )


            for part in parts:

                inline_data = getattr(
                    part,
                    "inline_data",
                    None
                )


                if inline_data:

                    data = getattr(
                        inline_data,
                        "data",
                        None
                    )

                    if data:

                        generated_image = Image.open(
                            io.BytesIO(data)
                        )

                        return (
                            generated_image,
                            None
                        )


        return (
            None,
            "⚠️ Image generation is currently unavailable."
        )


    except Exception as e:

        error_message = str(e)
        error_lower = error_message.lower()


        if (
            "429" in error_lower
            or "quota" in error_lower
        ):

            return (
                None,
                "⚠️ Image generation limit reached. Please try later."
            )


        if (
            "503" in error_lower
            or "unavailable" in error_lower
        ):

            return (
                None,
                "⚠️ Image server is busy. Please try again later."
            )


        if (
            "404" in error_lower
            or "not found" in error_lower
        ):

            return (
                None,
                "⚠️ Image model is not available for this API."
            )


        return (
            None,
            "⚠️ Image generation failed. Please try again."
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(APP_NAME)

    st.caption(
        "AI Academic & Technical Assistant"
    )

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


    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    api_key = get_api_key()

    if api_key:

        st.success(
            "🟢 AI API Connected"
        )

    else:

        st.warning(
            "🟡 API Key Not Set"
        )


# ============================================================
# MAIN HEADER
# ============================================================

st.title(APP_NAME)

st.caption(
    "AI Assistant | Projects | Labs | Events | Exams | Placements"
)

st.divider()


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        "🤖 Project & Lab Guide"
    )

    st.caption(
        "Ask any academic, technical or general question."
    )


    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Ask AI",
            "🖼️ Upload Photo",
            "📸 Camera"
        ]
    )


    # ========================================================
    # TEXT CHAT
    # ========================================================

    with tab1:

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )


        user_question = st.chat_input(
            "Ask any question..."
        )


        if user_question:

            with st.chat_message(
                "user"
            ):

                st.markdown(
                    user_question
                )


            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_question
                }
            )


            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "Thinking..."
                ):

                    answer = get_ai_response(
                        user_question,
                        mode="project"
                    )


                st.markdown(
                    answer
                )


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

        uploaded_photo = st.file_uploader(
            "Upload Question, Diagram, Circuit or Lab Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )


        photo_question = st.text_input(
            "Ask a question about the uploaded image"
        )


        if uploaded_photo:

            image = Image.open(
                uploaded_photo
            )

            st.image(
                image,
                use_container_width=True
            )


            if st.button(
                "🤖 Analyze Uploaded Image",
                use_container_width=True
            ):

                if photo_question:

                    question = photo_question

                else:

                    question = (
                        "Analyze this image and explain it clearly."
                    )


                with st.spinner(
                    "Analyzing image..."
                ):

                    answer = get_ai_response(
                        question,
                        mode="project",
                        image=image
                    )


                st.subheader(
                    "🤖 AI Answer"
                )

                st.markdown(
                    answer
                )


    # ========================================================
    # CAMERA PHOTO
    # ========================================================

    with tab3:

        camera_photo = st.camera_input(
            "Take a Photo"
        )


        camera_question = st.text_input(
            "Ask a question about the camera photo",
            key="camera_question"
        )


        if camera_photo:

            image = Image.open(
                camera_photo
            )

            st.image(
                image,
                use_container_width=True
            )


            if st.button(
                "🤖 Analyze Camera Photo",
                use_container_width=True
            ):

                if camera_question:

                    question = camera_question

                else:

                    question = (
                        "Analyze this image and explain it clearly."
                    )


                with st.spinner(
                    "Analyzing image..."
                ):

                    answer = get_ai_response(
                        question,
                        mode="project",
                        image=image
                    )


                st.subheader(
                    "🤖 AI Answer"
                )

                st.markdown(
                    answer
                )


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 AI Event & Workshop Planner"
    )

    st.caption(
        "Create event plans, image prompts and promotional images."
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
            "Guest Lecture",
            "Hackathon",
            "Project Expo",
            "College Fest",
            "Cultural Event",
            "Sports Event"
        ]
    )


    target_audience = st.text_input(
        "Target Audience",
        placeholder="Example: Final Year EEE Students"
    )


    col1, col2 = st.columns(2)


    # EVENT PLAN
    with col1:

        if st.button(
            "📋 Generate Event Plan",
            use_container_width=True
        ):

            if not event_name.strip():

                st.warning(
                    "Please enter Event Name."
                )

            else:

                request = f"""
Event Name: {event_name}

Event Type: {event_type}

Target Audience: {target_audience}
"""


                with st.spinner(
                    "Creating Event Plan..."
                ):

                    answer = get_ai_response(
                        request,
                        mode="event"
                    )


                st.subheader(
                    "📋 Generated Event Plan"
                )

                st.markdown(
                    answer
                )


    # IMAGE PROMPT
    with col2:

        if st.button(
            "📝 Generate Image Prompt",
            use_container_width=True
        ):

            generated_prompt = (
                create_event_image_prompt(
                    event_name or "College Event",
                    event_type,
                    target_audience or "College Students"
                )
            )


            st.subheader(
                "🖼️ Event Image Prompt"
            )

            st.code(
                generated_prompt,
                language=None
            )


    st.divider()


    # ========================================================
    # TEXT TO IMAGE
    # ========================================================

    st.subheader(
        "🎨 Event Text to Image"
    )


    default_prompt = (
        create_event_image_prompt(
            event_name or "College Event",
            event_type,
            target_audience or "Students"
        )
    )


    image_prompt = st.text_area(
        "Image Prompt",
        value=default_prompt,
        height=220
    )


    if st.button(
        "🎨 Generate Event Image",
        use_container_width=True
    ):

        with st.spinner(
            "Generating image..."
        ):

            generated_image, error = (
                generate_event_image(
                    image_prompt
                )
            )


        if error:

            st.error(
                error
            )

        else:

            st.success(
                "Image Generated Successfully!"
            )

            st.image(
                generated_image,
                use_container_width=True
            )


# ============================================================
# EXAM HACKER
# ============================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 AI Exam Preparation"
    )


    subject_name = st.text_input(
        "Subject Name",
        placeholder="Example: Fundamentals of Management"
    )


    topic_name = st.text_input(
        "Topic / Chapter / Question",
        placeholder="Example: Levels of Management"
    )


    answer_type = st.selectbox(
        "Select Answer Type",
        [
            "2 Marks Answer",
            "5 Marks Answer",
            "10 Marks Answer",
            "Long Answer",
            "Short Notes",
            "Important Questions"
        ]
    )


    if st.button(
        "📝 Generate Answer",
        use_container_width=True
    ):

        if not topic_name.strip():

            st.warning(
                "Please enter a Topic or Question."
            )

        else:

            request = f"""
Subject Name:
{subject_name}

Topic / Question:
{topic_name}

Required Answer Type:
{answer_type}

Give the answer according to the required marks.
"""


            with st.spinner(
                "Preparing Answer..."
            ):

                answer = get_ai_response(
                    request,
                    mode="exam"
                )


            st.subheader(
                "📝 Generated Answer"
            )

            st.markdown(
                answer
            )


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 AI Placement Preparation"
    )


    role_name = st.text_input(
        "Target Job Role / Technology",
        placeholder="Example: Electrical Engineer"
    )


    preparation_type = st.selectbox(
        "Preparation Type",
        [
            "Interview Questions",
            "Technical Questions",
            "HR Questions",
            "Resume Guidance",
            "Career Roadmap",
            "Mock Interview"
        ]
    )


    if st.button(
        "🎯 Generate Placement Guide",
        use_container_width=True
    ):

        if not role_name.strip():

            st.warning(
                "Please enter your Target Job Role."
            )

        else:

            request = f"""
Target Job Role:
{role_name}

Preparation Type:
{preparation_type}
"""


            with st.spinner(
                "Preparing your Placement Guide..."
            ):

                answer = get_ai_response(
                    request,
                    mode="placement"
                )


            st.subheader(
                "🎯 Placement Guide"
            )

            st.markdown(
                answer
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
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
