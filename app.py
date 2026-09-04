import io
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types


# ============================================================
# TECH MITHRA AI PRO - COMPLETE APP
# NO LOGIN SYSTEM
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "🚀 Tech Mithra AI Pro"

TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""


@st.cache_resource
def get_client(api_key):
    if not api_key:
        return None

    return genai.Client(api_key=api_key)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# AI RESPONSE FUNCTION
# ============================================================

def get_ai_response(question, mode="general", image=None):

    api_key = get_api_key()

    if not api_key:
        return "❌ Gemini API Key not found. Add GEMINI_API_KEY in Streamlit Secrets."

    try:
        client = get_client(api_key)
    except Exception:
        return "❌ Unable to connect to Gemini AI."

    if not question or not question.strip():
        return "Please enter a question."

    question = question.strip()

    if mode == "project":

        instruction = f"""
You are Tech Mithra AI Pro, a helpful AI assistant.

Answer the following question accurately and clearly:

{question}

Rules:
- Answer directly.
- Use simple English.
- Keep small questions short.
- For academic questions, give clear explanations.
- If the user asks for 2 marks, give a short exam answer.
- If the user asks for 5 marks, give a medium detailed answer.
- If the user asks for 10 marks or long answer, explain in detail.
- Use headings and bullet points when useful.
"""

    elif mode == "exam":

        instruction = f"""
You are an expert college exam preparation AI.

Answer:

{question}

Rules:
- Give an accurate academic answer.
- Use simple English.
- Start with a definition when appropriate.
- Make the answer suitable for writing in exams.
- Use headings and bullet points.
"""

    elif mode == "placement":

        instruction = f"""
You are an expert placement preparation AI.

User request:

{question}

Give:
- Practical answers
- Interview-focused preparation
- Simple English
- Important technical or HR questions when useful
- Professional guidance
"""

    elif mode == "event":

        instruction = f"""
You are a professional college event planner.

Create a detailed event plan based on:

{question}

Include:
1. Event Name
2. Objective
3. Event Overview
4. Target Audience
5. Schedule
6. Required Resources
7. Team Responsibilities
8. Budget Suggestions
9. Promotion Plan
10. Registration Plan
11. Certificates
12. Feedback
13. Conclusion

Use simple and practical English.
"""

    else:

        instruction = f"""
You are Tech Mithra AI Pro.

Answer this question accurately:

{question}

Use simple English and answer directly.
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
                max_output_tokens=1500
            )
        )

        if response and response.text:
            return response.text.strip()

        return "⚠️ AI could not generate an answer. Please try again."

    except Exception as e:

        error_text = str(e).lower()

        if "429" in error_text:
            return "⚠️ Too many requests. Please wait a moment and try again."

        if "api" in error_text and "key" in error_text:
            return "❌ Invalid Gemini API Key."

        if "404" in error_text:
            return "❌ AI model not available. Check the model name."

        if "503" in error_text:
            return "⚠️ AI server is busy. Please try again."

        return f"⚠️ Error: {str(e)}"


# ============================================================
# IMAGE PROMPT GENERATOR
# ============================================================

def generate_image_prompt(event_name, event_type, audience):

    return f"""
Create a professional, realistic and attractive college event promotional poster.

Event Name: {event_name}

Event Type: {event_type}

Target Audience: {audience}

Requirements:
- Modern design
- Professional appearance
- Attractive composition
- Technology and education atmosphere
- High quality
- Social media poster style
- Cinematic lighting
- Clean composition
- Space for event title and information
"""


# ============================================================
# TEXT TO IMAGE
# ============================================================

def generate_event_image(prompt):

    api_key = get_api_key()

    if not api_key:
        return None, "❌ Gemini API Key is missing."

    try:

        client = get_client(api_key)

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt
        )

        if response and response.candidates:

            for candidate in response.candidates:

                if candidate.content and candidate.content.parts:

                    for part in candidate.content.parts:

                        if (
                            hasattr(part, "inline_data")
                            and part.inline_data
                        ):

                            image_bytes = part.inline_data.data

                            generated_image = Image.open(
                                io.BytesIO(image_bytes)
                            )

                            return generated_image, None

        return None, "⚠️ Image could not be generated."

    except Exception as e:

        error_text = str(e).lower()

        if "429" in error_text:
            return None, "⚠️ Image generation limit reached."

        if "404" in error_text:
            return None, "⚠️ Image model is not available for this API."

        return None, f"⚠️ Image generation error: {str(e)}"


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

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title(APP_NAME)

st.caption(
    "AI Academic Assistant | Projects | Events | Exams | Placements"
)

st.divider()


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header("🤖 Project & Lab Guide")

    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Ask AI",
            "🖼️ Upload Photo",
            "📸 Camera"
        ]
    )


    # TEXT CHAT
    with tab1:

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


    # IMAGE UPLOAD
    with tab2:

        uploaded_photo = st.file_uploader(
            "Upload Question Paper, Diagram, Circuit or Image",
            type=["jpg", "jpeg", "png"]
        )

        photo_question = st.text_input(
            "Ask a question about this image"
        )

        if uploaded_photo:

            image = Image.open(uploaded_photo)

            st.image(
                image,
                use_container_width=True
            )

            if st.button(
                "🤖 Analyze Image",
                key="analyze_upload"
            ):

                if photo_question:
                    question = photo_question
                else:
                    question = (
                        "Analyze this image and explain it clearly."
                    )

                with st.spinner("Analyzing..."):

                    answer = get_ai_response(
                        question,
                        mode="project",
                        image=image
                    )

                st.markdown("### 🤖 AI Answer")
                st.markdown(answer)


    # CAMERA
    with tab3:

        camera_photo = st.camera_input(
            "Take a Photo"
        )

        camera_question = st.text_input(
            "Ask a question",
            key="camera_question"
        )

        if camera_photo:

            image = Image.open(camera_photo)

            st.image(
                image,
                use_container_width=True
            )

            if st.button(
                "🤖 Analyze Camera Photo"
            ):

                if camera_question:
                    question = camera_question
                else:
                    question = "Analyze this image."

                with st.spinner("Analyzing..."):

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
            "Sports Event"
        ]
    )

    target_audience = st.text_input(
        "Target Audience",
        placeholder="Example: Engineering Students"
    )

    col1, col2 = st.columns(2)


    with col1:

        if st.button("📋 Generate Event Plan"):

            if not event_name:

                st.warning("Please enter an Event Name.")

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

                st.markdown("## 📋 Event Plan")
                st.markdown(answer)


    with col2:

        if st.button("📝 Generate Image Prompt"):

            prompt = generate_image_prompt(
                event_name,
                event_type,
                target_audience
            )

            st.markdown("## 🖼️ Image Prompt")

            st.code(prompt)


    st.divider()

    st.subheader("🎨 Text to Image")

    image_prompt = st.text_area(
        "Enter Image Prompt",
        value=generate_image_prompt(
            event_name or "College Event",
            event_type,
            target_audience or "Students"
        ),
        height=180
    )

    if st.button("🎨 Generate Image"):

        with st.spinner("Generating Image..."):

            generated_image, error = generate_event_image(
                image_prompt
            )

        if error:

            st.error(error)

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

    st.header("📚 AI Exam Preparation")

    subject_name = st.text_input(
        "Subject Name"
    )

    topic_name = st.text_input(
        "Topic / Question"
    )

    answer_type = st.selectbox(
        "Answer Type",
        [
            "2 Marks Answer",
            "5 Marks Answer",
            "10 Marks Answer",
            "Long Answer",
            "Important Questions",
            "Short Notes"
        ]
    )

    if st.button("📝 Generate Answer"):

        if not topic_name:

            st.warning(
                "Please enter a Question or Topic."
            )

        else:

            request = f"""
Subject: {subject_name}

Question:
{topic_name}

Required Answer Type:
{answer_type}
"""

            with st.spinner(
                "Preparing Answer..."
            ):

                answer = get_ai_response(
                    request,
                    mode="exam"
                )

            st.markdown("## 📝 Exam Answer")

            st.markdown(answer)


# ============================================================
# PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.header("💼 AI Placement Preparation")

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
        "🎯 Generate Placement Guide"
    ):

        if not role_name:

            st.warning(
                "Please enter Target Job Role."
            )

        else:

            request = f"""
Target Role:
{role_name}

Preparation Type:
{preparation_type}
"""

            with st.spinner(
                "Preparing Placement Guide..."
            ):

                answer = get_ai_response(
                    request,
                    mode="placement"
                )

            st.markdown(
                "## 🎯 Placement Guide"
            )

            st.markdown(answer)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; opacity:0.7;">
        🚀 <b>Tech Mithra AI Pro</b><br>
        AI Academic Assistant | Study | Projects | Events | Placements
    </div>
    """,
    unsafe_allow_html=True
)
