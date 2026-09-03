import streamlit as st
from openai import OpenAI
from PIL import Image


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro 🎓",
    page_icon="🚀",
    layout="wide"
)


ADMIN_EMAIL = "madhukrishnamogili@gmail.com"


# =====================================================
# SESSION SETTINGS
# =====================================================

if "app_name" not in st.session_state:
    st.session_state.app_name = "Tech Mithra Pro 🎓"

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


# =====================================================
# LOGIN SYSTEM
# =====================================================

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

        email_input = st.text_input("📧 Email Address")

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

                st.query_params["user"] = email_input

                st.rerun()

            else:

                st.error(
                    "ఈమెయిల్ మరియు పాస్‌వర్డ్ ఇవ్వండి!"
                )

    st.stop()


# =====================================================
# OPENAI CLIENT
# =====================================================

def get_client():

    try:

        api_key = st.secrets["OPENAI_API_KEY"]

        return OpenAI(
            api_key=api_key
        )

    except Exception:

        st.error(
            "❌ OPENAI_API_KEY కనబడలేదు. "
            "Streamlit Secrets లో API Key add చేయండి."
        )

        return None


# =====================================================
# AI RESPONSE
# =====================================================

def get_openai_response(
    stream_name,
    question,
    mode
):

    client = get_client()

    if client is None:
        return None


    # ---------------------------------------------
    # PROJECT & LAB GUIDE
    # ---------------------------------------------

    if mode == "🤖 Project & Lab Guide":

        feature_instruction = """

You are an expert academic and technical tutor.

Answer the EXACT question asked by the student.

Rules:

1. First give a direct definition.
2. Explain the topic clearly.
3. Use simple English.
4. Give important points.
5. Use bullet points where useful.
6. Give examples when relevant.
7. For engineering questions explain working principle,
   components and applications when applicable.
8. Do NOT give generic or unrelated answers.
9. If the question is short, answer directly.
10. If the user asks for a long answer,
    provide a detailed exam-style answer.

"""


    # ---------------------------------------------
    # EXAM HACKER
    # ---------------------------------------------

    elif mode == "📚 Exam Hacker":

        feature_instruction = """

You are an exam preparation assistant.

Based on the exact topic given by the student, provide:

1. Definition
2. Important concepts
3. Key points
4. Short-answer questions
5. Long-answer questions
6. Revision notes

Keep everything relevant to the topic.
Do not generate generic answers.

"""


    # ---------------------------------------------
    # EVENT PLANNER
    # ---------------------------------------------

    elif mode == "🎪 Event Planner":

        feature_instruction = """

You are a professional college event planner.

Create a complete plan based on the exact event topic.

Include:

1. Event objective
2. Target participants
3. Event schedule
4. Required resources
5. Team responsibilities
6. Budget considerations
7. Promotion strategy
8. Expected outcome

"""


    # ---------------------------------------------
    # PLACEMENT PREP
    # ---------------------------------------------

    elif mode == "💼 Placement Prep":

        feature_instruction = """

You are a professional placement and interview preparation assistant.

Based on the exact job role requested, provide:

1. Required skills
2. Important technical topics
3. Interview questions
4. Sample answers
5. HR questions
6. Preparation roadmap

"""


    else:

        feature_instruction = """
Answer the exact question clearly and accurately.
"""


    instructions = f"""

You are Tech Mithra AI Pro.

Student Stream:
{stream_name}

{feature_instruction}

IMPORTANT:

- Answer only what the user asks.
- Never give unrelated generic academic reports.
- Be accurate.
- Use simple English.
- Use Telugu if the student asks in Telugu.

"""


    try:

        response = client.responses.create(

            model="gpt-5.6-luna",

            instructions=instructions,

            input=question
        )


        return response.output_text


    except Exception as e:

        return (
            "❌ AI Error: "
            + str(e)
        )


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        st.session_state.app_logo,
        width=100
    )

    st.title(
        st.session_state.app_name
    )


    # ADMIN SETTINGS

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

                st.session_state.app_name = new_name
                st.session_state.app_logo = new_logo

                st.rerun()


    st.divider()


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
        "🚪 Logout"
    ):

        st.session_state.logged_in = False

        st.session_state.user_email = ""

        st.session_state.messages = []

        st.query_params.clear()

        st.rerun()


# =====================================================
# PROJECT & LAB GUIDE
# =====================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        f"🤖 {st.session_state.app_name}"
    )


    stream_short = education_stream


    # CHAT HISTORY

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )


    # QUESTION INPUT

    prompt = st.chat_input(
        "Ask any academic or technical question..."
    )


    if prompt:


        # USER MESSAGE

        with st.chat_message("user"):

            st.markdown(prompt)


        st.session_state.messages.append(

            {

                "role": "user",

                "content": prompt

            }

        )


        # AI MESSAGE

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Tech Mithra AI is thinking..."
            ):

                reply_text = get_openai_response(

                    stream_short,

                    prompt,

                    app_mode

                )


                if reply_text:

                    st.markdown(
                        reply_text
                    )


        # SAVE AI MESSAGE

        if reply_text:

            st.session_state.messages.append(

                {

                    "role": "assistant",

                    "content": reply_text

                }

            )


# =====================================================
# EVENT PLANNER
# =====================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 Event & Workshop Planner"
    )


    event_topic = st.text_area(

        "Enter Event Name / Topic:",

        placeholder=
        "Example: PLC Workshop for EEE Students"

    )


    if st.button(
        "Generate Event Plan"
    ):


        if event_topic:


            with st.spinner(
                "Creating Event Plan..."
            ):


                answer = get_openai_response(

                    education_stream,

                    event_topic,

                    app_mode

                )


                if answer:

                    st.markdown(answer)


        else:

            st.warning(
                "Please enter an Event Topic."
            )


# =====================================================
# EXAM HACKER
# =====================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 AI Exam Preparation"
    )


    subject_name = st.text_area(

        "Enter Subject or Topic:",

        placeholder=
        "Example: Electric Vehicles"

    )


    if st.button(
        "Generate Exam Questions"
    ):


        if subject_name:


            with st.spinner(
                "Preparing Exam Questions..."
            ):


                answer = get_openai_response(

                    education_stream,

                    subject_name,

                    app_mode

                )


                if answer:

                    st.markdown(answer)


        else:

            st.warning(
                "Please enter a subject or topic."
            )


# =====================================================
# PLACEMENT PREP
# =====================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 Placement & Career Preparation"
    )


    role_name = st.text_area(

        "Enter Target Job Role / Technology:",

        placeholder=
        "Example: Electrical Engineer"

    )


    if st.button(
        "Generate Interview Guide"
    ):


        if role_name:


            with st.spinner(
                "Preparing Interview Guide..."
            ):


                answer = get_openai_response(

                    education_stream,

                    role_name,

                    app_mode

                )


                if answer:

                    st.markdown(answer)


        else:

            st.warning(
                "Please enter a Job Role."
            )
