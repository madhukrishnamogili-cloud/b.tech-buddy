import streamlit as st
from openai import OpenAI
import base64


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# SETTINGS
# ============================================================

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

TEXT_MODEL = "gpt-5.6-luna"
IMAGE_MODEL = "gpt-image-2"


# ============================================================
# SESSION STATE
# ============================================================

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

if "generated_event_plan" not in st.session_state:
    st.session_state.generated_event_plan = ""

if "generated_image_prompt" not in st.session_state:
    st.session_state.generated_image_prompt = ""

if "generated_image" not in st.session_state:
    st.session_state.generated_image = None


# ============================================================
# OPENAI CLIENT
# ============================================================

def get_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]

        client = OpenAI(
            api_key=api_key
        )

        return client

    except Exception:
        return None


# ============================================================
# MAIN AI RESPONSE FUNCTION
# ============================================================

def get_ai_response(stream_name, user_question, mode):

    client = get_client()

    if client is None:
        return """
❌ **OpenAI API Key Error**

Please add your API key in Streamlit Secrets.

Example:

OPENAI_API_KEY = "your_api_key_here"
"""


    # --------------------------------------------------------
    # PROJECT & LAB GUIDE
    # --------------------------------------------------------

    if mode == "🤖 Project & Lab Guide":

        feature_instruction = """
You are an expert academic and technical tutor.

Answer the exact question asked by the student.

Rules:
- Give the direct answer first.
- Explain clearly.
- Use simple English.
- If the question is Telugu, answer in Telugu.
- Use headings when useful.
- Use bullet points when useful.
- For technical questions explain definition, working,
  components and applications when relevant.
- Do not give unrelated generic answers.
"""


    # --------------------------------------------------------
    # EVENT PLANNER
    # --------------------------------------------------------

    elif mode == "🎪 Event Planner":

        feature_instruction = """
You are a professional college event planner.

Create a detailed and practical event plan.

Include:

1. Event Title
2. Event Theme
3. Objective
4. Target Participants
5. Suggested Venue
6. Date and Time Suggestion
7. Complete Event Schedule
8. Required Resources
9. Team Responsibilities
10. Budget Considerations
11. Promotion Strategy
12. Expected Outcome

Keep everything directly related to the event topic.
"""


    # --------------------------------------------------------
    # EXAM HACKER
    # --------------------------------------------------------

    elif mode == "📚 Exam Hacker":

        feature_instruction = """
You are an expert exam preparation assistant.

Prepare study material based on the topic.

Include:

1. Definition
2. Important Concepts
3. Key Points
4. Important Short Questions
5. Important 5-Mark Questions
6. Important Long Questions
7. Quick Revision Notes

Keep the content directly related to the topic.
"""


    # --------------------------------------------------------
    # PLACEMENT PREP
    # --------------------------------------------------------

    elif mode == "💼 Placement Prep":

        feature_instruction = """
You are a professional placement and interview assistant.

Based on the requested job role or technology provide:

1. Required Skills
2. Important Technical Topics
3. Technical Interview Questions
4. Sample Answers
5. HR Interview Questions
6. Preparation Roadmap
7. Career Tips

Keep everything directly related to the role.
"""


    else:

        feature_instruction = """
Answer accurately and clearly.
"""


    instructions = f"""
You are Tech Mithra AI Pro.

The student's education stream is:

{stream_name}

{feature_instruction}

Important rules:

- Answer exactly what the user asks.
- Be helpful and accurate.
- Do not give unrelated generic content.
- Use simple language.
- If the user writes in Telugu, answer in Telugu.
- If the user writes in English, answer in English.
"""


    try:

        response = client.responses.create(
            model=TEXT_MODEL,
            instructions=instructions,
            input=user_question
        )

        return response.output_text

    except Exception as e:

        return f"""
❌ **AI Error**

{str(e)}
"""


# ============================================================
# EVENT IMAGE PROMPT GENERATOR
# ============================================================

def generate_event_image_prompt(event_topic, event_plan):

    client = get_client()

    if client is None:
        return "❌ API Key not found."


    instructions = """
You are an expert AI image prompt writer.

Create one detailed professional image generation prompt
for a college event promotional image.

The image prompt should include:

- College environment
- Relevant students
- Event stage or venue
- Decorations
- Professional lighting
- Realistic atmosphere
- Cinematic composition
- High detail
- Professional event photography style

Do not include unwanted text inside the generated image.

Return only the image generation prompt.
"""


    user_input = f"""
Event Topic:

{event_topic}

Event Plan:

{event_plan}

Create a professional AI image generation prompt.
"""


    try:

        response = client.responses.create(
            model=TEXT_MODEL,
            instructions=instructions,
            input=user_input
        )

        return response.output_text

    except Exception as e:

        return f"❌ Prompt Generation Error: {str(e)}"


# ============================================================
# TEXT TO IMAGE GENERATOR
# ============================================================

def generate_event_image(image_prompt):

    client = get_client()

    if client is None:
        return None, "API Key not found."


    try:

        result = client.images.generate(
            model=IMAGE_MODEL,
            prompt=image_prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json

        image_bytes = base64.b64decode(
            image_base64
        )

        return image_bytes, None


    except Exception as e:

        return None, str(e)


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


    # --------------------------------------------------------
    # ADMIN SETTINGS
    # --------------------------------------------------------

    if (
        st.session_state.user_email.lower()
        == ADMIN_EMAIL.lower()
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

                st.rerun()


    st.divider()


    # --------------------------------------------------------
    # STREAM SELECTION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # APP OPTIONS
    # --------------------------------------------------------

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
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.generated_event_plan = ""

        st.session_state.generated_image_prompt = ""

        st.session_state.generated_image = None

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
# MAIN PAGE
# ============================================================

st.title(
    f"🚀 {st.session_state.app_name}"
)

st.caption(
    f"Selected Stream: {education_stream}"
)


# ============================================================
# OPTION 1: PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.header(
        "🤖 Project & Lab Guide"
    )

    st.info(
        "Ask any academic, technical or general question."
    )


    # Show chat history

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # Ask question

    question = st.chat_input(
        "Ask any question..."
    )


    if question:

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


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# ============================================================
# OPTION 2: EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.header(
        "🎪 AI Event & Workshop Planner"
    )

    st.write(
        "Generate an Event Plan, AI Photo Prompt and Event Image."
    )


    event_topic = st.text_area(
        "🎯 Enter Event Name / Topic:",
        placeholder="Example: PLC Workshop for EEE Students"
    )


    # --------------------------------------------------------
    # GENERATE EVENT PLAN
    # --------------------------------------------------------

    if st.button(
        "📋 Generate Event Plan",
        use_container_width=True
    ):

        if event_topic.strip():

            with st.spinner(
                "🤖 Creating Event Plan..."
            ):

                event_plan = get_ai_response(
                    education_stream,
                    event_topic,
                    app_mode
                )

                st.session_state.generated_event_plan = (
                    event_plan
                )


        else:

            st.warning(
                "Please enter an Event Topic."
            )


    # --------------------------------------------------------
    # SHOW EVENT PLAN
    # --------------------------------------------------------

    if st.session_state.generated_event_plan:

        st.subheader(
            "📋 Generated Event Plan"
        )

        st.markdown(
            st.session_state.generated_event_plan
        )

        st.divider()


        # ----------------------------------------------------
        # GENERATE IMAGE PROMPT
        # ----------------------------------------------------

        if st.button(
            "✍️ Generate Event Photo Prompt",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Creating AI Image Prompt..."
            ):

                image_prompt = (
                    generate_event_image_prompt(
                        event_topic,
                        st.session_state.generated_event_plan
                    )
                )

                st.session_state.generated_image_prompt = (
                    image_prompt
                )


    # --------------------------------------------------------
    # SHOW IMAGE PROMPT
    # --------------------------------------------------------

    if st.session_state.generated_image_prompt:

        st.subheader(
            "📝 AI Generated Image Prompt"
        )

        st.text_area(
            "Photo Generation Prompt:",
            value=st.session_state.generated_image_prompt,
            height=250
        )

        st.divider()


        # ----------------------------------------------------
        # GENERATE IMAGE
        # ----------------------------------------------------

        if st.button(
            "🖼️ Generate Event Image",
            use_container_width=True
        ):

            with st.spinner(
                "🎨 AI is generating image..."
            ):

                image_bytes, error = (
                    generate_event_image(
                        st.session_state.generated_image_prompt
                    )
                )


                if error:

                    st.error(
                        f"Image Generation Error: {error}"
                    )

                else:

                    st.session_state.generated_image = (
                        image_bytes
                    )


    # --------------------------------------------------------
    # SHOW GENERATED IMAGE
    # --------------------------------------------------------

    if st.session_state.generated_image:

        st.subheader(
            "🎨 Generated Event Image"
        )

        st.image(
            st.session_state.generated_image,
            caption="AI Generated Event Promotional Image",
            use_container_width=True
        )

        st.download_button(
            label="⬇️ Download Event Image",
            data=st.session_state.generated_image,
            file_name="tech_mithra_event_image.png",
            mime="image/png",
            use_container_width=True
        )


# ============================================================
# OPTION 3: EXAM HACKER
# ============================================================

elif app_mode == "📚 Exam Hacker":

    st.header(
        "📚 AI Exam Preparation"
    )

    subject_name = st.text_area(
        "Enter Subject or Topic:",
        placeholder="Example: Electric Vehicles"
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


# ============================================================
# OPTION 4: PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.header(
        "💼 Placement & Career Preparation"
    )

    role_name = st.text_area(
        "Enter Target Job Role / Technology:",
        placeholder="Example: Electrical Engineer"
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
