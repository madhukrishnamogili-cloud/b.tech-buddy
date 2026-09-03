import streamlit as st
from openai import OpenAI
from PIL import Image
import base64


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# APP SETTINGS
# =========================================================

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra AI Pro 🎓"

if "app_logo" not in st.session_state:
    st.session_state.app_logo = (
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""


# =========================================================
# OPENAI CLIENT
# =========================================================

def get_client():
    try:
        api_key = st.secrets["AQ.Ab8RN6I3jgQZO2vSrPEKFThDE70F-Y0UwMus30JK3CbBZc4eDw"]
        return OpenAI(api_key=api_key)
    except Exception:
        st.error(
            "❌ OpenAI API Key కనబడలేదు. "
            "Streamlit Secrets లో OPENAI_API_KEY add చేయండి."
        )
        return None


# =========================================================
# IMAGE TO BASE64
# =========================================================

def image_to_base64(image_file):

    image_bytes = image_file.getvalue()

    encoded = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    mime_type = image_file.type

    return f"data:{mime_type};base64,{encoded}"


# =========================================================
# AI RESPONSE FUNCTION
# =========================================================

def get_ai_response(
    stream_name,
    question,
    mode,
    image_file=None
):

    client = get_client()

    if client is None:
        return None

    # Different instructions for different features

    if mode == "🤖 Project & Lab Guide":

        feature_instruction = """
You are an expert academic tutor and technical assistant.

Answer the student's exact question.

For technical questions:
1. Give a direct definition first.
2. Explain the concept clearly.
3. Explain working principle if applicable.
4. List important components.
5. Give applications.
6. Give advantages and disadvantages when relevant.
7. Use simple English suitable for students.

Do not give generic or unrelated content.
If the question is short, give a short accurate answer.
If the student asks for a long answer, give a detailed exam-style answer.
"""

    elif mode == "📚 Exam Hacker":

        feature_instruction = """
You are an exam preparation assistant.

Answer the exact topic requested by the student.

Provide:
1. Important definition.
2. Key concepts.
3. Important exam points.
4. Possible short-answer questions.
5. Possible long-answer questions.
6. Easy revision notes.

Keep the answer academically accurate.
Do not generate unrelated generic content.
"""

    elif mode == "🎪 Event Planner":

        feature_instruction = """
You are a professional college event planner.

Create a practical event plan based exactly on the user's event topic.

Include:
1. Event objective.
2. Target participants.
3. Schedule.
4. Required resources.
5. Team responsibilities.
6. Budget considerations.
7. Promotion plan.
8. Expected outcome.
"""

    elif mode == "💼 Placement Prep":

        feature_instruction = """
You are a professional placement and interview preparation assistant.

Based on the job role or technology requested, provide:

1. Required skills.
2. Important technical topics.
3. Frequently asked interview questions.
4. Sample answers.
5. HR questions.
6. Preparation roadmap.

Make the content relevant to the exact role requested.
"""

    else:
        feature_instruction = """
You are a helpful AI assistant.
Answer the user's exact question accurately.
"""


    system_instruction = f"""
You are Tech Mithra AI Pro.

The student belongs to:
{stream_name}

{feature_instruction}

IMPORTANT RULES:

- Answer the exact question asked.
- Never replace the answer with generic academic text.
- Do not invent unrelated information.
- Use clear headings.
- Use bullet points where useful.
- Explain difficult topics in simple English.
- You can answer in Telugu if the user asks in Telugu.
"""


    try:

        # -------------------------------
        # TEXT ONLY
        # -------------------------------

        if image_file is None:

            response = client.responses.create(

                model="gpt-5.6-luna",

                instructions=system_instruction,

                input=question
            )

        # -------------------------------
        # TEXT + IMAGE
        # -------------------------------

        else:

            image_data = image_to_base64(
                image_file
            )

            response = client.responses.create(

                model="gpt-5.6-luna",

                instructions=system_instruction,

                input=[
                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "input_text",

                                "text": question
                            },

                            {
                                "type": "input_image",

                                "image_url": image_data
                            }
                        ]
                    }
                ]
            )

        return response.output_text

    except Exception as e:

        return (
            "❌ AI response error:\n\n"
            f"`{str(e)}`"
        )


# =========================================================
# SIMPLE LOGIN
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        f"""
        <h1 style='text-align:center;'>
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

            if email_input and password_input:

                st.session_state.logged_in = True

                st.session_state.user_email = (
                    email_input
                )

                st.rerun()

            else:

                st.error(
                    "ఈమెయిల్ మరియు పాస్‌వర్డ్ ఇవ్వండి!"
                )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        st.session_state.app_logo,
        width=100
    )

    st.title(
        st.session_state.app_name
    )


    # -------------------------
    # ADMIN SETTINGS
    # -------------------------

    if (
        st.session_state.user_email
        == ADMIN_EMAIL
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

                st.session_state.app_name = (
                    new_name
                )

                st.session_state.app_logo = (
                    new_logo
                )

                st.rerun()


    st.divider()


    education_stream = st.selectbox(

        "📚 Select Stream",

        [
            "⚡ Engineering",
            "💊 Pharmacy",
            "🩺 Nursing",
            "📈 MBA"
        ]
    )


    st.divider()


    app_mode = st.radio(

        "Select Feature:",

        [
            "🤖 Project & Lab Guide",
            "🎪 Event Planner",
            "📚 Exam Hacker",
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

        st.rerun()


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    f"🚀 {st.session_state.app_name}"
)

st.caption(
    f"Selected Stream: {education_stream}"
)


# =========================================================
# PROJECT & LAB GUIDE
# =========================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        "🤖 AI Academic & Technical Assistant"
    )


    tab1, tab2, tab3 = st.tabs(

        [
            "💬 Ask Question",
            "🖼️ Upload Image",
            "📸 Camera"
        ]
    )


    image_file = None


    with tab2:

        uploaded_file = st.file_uploader(

            "Upload Question / Lab Manual / Diagram",

            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )


        if uploaded_file:

            image_file = uploaded_file

            image = Image.open(
                uploaded_file
            )

            st.image(
                image,
                caption="Uploaded Image",
                width=400
            )


    with tab3:

        camera_photo = st.camera_input(

            "Take a Photo"
        )


        if camera_photo:

            image_file = camera_photo

            image = Image.open(
                camera_photo
            )

            st.image(
                image,
                caption="Camera Image",
                width=400
            )


    # -------------------------
    # SHOW CHAT HISTORY
    # -------------------------

    for message in (
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # -------------------------
    # USER QUESTION
    # -------------------------

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
                "🤖 Tech Mithra AI is thinking..."
            ):

                answer = get_ai_response(

                    education_stream,

                    prompt,

                    app_mode,

                    image_file
                )


                st.markdown(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# =========================================================
# EVENT PLANNER
# =========================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 Event & Workshop Planner"
    )


    event_topic = st.text_area(

        "Enter Event Name or Topic",

        placeholder=
        "Example: PLC Workshop for EEE Students"
    )


    if st.button(
        "Generate Event Plan",
        use_container_width=True
    ):

        if event_topic:

            with st.spinner(
                "Creating Event Plan..."
            ):

                answer = get_ai_response(

                    education_stream,

                    event_topic,

                    app_mode
                )

                st.markdown(answer)

        else:

            st.warning(
                "Please enter an event topic."
            )


# =========================================================
# EXAM HACKER
# =========================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 AI Exam Preparation"
    )


    subject_topic = st.text_area(

        "Enter Subject / Topic",

        placeholder=
        "Example: Electric Vehicles"
    )


    if st.button(
        "Generate Exam Preparation",
        use_container_width=True
    ):

        if subject_topic:

            with st.spinner(
                "Preparing exam notes..."
            ):

                answer = get_ai_response(

                    education_stream,

                    subject_topic,

                    app_mode
                )

                st.markdown(answer)

        else:

            st.warning(
                "Please enter a subject or topic."
            )


# =========================================================
# PLACEMENT PREP
# =========================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 Placement & Interview Preparation"
    )


    role_name = st.text_area(

        "Enter Job Role / Technology",

        placeholder=
        "Example: Electrical Engineer"
    )


    if st.button(
        "Generate Interview Guide",
        use_container_width=True
    ):

        if role_name:

            with st.spinner(
                "Preparing Interview Guide..."
            ):

                answer = get_ai_response(

                    education_stream,

                    role_name,

                    app_mode
                )

                st.markdown(answer)

        else:

            st.warning(
                "Please enter a job role."
            )
