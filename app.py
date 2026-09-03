import streamlit as st
from openai import OpenAI


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)


# =========================================================
# APP SETTINGS
# =========================================================

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"


# =========================================================
# SESSION STATE
# =========================================================

if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra AI Pro 🎓"

if "app_logo" not in st.session_state:
    st.session_state.app_logo = (
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# LOGIN SYSTEM
# =========================================================

if "user" in st.query_params:

    st.session_state.logged_in = True
    st.session_state.user_email = st.query_params["user"]


if not st.session_state.logged_in:

    st.markdown(
        f"""
        <h1 style='text-align:center;'>
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

                st.session_state.user_email = (
                    email_input
                )

                st.query_params["user"] = (
                    email_input
                )

                st.rerun()

            else:

                st.error(
                    "ఈమెయిల్ మరియు పాస్‌వర్డ్ ఇవ్వండి!"
                )

    st.stop()


# =========================================================
# OPENAI CLIENT
# =========================================================

def get_client():

    try:

        api_key = st.secrets["OPENAI_API_KEY"]

        return OpenAI(
            api_key=api_key
        )

    except Exception as e:

        st.error(
            "❌ OPENAI_API_KEY కనబడలేదు. "
            "Streamlit Secrets లో API Key add చేయండి."
        )

        return None


# =========================================================
# AI RESPONSE FUNCTION
# =========================================================

def get_openai_response(
    stream_name,
    question,
    mode
):

    client = get_client()

    if client is None:

        return None


    # =====================================================
    # PROJECT & LAB GUIDE INSTRUCTIONS
    # =====================================================

    if mode == "🤖 Project & Lab Guide":

        feature_instruction = """

You are an expert academic and technical tutor.

Answer the EXACT question asked by the student.

Rules:

1. Give a direct definition first.
2. Explain the concept clearly.
3. Use simple English.
4. Give important points.
5. Use bullet points where useful.
6. Give examples when relevant.
7. For engineering questions explain components,
   working principle and applications when applicable.
8. Do NOT give generic answers.
9. Do NOT give unrelated information.
10. If the question is short, answer directly.
11. If the user asks for a long answer,
    provide a detailed exam-style answer.

"""


    # =====================================================
    # EXAM PREPARATION
    # =====================================================

    elif mode == "📚 Exam Hacker":

        feature_instruction = """

You are an exam preparation assistant.

Based on the exact topic given by the student,
provide useful exam preparation material.

Include:

1. Definition
2. Important concepts
3. Key points
4. Short-answer questions
5. Long-answer questions
6. Revision notes

Everything must be relevant to the topic.

Do not generate generic unrelated content.

"""


    # =====================================================
    # EVENT PLANNER
    # =====================================================

    elif mode == "🎪 Event Planner":

        feature_instruction = """

You are a professional college event planner.

Create a complete event plan based on
the exact event topic given by the user.

Include:

1. Event title
2. Event objective
3. Target participants
4. Event schedule
5. Required resources
6. Team responsibilities
7. Budget considerations
8. Promotion strategy
9. Expected outcome

"""


    # =====================================================
    # PLACEMENT PREPARATION
    # =====================================================

    elif mode == "💼 Placement Prep":

        feature_instruction = """

You are a professional placement and
interview preparation assistant.

Based on the exact job role or technology
requested by the student, provide:

1. Required skills
2. Important technical topics
3. Interview questions
4. Sample answers
5. HR questions
6. Preparation roadmap

"""


    else:

        feature_instruction = """

Answer the exact question clearly
and accurately.

"""


    # =====================================================
    # MAIN AI INSTRUCTIONS
    # =====================================================

    instructions = f"""

You are Tech Mithra AI Pro.

Student Stream:

{stream_name}

{feature_instruction}

IMPORTANT RULES:

- Answer the exact question asked.
- Never give unrelated generic academic reports.
- Be accurate.
- Use simple English.
- Use headings when useful.
- Use bullet points when useful.
- If the user asks in Telugu, answer in Telugu.
- If the user asks in English, answer in English.

"""


    # =====================================================
    # OPENAI API CALL
    # =====================================================

    try:

        response = client.responses.create(

            model="gpt-4o-mini",

            instructions=instructions,

            input=question
        )

        return response.output_text


    except Exception as e:

        return (
            "❌ AI Error:\n\n"
            + str(e)
        )


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


    # =====================================================
    # ADMIN SETTINGS
    # =====================================================

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

                st.session_state.app_name = (
                    new_name
                )

                st.session_state.app_logo = (
                    new_logo
                )

                st.rerun()


    st.divider()


    # =====================================================
    # STREAM SELECTION
    # =====================================================

    education_stream = st.selectbox(

        "📚 Select Stream:",

        [

            "⚡ Engineering (B.Tech / EEE / CSE)",

            "💊 Pharmacy (B.Pharm / Pharm.D)",

            "🩺 Nursing (B.Sc / GNM)",

            "📈 MBA (Management)"

        ]

    )


    st.divider()


    # =====================================================
    # FEATURE SELECTION
    # =====================================================

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


    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user_email = ""

        st.session_state.messages = []

        st.query_params.clear()

        st.rerun()


# =========================================================
# MAIN APP
# =========================================================

st.title(
    f"🚀 {st.session_state.app_name}"
)


# =========================================================
# PROJECT & LAB GUIDE
# =========================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        "🤖 AI Academic & Technical Assistant"
    )

    st.caption(
        f"Selected Stream: {education_stream}"
    )


    # =====================================================
    # SHOW CHAT HISTORY
    # =====================================================

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Ask any academic or technical question..."
    )


    if prompt:


        # USER MESSAGE

        with st.chat_message(
            "user"
        ):

            st.markdown(
                prompt
            )


        st.session_state.messages.append(

            {

                "role": "user",

                "content": prompt

            }

        )


        # AI MESSAGE

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 Tech Mithra AI is thinking..."
            ):

                reply_text = get_openai_response(

                    education_stream,

                    prompt,

                    app_mode

                )


                if reply_text:

                    st.markdown(
                        reply_text
                    )


        # SAVE AI RESPONSE

        if reply_text:

            st.session_state.messages.append(

                {

                    "role": "assistant",

                    "content": reply_text

                }

            )


# =========================================================
# EVENT PLANNER
# =========================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 Event & Workshop Planner"
    )


    st.write(
        "Enter your college event or workshop topic."
    )


    event_topic = st.text_area(

        "Enter Event Name / Topic:",

        placeholder=
        "Example: PLC Workshop for EEE Students"

    )


    if st.button(
        "Generate Event Plan",
        use_container_width=True
    ):


        if event_topic.strip():


            with st.spinner(
                "🤖 Creating Event Plan..."
            ):


                answer = get_openai_response(

                    education_stream,

                    event_topic,

                    app_mode

                )


                if answer:

                    st.markdown(
                        answer
                    )


        else:

            st.warning(
                "Please enter an Event Topic."
            )


# =========================================================
# EXAM HACKER
# =========================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 AI Exam Preparation"
    )


    st.write(
        "Enter a subject or topic for exam preparation."
    )


    subject_name = st.text_area(

        "Enter Subject or Topic:",

        placeholder=
        "Example: Electric Vehicles"

    )


    if st.button(
        "Generate Exam Preparation",
        use_container_width=True
    ):


        if subject_name.strip():


            with st.spinner(
                "🤖 Preparing Exam Notes..."
            ):


                answer = get_openai_response(

                    education_stream,

                    subject_name,

                    app_mode

                )


                if answer:

                    st.markdown(
                        answer
                    )


        else:

            st.warning(
                "Please enter a Subject or Topic."
            )


# =========================================================
# PLACEMENT PREP
# =========================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 Placement & Career Preparation"
    )


    st.write(
        "Enter your target job role or technology."
    )


    role_name = st.text_area(

        "Enter Target Job Role / Technology:",

        placeholder=
        "Example: Electrical Engineer"

    )


    if st.button(
        "Generate Interview Guide",
        use_container_width=True
    ):


        if role_name.strip():


            with st.spinner(
                "🤖 Preparing Interview Guide..."
            ):


                answer = get_openai_response(

                    education_stream,

                    role_name,

                    app_mode

                )


                if answer:

                    st.markdown(
                        answer
                    )


        else:

            st.warning(
                "Please enter a Job Role or Technology."
            )
