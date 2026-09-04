# ============================================================
# TECH MITHRA AI PRO
# COMPLETE app.py - ONE FILE
# ============================================================
#
# INSTALL:
# pip install streamlit google-genai pillow
#
# STREAMLIT SECRETS:
# Create:
# .streamlit/secrets.toml
#
# Add:
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
#
# RUN:
# streamlit run app.py
#
# ============================================================


import streamlit as st
from google import genai
from PIL import Image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APP NAME
# ============================================================

APP_NAME = "🚀 Tech Mithra AI Pro"


# ============================================================
# CUSTOM CSS - MOBILE FRIENDLY
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 28px !important;
        }

        h2 {
            font-size: 23px !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# GET GEMINI API KEY
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
def get_gemini_client(api_key):

    try:

        client = genai.Client(
            api_key=api_key
        )

        return client

    except Exception:

        return None


# ============================================================
# FAST AI MODELS
# ============================================================

FAST_MODELS = [

    "gemini-2.5-flash-lite",

    "gemini-2.5-flash"

]


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(question, instruction="", image=None):

    api_key = get_api_key()

    if not api_key:

        return None


    client = get_gemini_client(api_key)

    if client is None:

        return None


    prompt = f"""
{instruction}

User Question:

{question}

Important Instructions:

- Answer directly.
- Understand the user's exact question.
- For small questions give a short and fast answer.
- For detailed questions give a detailed answer.
- Use simple English.
- Use headings when needed.
- Use bullet points when useful.
- Be helpful like ChatGPT.
- Do not unnecessarily repeat information.
"""


    if image is not None:

        contents = [

            prompt,

            image

        ]

    else:

        contents = prompt


    for model_name in FAST_MODELS:

        try:

            response = client.models.generate_content(

                model=model_name,

                contents=contents

            )


            if response:

                if getattr(response, "text", None):

                    return response.text.strip()


        except Exception:

            continue


    return None


# ============================================================
# LOCAL FALLBACK ANSWERS
# ============================================================

def local_answer(question):

    q = question.lower().strip()


    if q in ["hi", "hello", "hey"]:

        return """
Hello! 👋

I am **Tech Mithra AI Pro**.

Ask me any question and I will help you.
"""


    if "what is ev" in q:

        return """
## 🚗 What is an EV?

EV stands for **Electric Vehicle**.

An Electric Vehicle uses an electric motor powered by a battery instead of depending completely on petrol or diesel.

### Main Parts

- Battery
- Electric Motor
- Motor Controller
- Charger
- Battery Management System

### Advantages

- Low pollution
- Low running cost
- High efficiency
- Less noise

**Examples:** Electric cars, electric bikes and electric buses.
"""


    if "what is electric vehicle" in q:

        return """
## 🚗 Electric Vehicle

An Electric Vehicle is a vehicle that uses electrical energy stored in batteries to run an electric motor.

It is an environmentally friendly alternative to conventional petrol and diesel vehicles.
"""


    if "what is python" in q:

        return """
## 🐍 What is Python?

Python is a high-level and easy-to-learn programming language.

### Applications

- Artificial Intelligence
- Machine Learning
- Web Development
- Data Science
- Automation
"""


    if "what is iot" in q:

        return """
## 🌐 What is IoT?

IoT stands for **Internet of Things**.

It is a system in which physical devices are connected to the internet to collect and exchange data.

### Examples

- Smart Homes
- Smart Watches
- Smart Agriculture
- Smart Vehicles
"""


    if "what is ethics" in q:

        return """
## What is Ethics?

Ethics refers to moral principles that guide human behaviour.

Ethics helps people understand what is right and wrong.

### Importance

- Honesty
- Responsibility
- Trust
- Professional behaviour
"""


    return f"""
## Answer

### {question}

I could not connect to the AI service at the moment.

Please check:

1. Gemini API Key
2. Internet connection
3. Streamlit Secrets configuration
4. Gemini API availability

Then try again.
"""


# ============================================================
# MAIN CHAT AI
# ============================================================

def get_ai_answer(question, image=None):

    instruction = """
You are Tech Mithra AI Pro, an intelligent AI assistant.

You can answer:

- General Questions
- Engineering Questions
- EEE Questions
- CSE Questions
- MBA Questions
- Pharmacy Questions
- Nursing Questions
- Science Questions
- Technology Questions
- Programming Questions
- Career Questions
- Educational Questions

Behave like a helpful AI assistant.

If the question is simple, answer quickly and concisely.

If the user asks for a long answer, explain clearly with:

1. Definition
2. Explanation
3. Important Points
4. Applications
5. Conclusion

If an image is provided, analyze the visible image and answer based on it.
"""


    answer = ask_ai(

        question=question,

        instruction=instruction,

        image=image

    )


    if answer:

        return answer


    return local_answer(question)


# ============================================================
# EVENT PLANNER FUNCTION
# ============================================================

def get_event_plan(event_name, event_type, audience):

    prompt = f"""
Create a complete college event plan.

Event Name:
{event_name}

Event Type:
{event_type}

Target Audience:
{audience}
"""


    instruction = """
You are an expert college event planner.

Create a useful and practical event plan.

Include:

1. Event Objective
2. Event Description
3. Target Audience
4. Event Schedule
5. Required Resources
6. Team Responsibilities
7. Budget Categories
8. Promotion Plan
9. Certificate Plan
10. Expected Outcomes

Use clear headings.
"""


    answer = ask_ai(

        question=prompt,

        instruction=instruction

    )


    if answer:

        return answer


    return f"""
# 📋 Event Plan

## Event Name

{event_name}

## Event Type

{event_type}

## Target Audience

{audience}

## Objective

To provide students with knowledge, practical learning and interactive experience.

## Suggested Schedule

### 09:00 AM
Registration

### 09:30 AM
Inauguration

### 10:00 AM
Main Technical Session

### 11:30 AM
Break

### 12:00 PM
Practical Session

### 01:30 PM
Lunch Break

### 02:30 PM
Interactive Session

### 04:00 PM
Feedback

### 04:30 PM
Certificate Distribution

## Requirements

- Venue
- Laptop
- Projector
- Internet
- Registration Desk
- Student Volunteers
- Faculty Coordinators
- Certificates

## Promotion

- WhatsApp Groups
- Instagram
- College Notice Board
- Department Announcements
"""


# ============================================================
# EVENT IMAGE PROMPT
# ============================================================

def get_event_image_prompt(event_name, event_type, audience):

    prompt = f"""
Create one professional AI image generation prompt.

Event Name:
{event_name}

Event Type:
{event_type}

Target Audience:
{audience}
"""


    instruction = """
You are an expert AI image prompt engineer.

Generate one detailed image generation prompt.

The image should be suitable for:

- College Event Poster
- Instagram Post
- Workshop Poster
- Technical Event

Use modern professional design.
Only provide the image generation prompt.
"""


    answer = ask_ai(

        question=prompt,

        instruction=instruction

    )


    if answer:

        return answer


    return f"""
Create a professional modern college event poster for "{event_name}".

Event Type: {event_type}

Target Audience: {audience}

Modern academic environment, students participating in the event,
professional technology theme, cinematic lighting,
clean composition, realistic details,
professional poster design,
space for event title and information,
high quality,
4K,
vertical composition.
"""


# ============================================================
# EXAM PREPARATION
# ============================================================

def get_exam_answer(subject, topic, answer_type):

    prompt = f"""
Subject:
{subject}

Topic:
{topic}

Required Answer Type:
{answer_type}
"""


    instruction = """
You are an expert university exam preparation assistant.

Write an accurate and exam-ready answer.

For 2 Marks:
Give a short definition and key points.

For 5 Marks:
Give definition, explanation and important points.

For 10 Marks:
Give detailed explanation with headings, points and conclusion.

For Detailed Explanation:
Explain the topic completely.

Use simple English.
"""


    answer = ask_ai(

        question=prompt,

        instruction=instruction

    )


    if answer:

        return answer


    return local_answer(topic)


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

def get_placement_guide(role):

    prompt = f"""
Target Job Role or Technology:

{role}
"""


    instruction = """
You are an expert placement mentor.

Create a placement preparation guide.

Include:

1. Required Skills
2. Important Technical Topics
3. Technical Interview Questions
4. HR Interview Questions
5. Resume Tips
6. Preparation Roadmap

Make the answer useful for college students.
"""


    answer = ask_ai(

        question=prompt,

        instruction=instruction

    )


    if answer:

        return answer


    return f"""
# 🎯 Placement Guide

## Target Role

{role}

## Required Skills

- Technical Knowledge
- Communication Skills
- Problem Solving
- Teamwork

## Important Interview Questions

1. Tell me about yourself.
2. Explain your project.
3. What are your strengths?
4. Why should we hire you?

## Preparation Plan

- Study fundamentals.
- Practice interview questions.
- Improve communication.
- Build projects.
"""


# ============================================================
# ONE TIME LOGIN CHECK
# ============================================================

try:

    saved_user = st.query_params.get("user")

    if saved_user:

        st.session_state.logged_in = True

        st.session_state.user_email = saved_user


except Exception:

    pass


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:


    st.markdown(
        """
        <div style="text-align:center; padding-top:50px;">
            <h1>🚀 Tech Mithra AI Pro</h1>
            <h3>AI Assistant for Students</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(

        [1, 2, 1]

    )


    with col2:


        st.subheader("🔐 Login")


        email = st.text_input(

            "📧 Email Address",

            key="login_email"

        )


        password = st.text_input(

            "🔑 Password",

            type="password",

            key="login_password"

        )


        if st.button(

            "🚀 Login",

            use_container_width=True

        ):


            if email.strip() and password.strip():


                st.session_state.logged_in = True

                st.session_state.user_email = email.strip()


                # Save user in URL
                try:

                    st.query_params["user"] = email.strip()

                except Exception:

                    pass


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


    st.title(APP_NAME)


    st.caption(

        f"👤 {st.session_state.user_email}"

    )


    st.divider()


    app_mode = st.radio(

        "📱 Select Feature",

        [

            "🤖 AI Chat",

            "🎪 Event Planner",

            "📚 Exam Preparation",

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


        try:

            st.query_params.clear()

        except Exception:

            pass


        st.rerun()


# ============================================================
# AI CHAT
# ============================================================

if app_mode == "🤖 AI Chat":


    st.title("🤖 AI Chat")


    st.caption(

        "Ask any question and get an AI answer."

    )


    tab1, tab2, tab3 = st.tabs(

        [

            "💬 Ask Question",

            "🖼️ Upload Photo",

            "📸 Camera"

        ]

    )


    question = ""

    selected_image = None


    # --------------------------------------------------------
    # TEXT QUESTION
    # --------------------------------------------------------

    with tab1:


        question = st.text_input(

            "Ask anything",

            placeholder="Example: What is an Electric Vehicle?"

        )


    # --------------------------------------------------------
    # UPLOAD IMAGE
    # --------------------------------------------------------

    with tab2:


        uploaded_file = st.file_uploader(

            "Upload Image",

            type=["jpg", "jpeg", "png"]

        )


        if uploaded_file:


            selected_image = Image.open(

                uploaded_file

            )


            st.image(

                selected_image,

                width=350

            )


            question = st.text_input(

                "Ask about this image",

                key="uploaded_image_question"

            )


    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    with tab3:


        camera_file = st.camera_input(

            "Take a Photo"

        )


        if camera_file:


            selected_image = Image.open(

                camera_file

            )


            st.image(

                selected_image,

                width=350

            )


            question = st.text_input(

                "Ask about this photo",

                key="camera_image_question"

            )


    # --------------------------------------------------------
    # SHOW CHAT HISTORY
    # --------------------------------------------------------

    st.divider()


    for message in st.session_state.messages:


        with st.chat_message(

            message["role"]

        ):


            st.markdown(

                message["content"]

            )


    # --------------------------------------------------------
    # GET ANSWER
    # --------------------------------------------------------

    if st.button(

        "🚀 Get Answer",

        use_container_width=True

    ):


        if question.strip():


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

                    "Thinking..."

                ):


                    answer = get_ai_answer(

                        question,

                        selected_image

                    )


                    st.markdown(answer)


            st.session_state.messages.append(

                {

                    "role": "assistant",

                    "content": answer

                }

            )


        else:


            st.warning(

                "Please enter a question."

            )


    if st.button(

        "🗑️ Clear Chat"

    ):


        st.session_state.messages = []


        st.rerun()


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":


    st.title("🎪 Event Planner")


    event_name = st.text_input(

        "Event Name",

        placeholder="Example: PLC Technical Workshop"

    )


    event_type = st.selectbox(

        "Event Type",

        [

            "Technical Workshop",

            "Seminar",

            "Guest Lecture",

            "Hackathon",

            "College Fest",

            "Cultural Event",

            "Project Exhibition",

            "Awareness Program"

        ]

    )


    audience = st.text_input(

        "Target Audience",

        placeholder="Example: Engineering Students"

    )


    col1, col2 = st.columns(2)


    with col1:


        generate_plan = st.button(

            "📋 Generate Event Plan",

            use_container_width=True

        )


    with col2:


        generate_image_prompt = st.button(

            "🎨 Generate Image Prompt",

            use_container_width=True

        )


    if generate_plan:


        if event_name.strip():


            with st.spinner(

                "Generating event plan..."

            ):


                result = get_event_plan(

                    event_name,

                    event_type,

                    audience

                )


            st.markdown(result)


        else:


            st.warning(

                "Please enter an Event Name."

            )


    if generate_image_prompt:


        if event_name.strip():


            with st.spinner(

                "Creating AI image prompt..."

            ):


                result = get_event_image_prompt(

                    event_name,

                    event_type,

                    audience

                )


            st.subheader(

                "🎨 AI Image Generation Prompt"

            )


            st.code(

                result,

                language=None

            )


        else:


            st.warning(

                "Please enter an Event Name."

            )


# ============================================================
# EXAM PREPARATION
# ============================================================

elif app_mode == "📚 Exam Preparation":


    st.title("📚 Exam Preparation")


    subject = st.text_input(

        "Subject Name",

        placeholder="Example: Electrical Machines"

    )


    topic = st.text_input(

        "Topic",

        placeholder="Example: Transformer"

    )


    answer_type = st.selectbox(

        "Answer Type",

        [

            "2 Marks Answer",

            "5 Marks Answer",

            "10 Marks Answer",

            "Detailed Explanation"

        ]

    )


    if st.button(

        "📝 Generate Exam Answer",

        use_container_width=True

    ):


        if subject.strip() and topic.strip():


            with st.spinner(

                "Preparing answer..."

            ):


                result = get_exam_answer(

                    subject,

                    topic,

                    answer_type

                )


            st.markdown(result)


        else:


            st.warning(

                "Please enter Subject and Topic."

            )


# ============================================================
# PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":


    st.title("💼 Placement Preparation")


    role = st.text_input(

        "Target Job Role / Technology",

        placeholder="Example: Electrical Engineer"

    )


    if st.button(

        "🎯 Generate Placement Guide",

        use_container_width=True

    ):


        if role.strip():


            with st.spinner(

                "Preparing placement guide..."

            ):


                result = get_placement_guide(

                    role

                )


            st.markdown(result)


        else:


            st.warning(

                "Please enter Job Role or Technology."

            )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.markdown(

    """
    <center>

    <h3>🚀 Tech Mithra AI Pro</h3>

    <p>
    AI Chat |
    Event Planner |
    Exam Preparation |
    Placement Preparation
    </p>

    </center>
    """,

    unsafe_allow_html=True

)
