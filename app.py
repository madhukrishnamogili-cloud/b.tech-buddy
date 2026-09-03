import streamlit as st
from google import genai
from PIL import Image


# ============================================================
# TECH MITHRA AI PRO - COMPLETE STREAMLIT APPLICATION
# ============================================================


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# APP SETTINGS
# ============================================================

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

DEFAULT_APP_NAME = "Tech Mithra AI Pro 🎓"

DEFAULT_LOGO = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

defaults = {
    "app_name": DEFAULT_APP_NAME,
    "app_logo": DEFAULT_LOGO,
    "logged_in": False,
    "user_email": "",
    "messages": [],
    "event_result": "",
    "event_image_prompt": "",
    "exam_result": "",
    "placement_result": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GET GEMINI API KEY
# ============================================================

def get_api_key():

    try:

        api_key = st.secrets.get(
            "GEMINI_API_KEY",
            ""
        )

        if api_key:
            return api_key.strip()

    except Exception:
        pass

    return ""


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

def get_gemini_client():

    api_key = get_api_key()

    if not api_key:
        return None, "API_KEY_NOT_FOUND"

    try:

        client = genai.Client(
            api_key=api_key
        )

        return client, None

    except Exception as e:

        return None, str(e)


# ============================================================
# ERROR HANDLER
# ============================================================

def format_error(error):

    error_text = str(error)
    error_lower = error_text.lower()

    if error == "API_KEY_NOT_FOUND":

        return """
❌ **Gemini API Key Not Found**

Please add your Gemini API key in Streamlit Secrets.

Example:

GEMINI_API_KEY = "YOUR_API_KEY"
"""

    if (
        "401" in error_lower
        or "403" in error_lower
        or "api key" in error_lower
        or "unauthenticated" in error_lower
    ):

        return """
❌ **Invalid API Key**

Please check your Gemini API key.
"""

    if (
        "429" in error_lower
        or "quota" in error_lower
        or "resource exhausted" in error_lower
    ):

        return """
⚠️ **API Limit Reached**

Please wait and try again later.
"""

    return f"""
❌ **AI Error**

{error_text}
"""


# ============================================================
# MAIN AI RESPONSE FUNCTION
# ============================================================

def ask_ai(question, instruction, image=None):

    client, error = get_gemini_client()

    if error:
        return format_error(error)

    try:

        if image is not None:

            contents = [
                instruction,
                question,
                image
            ]

        else:

            contents = f"""
{instruction}

USER QUESTION:

{question}

Give the best accurate answer.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        if response.text:
            return response.text

        return "⚠️ AI could not generate an answer. Please try again."

    except Exception as e:

        return format_error(e)


# ============================================================
# ONE TIME LOGIN USING QUERY PARAMETER
# ============================================================

if "user" in st.query_params:

    saved_user = st.query_params.get(
        "user",
        ""
    )

    if saved_user:

        st.session_state.logged_in = True

        st.session_state.user_email = saved_user


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        f"""
        <h1 style="text-align:center;">
        🔐 Login to {st.session_state.app_name}
        </h1>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        email_input = st.text_input(
            "📧 Email Address"
        )

        password_input = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if (
                email_input.strip()
                and password_input.strip()
            ):

                st.session_state.logged_in = True

                st.session_state.user_email = (
                    email_input.strip()
                )

                st.query_params["user"] = (
                    email_input.strip()
                )

                st.success(
                    "Login Successful!"
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
            st.session_state.app_logo,
            width=100
        )

    except Exception:

        st.write("🚀")


    st.title(
        st.session_state.app_name
    )


    st.caption(
        f"👤 {st.session_state.user_email}"
    )


    # ========================================================
    # ADMIN SETTINGS
    # ========================================================

    if (
        st.session_state.user_email.lower()
        == ADMIN_EMAIL.lower()
    ):

        with st.expander(
            "⚙️ Admin Settings"
        ):

            new_name = st.text_input(
                "App Name",
                st.session_state.app_name
            )

            new_logo = st.text_input(
                "Logo URL",
                st.session_state.app_logo
            )

            if st.button(
                "💾 Save Settings"
            ):

                st.session_state.app_name = new_name

                st.session_state.app_logo = new_logo

                st.success(
                    "Settings Saved!"
                )

                st.rerun()


    st.divider()


    # ========================================================
    # EDUCATION STREAM
    # ========================================================

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


    # ========================================================
    # APP FEATURES
    # ========================================================

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


    # ========================================================
    # CLEAR CHAT
    # ========================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user_email = ""

        st.session_state.messages = []

        st.query_params.clear()

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    f"🚀 {st.session_state.app_name}"
)

st.caption(
    f"📚 Selected Stream: {education_stream}"
)


# ============================================================
# FEATURE 1 - PROJECT AND LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        "🤖 Project & Lab Guide"
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

                st.markdown(
                    prompt
                )


            with st.chat_message("assistant"):

                with st.spinner(
                    "🤖 AI is thinking..."
                ):

                    instruction = f"""
You are Tech Mithra AI Pro.

You are a helpful educational and technical AI assistant.

Student Stream:

{education_stream}

Rules:

1. Answer the exact question.
2. Give a direct answer first.
3. Use simple and clear English.
4. If the user asks in Telugu, answer in Telugu.
5. Use headings and bullet points.
6. For technical questions explain working.
7. For exam questions give exam-friendly answers.
8. Give accurate information.
"""

                    answer = ask_ai(
                        prompt,
                        instruction
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
    # IMAGE UPLOAD
    # ========================================================

    with tab2:

        st.subheader(
            "🖼️ Upload Question / Diagram / Notes"
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

            uploaded_image = Image.open(
                uploaded_file
            )


            st.image(
                uploaded_image,
                caption="Uploaded Image",
                use_container_width=True
            )


            image_question = st.text_input(
                "Ask a question about this image"
            )


            if st.button(
                "🤖 Analyze Uploaded Image",
                use_container_width=True
            ):

                if image_question:

                    with st.spinner(
                        "Analyzing image..."
                    ):

                        instruction = f"""
You are an educational AI assistant.

Student Stream:

{education_stream}

Analyze the uploaded image carefully.

If it contains:

- Exam questions, answer correctly.
- Circuit diagrams, explain working.
- Technical diagrams, explain components.
- Notes, explain the topic.
- Lab experiments, explain procedure and working.

Use simple and clear language.
"""

                        answer = ask_ai(
                            image_question,
                            instruction,
                            uploaded_image
                        )


                        st.markdown(
                            answer
                        )

                else:

                    st.warning(
                        "Please enter a question."
                    )


    # ========================================================
    # CAMERA PHOTO
    # ========================================================

    with tab3:

        camera_photo = st.camera_input(
            "Take a Photo"
        )


        if camera_photo:

            camera_image = Image.open(
                camera_photo
            )


            st.image(
                camera_image,
                caption="Camera Photo",
                use_container_width=True
            )


            camera_question = st.text_input(
                "Ask about this photo"
            )


            if st.button(
                "🤖 Analyze Camera Photo",
                use_container_width=True
            ):

                if camera_question:

                    with st.spinner(
                        "Analyzing photo..."
                    ):

                        instruction = f"""
You are an expert academic assistant.

Student Stream:

{education_stream}

Analyze the image carefully.

If it contains an exam question:

1. Read the question carefully.
2. Give the correct answer.
3. Explain the answer.
4. Use an exam-friendly format.
"""

                        answer = ask_ai(
                            camera_question,
                            instruction,
                            camera_image
                        )


                        st.markdown(
                            answer
                        )

                else:

                    st.warning(
                        "Please enter a question."
                    )


# ============================================================
# FEATURE 2 - EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 Event & Workshop Planner"
    )


    event_name = st.text_input(
        "🎯 Event Name"
    )


    event_type = st.selectbox(

        "Event Type",

        [
            "Technical Workshop",
            "Seminar",
            "College Fest",
            "Hackathon",
            "Project Expo",
            "Guest Lecture",
            "Cultural Event",
            "Sports Event"
        ]

    )


    event_audience = st.text_input(
        "👥 Target Audience"
    )


    # ========================================================
    # GENERATE EVENT PLAN
    # ========================================================

    if st.button(
        "📋 Generate Event Plan",
        use_container_width=True
    ):

        if event_name:

            with st.spinner(
                "Creating event plan..."
            ):

                question = f"""
Event Name:

{event_name}

Event Type:

{event_type}

Target Audience:

{event_audience}
"""

                instruction = """
You are a professional event planner.

Create a complete event plan including:

1. Event Overview
2. Objectives
3. Target Audience
4. Venue Requirements
5. Equipment Required
6. Team Responsibilities
7. Complete Event Schedule
8. Budget Categories
9. Promotion Plan
10. Registration Plan
11. Event Day Checklist
12. Expected Outcome
"""

                result = ask_ai(
                    question,
                    instruction
                )


                st.session_state.event_result = result

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


    # ========================================================
    # EVENT IMAGE PROMPT GENERATOR
    # ========================================================

    st.divider()


    st.subheader(
        "✍️ Event Image Prompt Generator"
    )


    image_style = st.selectbox(

        "Image Style",

        [
            "Realistic",
            "Cinematic",
            "Professional College Event",
            "Modern Poster",
            "Futuristic"
        ]

    )


    if st.button(
        "✨ Generate Image Prompt",
        use_container_width=True
    ):

        if event_name:

            question = f"""
Create an AI image prompt.

Event Name:

{event_name}

Event Type:

{event_type}

Target Audience:

{event_audience}

Image Style:

{image_style}
"""

            instruction = """
You are an expert AI image prompt writer.

Create one detailed professional AI image generation prompt.

Include:

- College environment
- Students
- Event activity
- Stage setup
- Decorations
- Professional lighting
- High quality
- Realistic details

Return only the final image prompt.
"""

            result = ask_ai(
                question,
                instruction
            )


            st.session_state.event_image_prompt = result

        else:

            st.warning(
                "Please enter Event Name first."
            )


    if st.session_state.event_image_prompt:

        st.text_area(

            "🎨 Generated Image Prompt",

            value=st.session_state.event_image_prompt,

            height=250

        )


# ============================================================
# FEATURE 3 - EXAM HACKER
# ============================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 Exam Preparation"
    )


    subject_name = st.text_input(
        "Enter Subject / Topic"
    )


    exam_type = st.selectbox(

        "Preparation Type",

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
        "📝 Generate Exam Material",
        use_container_width=True
    ):

        if subject_name:

            with st.spinner(
                "Preparing exam material..."
            ):

                instruction = f"""
You are an expert university exam preparation assistant.

Student Stream:

{education_stream}

Preparation Type:

{exam_type}

Generate accurate and useful exam material.

Use:

- Clear headings
- Important points
- Simple English
- Exam-friendly format
- Correct technical explanations
"""

                result = ask_ai(
                    subject_name,
                    instruction
                )


                st.session_state.exam_result = result

        else:

            st.warning(
                "Please enter Subject Name."
            )


    if st.session_state.exam_result:

        st.subheader(
            "📝 Exam Material"
        )


        st.markdown(
            st.session_state.exam_result
        )


# ============================================================
# FEATURE 4 - PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 Placement & Career Preparation"
    )


    role_name = st.text_input(
        "🎯 Target Job Role"
    )


    company_name = st.text_input(
        "🏢 Target Company (Optional)"
    )


    if st.button(
        "💼 Generate Placement Guide",
        use_container_width=True
    ):

        if role_name:

            with st.spinner(
                "Preparing placement guide..."
            ):

                question = f"""
Target Job Role:

{role_name}

Target Company:

{company_name}

Student Stream:

{education_stream}
"""

                instruction = """
You are an expert placement mentor.

Create a complete placement preparation guide.

Include:

1. Job Role Overview
2. Required Skills
3. Important Technical Topics
4. Technical Interview Questions
5. Sample Technical Answers
6. HR Interview Questions
7. Self Introduction Sample
8. Resume Tips
9. Project Explanation Tips
10. 7-Day Preparation Plan
"""

                result = ask_ai(
                    question,
                    instruction
                )


                st.session_state.placement_result = result

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
