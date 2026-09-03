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
# OPENAI CLIENT
# =========================================================

def get_client():

    try:

        api_key = st.secrets["OPENAI_API_KEY"]

        return OpenAI(
            api_key=api_key
        )

    except Exception:

        return None


# =========================================================
# AI RESPONSE FUNCTION
# =========================================================

def get_ai_response(
    stream_name,
    question,
    mode
):

    client = get_client()

    if client is None:

        return (
            "❌ API Key not found.\n\n"
            "Please add OPENAI_API_KEY in Streamlit Secrets."
        )


    # =====================================================
    # PROJECT & LAB GUIDE
    # =====================================================

    if mode == "🤖 Project & Lab Guide":

        feature_instruction = """

You are an expert academic and technical tutor.

Answer the EXACT question asked by the student.

Rules:

1. Give a direct definition first.
2. Explain clearly.
3. Use simple English.
4. Give important points.
5. Use bullet points when useful.
6. Give examples when relevant.
7. For engineering questions explain:
   - Definition
   - Components
   - Working principle
   - Applications
8. Do NOT give generic answers.
9. Do NOT give unrelated information.
10. Answer according to the exact question.

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

1. Event Title
2. Event Objective
3. Target Participants
4. Date and Schedule Suggestion
5. Required Resources
6. Team Responsibilities
7. Budget Requirements
8. Promotion Plan
9. Expected Outcome

"""


    # =====================================================
    # EXAM HACKER
    # =====================================================

    elif mode == "📚 Exam Hacker":

        feature_instruction = """

You are an expert exam preparation assistant.

Based on the exact subject or topic,
provide:

1. Simple Definition
2. Important Concepts
3. Key Points
4. Important 2-Mark Questions
5. Important 5-Mark Questions
6. Important Long Questions
7. Quick Revision Notes

Keep everything directly related to
the topic requested by the student.

"""


    # =====================================================
    # PLACEMENT PREP
    # =====================================================

    elif mode == "💼 Placement Prep":

        feature_instruction = """

You are a professional placement and
interview preparation assistant.

Based on the exact job role or technology,
provide:

1. Required Skills
2. Important Technical Topics
3. Frequently Asked Interview Questions
4. Sample Answers
5. HR Interview Questions
6. Preparation Roadmap
7. Tips for Students

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
- Never give unrelated generic answers.
- Be accurate.
- Use simple English.
- Use headings when useful.
- Use bullet points when useful.
- If the user asks in Telugu, answer in Telugu.
- If the user asks in English, answer in English.
- Do not invent information.

"""


    # =====================================================
    # OPENAI API REQUEST
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
# LOGIN SYSTEM
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


    # =====================================================
    # LOGO
    # =====================================================

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
    # CLEAR CHAT
    # =====================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


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

        st.rerun()


# =========================================================
# MAIN PAGE
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

    st.info(
        "Ask any academic, technical or general question."
    )


    # =====================================================
    # SHOW CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # =====================================================
    # QUESTION INPUT
    # =====================================================

    question = st.chat_input(
        "Ask your question here..."
    )


    if question:


        # =================================================
        # USER MESSAGE
        # =================================================

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )


        st.session_state.messages.append(

            {

                "role": "user",

                "content": question

            }

        )


        # =================================================
        # AI MESSAGE
        # =================================================

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 Tech Mithra AI is thinking..."
            ):

                answer = get_ai_response(

                    education_stream,

                    question,

                    app_mode

                )


                st.markdown(
                    answer
                )


        # =================================================
        # SAVE AI MESSAGE
        # =================================================

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


    st.write(
        "Enter your college event or workshop topic."
    )


    event_topic = st.text_area(

        "Enter Event Name / Topic:",

        placeholder=
        "Example: PLC Workshop for EEE Students"

    )


    if st.button(
        "🚀 Generate Event Plan",
        use_container_width=True
    ):


        if event_topic.strip():


            with st.spinner(
                "🤖 Creating Event Plan..."
            ):


                answer = get_ai_response(

                    education_stream,

                    event_topic,

                    app_mode

                )


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
        "📚 Generate Exam Preparation",
        use_container_width=True
    ):


        if subject_name.strip():


            with st.spinner(
                "🤖 Preparing Exam Notes..."
            ):


                answer = get_ai_response(

                    education_stream,

                    subject_name,

                    app_mode

                )


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
        "💼 Generate Interview Guide",
        use_container_width=True
    ):


        if role_name.strip():


            with st.spinner(
                "🤖 Preparing Interview Guide..."
            ):


                answer = get_ai_response(

                    education_stream,

                    role_name,

                    app_mode

                )


                st.markdown(
                    answer
                )


        else:

            st.warning(
                "Please enter a Job Role or Technology."
            )
