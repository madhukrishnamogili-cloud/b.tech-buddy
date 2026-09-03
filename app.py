import streamlit as st
from google import genai
from PIL import Image
import base64
import io


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

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

DEFAULT_APP_NAME = "Tech Mithra AI Pro 🎓"

DEFAULT_LOGO = (
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
)


# ============================================================
# SESSION STATE
# ============================================================

if "app_name" not in st.session_state:
    st.session_state.app_name = DEFAULT_APP_NAME

if "app_logo" not in st.session_state:
    st.session_state.app_logo = DEFAULT_LOGO

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "event_result" not in st.session_state:
    st.session_state.event_result = ""

if "exam_result" not in st.session_state:
    st.session_state.exam_result = ""

if "placement_result" not in st.session_state:
    st.session_state.placement_result = ""


# ============================================================
# GET GEMINI API KEY
# ============================================================

def get_api_key():

    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return None


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

def get_client():

    api_key = get_api_key()

    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
        return client

    except Exception:
        return None


# ============================================================
# TEXT AI FUNCTION
# ============================================================

def ask_ai(question, system_instruction="", image=None):

    client = get_client()

    if client is None:

        return (
            "❌ Gemini API Key not found.\n\n"
            "Please add GEMINI_API_KEY in Streamlit Secrets."
        )

    try:

        if image is not None:

            contents = [
                system_instruction,
                question,
                image
            ]

        else:

            contents = f"""
{system_instruction}

User Question:

{question}
"""

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=contents
        )

        if response.text:
            return response.text

        return "AI could not generate an answer. Please try again."

    except Exception as e:

        return f"""
❌ AI Error

{str(e)}
"""


# ============================================================
# IMAGE GENERATION FUNCTION
# ============================================================

def generate_image(prompt):

    client = get_client()

    if client is None:
        return None, "❌ Gemini API Key not found."

    try:

        interaction = client.interactions.create(
            model="gemini-3.1-flash-image",
            input=prompt
        )

        output_image = interaction.output_image

        if output_image is None:
            return None, "❌ Image was not generated."

        image_bytes = base64.b64decode(
            output_image.data
        )

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        return image, None

    except Exception as e:

        return None, str(e)


# ============================================================
# LOGIN SYSTEM
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

    col1, col2, col3 = st.columns([1, 2, 1])

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

            if email_input and password_input:

                st.session_state.logged_in = True
                st.session_state.user_email = email_input

                st.success("Login Successful!")

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

        st.write("🎓")

    st.title(
        st.session_state.app_name
    )

    st.caption(
        f"Logged in as: {st.session_state.user_email}"
    )

    # --------------------------------------------------------
    # ADMIN SETTINGS
    # --------------------------------------------------------

    if (
        st.session_state.user_email
        == ADMIN_EMAIL
    ):

        with st.expander(
            "⚙️ Admin Settings"
        ):

            new_name = st.text_input(
                "App Name",
                value=st.session_state.app_name
            )

            new_logo = st.text_input(
                "Logo URL",
                value=st.session_state.app_logo
            )

            if st.button(
                "💾 Save Settings"
            ):

                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo

                st.success(
                    "Settings Updated!"
                )

                st.rerun()

    st.divider()


    # --------------------------------------------------------
    # EDUCATION STREAM
    # --------------------------------------------------------

    education_stream = st.selectbox(

        "📚 Select Stream",

        [

            "Engineering (B.Tech / EEE / CSE)",

            "Pharmacy (B.Pharm / Pharm.D)",

            "Nursing (B.Sc / GNM)",

            "MBA (Management)"

        ]

    )

    st.divider()


    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Chat"
    ):

        st.session_state.messages = []

        st.rerun()


    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "🚪 Logout"
    ):

        st.session_state.logged_in = False

        st.session_state.user_email = ""

        st.session_state.messages = []

        st.rerun()


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.title(
        "🤖 Project & Lab Guide"
    )

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

        st.subheader(
            "💬 Ask Your Question"
        )

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


            with st.chat_message("assistant"):

                with st.spinner(
                    "AI is thinking..."
                ):

                    instruction = f"""
You are Tech Mithra AI.

You are a helpful AI assistant for students.

Student Stream:
{education_stream}

Answer the question clearly and accurately.

Rules:

1. Give a direct answer first.

2. Explain in simple English.

3. Use headings.

4. Use bullet points when useful.

5. For academic questions, provide exam-friendly answers.

6. Explain technical concepts step by step.

7. Give examples when useful.

8. Do not generate unrelated information.
"""

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
            "🖼️ Upload Photo and Ask Question"
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
                caption="Uploaded Image",
                use_container_width=True
            )


            image_question = st.text_input(

                "Ask a question about this image",

                placeholder=(
                    "Example: Explain this diagram"
                )

            )


            if st.button(
                "🤖 Analyze Uploaded Image"
            ):

                if image_question:

                    with st.spinner(
                        "Analyzing image..."
                    ):

                        instruction = f"""
You are an academic and technical AI assistant.

Student Stream:
{education_stream}

Analyze the uploaded image carefully.

Answer the user's question accurately.

If the image contains:

- Circuit diagram: explain components and working.
- Exam question: answer it.
- Notes: explain the topic.
- Technical diagram: explain each part.
- Lab experiment: explain procedure and working.

Use simple English.
"""

                        answer = ask_ai(

                            image_question,

                            instruction,

                            image

                        )

                        st.success(
                            "Analysis Completed"
                        )

                        st.markdown(answer)

                else:

                    st.warning(
                        "Please enter a question."
                    )


    # --------------------------------------------------------
    # CAMERA PHOTO
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "📸 Take Photo and Ask Question"
        )

        camera_photo = st.camera_input(
            "Take a Photo"
        )


        if camera_photo:

            camera_image = Image.open(
                camera_photo
            )

            st.image(
                camera_image,
                caption="Camera Image",
                use_container_width=True
            )


            camera_question = st.text_input(

                "Ask a question about camera image",

                placeholder=(
                    "Example: Solve this question"
                )

            )


            if st.button(
                "🤖 Analyze Camera Image"
            ):

                if camera_question:

                    with st.spinner(
                        "AI is analyzing..."
                    ):

                        instruction = f"""
You are a helpful AI assistant.

Analyze the image carefully.

Student Stream:
{education_stream}

Answer the question based on the image.

If it is an exam question:

- Understand the question.
- Give the correct answer.
- Explain clearly.
- Use exam-friendly format.
"""

                        answer = ask_ai(

                            camera_question,

                            instruction,

                            camera_image

                        )

                        st.markdown(answer)

                else:

                    st.warning(
                        "Please enter a question."
                    )


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.title(
        "🎪 Event & Workshop Planner"
    )

    st.write(
        "Generate complete event plans, schedules and poster prompts."
    )


    event_name = st.text_input(
        "🎯 Event Name"
    )

    event_type = st.selectbox(

        "Select Event Type",

        [

            "Technical Workshop",

            "Seminar",

            "College Fest",

            "Hackathon",

            "Project Expo",

            "Cultural Event",

            "Guest Lecture",

            "Sports Event"

        ]

    )


    event_audience = st.text_input(

        "Target Audience",

        placeholder=(
            "Example: Engineering Students"
        )

    )


    # --------------------------------------------------------
    # EVENT PLAN
    # --------------------------------------------------------

    if st.button(
        "📋 Generate Complete Event Plan"
    ):

        if event_name:

            with st.spinner(
                "Creating event plan..."
            ):

                event_prompt = f"""
Create a complete professional event plan.

Event Name:
{event_name}

Event Type:
{event_type}

Target Audience:
{event_audience}

Provide:

1. Event Overview
2. Objectives
3. Target Audience
4. Required Team Members
5. Complete Schedule
6. Budget Categories
7. Venue Requirements
8. Equipment Required
9. Promotion Plan
10. Social Media Plan
11. Registration Process
12. Event Day Checklist
13. Certificates Plan
14. Feedback Process
15. Conclusion

Use professional and simple English.
"""

                result = ask_ai(

                    event_prompt,

                    "You are an expert college event planner."

                )

                st.session_state.event_result = result

                st.markdown(result)

        else:

            st.warning(
                "Please enter Event Name."
            )


    # --------------------------------------------------------
    # PHOTO PROMPT GENERATOR
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "✍️ AI Event Photo Prompt Generator"
    )

    photo_style = st.selectbox(

        "Photo Style",

        [

            "Professional Photography",

            "Cinematic",

            "Realistic",

            "Modern Poster",

            "College Event Photography",

            "Futuristic",

            "Minimalist"

        ]

    )


    if st.button(
        "✨ Generate Event Image Prompt"
    ):

        if event_name:

            prompt_request = f"""
Create one detailed AI image generation prompt.

Event:
{event_name}

Event Type:
{event_type}

Style:
{photo_style}

The prompt should describe:

- College environment
- Students
- Stage or event activity
- Decorations
- Professional lighting
- Realistic details
- High quality composition

Return only the final image generation prompt.
"""

            image_prompt = ask_ai(

                prompt_request,

                "You are an expert AI image prompt engineer."

            )

            st.subheader(
                "Generated Image Prompt"
            )

            st.code(
                image_prompt,
                language=None
            )

        else:

            st.warning(
                "Enter Event Name first."
            )


    # --------------------------------------------------------
    # TEXT TO IMAGE
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🎨 Text to Image Generator"
    )

    text_to_image_prompt = st.text_area(

        "Describe the image you want to create",

        placeholder=(
            "Example: A professional college technical workshop "
            "with students learning robotics, realistic photography"
        ),

        height=150

    )


    if st.button(
        "🖼️ Generate Image"
    ):

        if text_to_image_prompt:

            with st.spinner(
                "Generating AI image..."
            ):

                generated_image, error = generate_image(
                    text_to_image_prompt
                )


                if error:

                    st.error(
                        f"Image Generation Error: {error}"
                    )

                else:

                    st.success(
                        "Image Generated Successfully!"
                    )

                    st.image(
                        generated_image,
                        use_container_width=True
                    )

        else:

            st.warning(
                "Please enter an image description."
            )


# ============================================================
# EXAM HACKER
# ============================================================

elif app_mode == "📚 Exam Hacker":

    st.title(
        "📚 Exam Hacker"
    )

    st.write(
        "Generate important questions and revision notes."
    )


    subject_name = st.text_input(
        "Enter Subject Name"
    )


    exam_type = st.selectbox(

        "Select Preparation Type",

        [

            "Important Questions",

            "Short Answers",

            "Long Answers",

            "5 Marks Questions",

            "10 Marks Questions",

            "Complete Revision Notes"

        ]

    )


    if st.button(
        "📝 Generate Exam Preparation"
    ):

        if subject_name:

            with st.spinner(
                "Preparing exam material..."
            ):

                exam_prompt = f"""
Student Stream:
{education_stream}

Subject:
{subject_name}

Preparation Type:
{exam_type}

Generate useful academic content.

If Important Questions:
Give important questions with answers.

If Short Answers:
Give concise exam answers.

If Long Answers:
Give detailed answers with headings.

If 5 Marks:
Give medium detailed answers.

If 10 Marks:
Give complete detailed answers.

If Revision Notes:
Give chapter-wise revision points.

Use simple English and exam-friendly format.
"""

                result = ask_ai(

                    exam_prompt,

                    "You are an expert university professor and exam preparation assistant."

                )

                st.session_state.exam_result = result

                st.markdown(result)

        else:

            st.warning(
                "Please enter Subject Name."
            )


# ============================================================
# PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.title(
        "💼 Placement & Career Prep"
    )

    st.write(
        "Prepare for technical interviews and placements."
    )


    role_name = st.text_input(

        "Target Job Role",

        placeholder=(
            "Example: Electrical Engineer, Python Developer"
        )

    )


    company_name = st.text_input(

        "Target Company (Optional)",

        placeholder=(
            "Example: TCS, Infosys"
        )

    )


    experience_level = st.selectbox(

        "Experience Level",

        [

            "Fresher",

            "Student",

            "Internship Candidate"

        ]

    )


    if st.button(
        "🎯 Generate Placement Guide"
    ):

        if role_name:

            with st.spinner(
                "Preparing interview guide..."
            ):

                placement_prompt = f"""
Student Stream:
{education_stream}

Target Role:
{role_name}

Target Company:
{company_name}

Candidate Level:
{experience_level}

Create a complete placement preparation guide.

Include:

1. Role Overview
2. Required Skills
3. Technical Topics
4. Top Interview Questions
5. Answers to Important Questions
6. HR Questions
7. Self Introduction Sample
8. Resume Tips
9. Project Explanation Tips
10. 7 Day Preparation Plan

Use simple English.
"""

                result = ask_ai(

                    placement_prompt,

                    "You are an expert career and placement mentor."

                )

                st.session_state.placement_result = result

                st.markdown(result)

        else:

            st.warning(
                "Please enter Target Job Role."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <h4>🚀 Tech Mithra AI Pro</h4>
        <p>AI Academic • Technical • Event • Exam • Placement Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)
