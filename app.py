# ============================================================
# TECH MITHRA AI PRO - COMPLETE app.py
#
# Install requirements:
# pip install streamlit google-genai pillow
#
# Streamlit Secrets:
# GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"
#
# Run:
# streamlit run app.py
# ============================================================

import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import time
import textwrap


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

APP_NAME = "🚀 Tech Mithra AI Pro"

STREAMS = [
    "⚡ Engineering (B.Tech / EEE / CSE)",
    "💊 Pharmacy (B.Pharm / Pharm.D)",
    "🩺 Nursing (B.Sc / GNM)",
    "📈 MBA (Management)"
]

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]


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
    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# ============================================================
# AI RESPONSE FUNCTION
# FAST RESPONSE + MODEL FALLBACK
# ============================================================

def ask_ai(prompt, system_instruction="", image=None):

    api_key = get_api_key()

    if not api_key:
        return None

    client = get_client(api_key)

    if client is None:
        return None

    final_prompt = f"""
{system_instruction}

User Question:
{prompt}

Give a clear and useful answer.
Use simple English.
Do not mention API errors.
"""

    if image is not None:
        contents = [final_prompt, image]
    else:
        contents = final_prompt

    for model_name in MODELS:

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )

            if response and getattr(response, "text", None):
                return response.text.strip()

        except Exception:
            continue

    return None


# ============================================================
# LOCAL FALLBACK ANSWER
# ============================================================

def local_answer(question, stream_name):

    question_lower = question.lower().strip()

    definitions = {

        "what is python": """
### Python

Python is a high-level and easy-to-learn programming language.

#### Important Points:
- Python has simple syntax.
- It is easy for beginners.
- It is used for web development.
- It is used in Artificial Intelligence.
- It is used for data science.
- It is used for automation.

#### Applications:
Python is used in AI, machine learning, web applications, software development and data analysis.
""",

        "what is iot": """
### Internet of Things (IoT)

IoT stands for **Internet of Things**.

It is a system in which physical devices are connected to the internet to collect, exchange and process data.

#### Examples:
- Smart homes
- Smart watches
- Smart agriculture
- Smart vehicles
- Industrial automation

#### Conclusion:
IoT helps devices communicate with each other through the internet and improves automation.
""",

        "what is ethics": """
### Ethics

Ethics refers to the moral principles that guide human behaviour.

It helps people understand what is right and wrong.

#### Importance of Ethics:
- Promotes honesty
- Builds trust
- Encourages responsibility
- Improves professional behaviour
- Helps in decision making

#### Conclusion:
Ethics is important for maintaining responsible and respectful behaviour in personal and professional life.
""",

        "what is ev": """
### Electric Vehicle (EV)

An Electric Vehicle is a vehicle that uses an electric motor for propulsion.

Instead of depending completely on petrol or diesel, an EV uses electrical energy stored in batteries.

#### Main Components:
- Battery
- Electric motor
- Motor controller
- Charger
- Battery Management System

#### Advantages:
- Low pollution
- Low running cost
- High efficiency
- Quiet operation

#### Conclusion:
Electric Vehicles are an important technology for sustainable transportation.
"""
    }

    for key, value in definitions.items():
        if key in question_lower:
            return value

    return f"""
### Answer: {question}

**Definition:**  
{question} is an important topic related to the {stream_name} field.

### Important Points

1. Understand the basic definition and purpose of the topic.
2. Study its important components and working principle.
3. Learn the practical applications.
4. Understand its advantages and limitations.
5. Use examples for better understanding.

### Applications

This topic can be useful in education, industry, research, technology and professional applications.

### Conclusion

For exam preparation, understand the definition, working principle, important components and practical applications of **{question}**.
"""


# ============================================================
# PROJECT AND LAB GUIDE ANSWER
# ============================================================

def project_answer(stream_name, question, image=None):

    instruction = f"""
You are Tech Mithra AI Pro.

You are an expert academic assistant for {stream_name} students.

Answer accurately and clearly.

If the question is small:
Give a direct answer quickly.

If the question is for exams:
Use:
1. Definition
2. Explanation
3. Important Points
4. Applications
5. Conclusion

If an image is provided:
Analyze the image and answer the student's question based on the visible content.

Use simple English suitable for college students.
"""

    result = ask_ai(
        prompt=question,
        system_instruction=instruction,
        image=image
    )

    if result:
        return result

    return local_answer(question, stream_name)


# ============================================================
# EXAM ANSWER
# ============================================================

def exam_answer(subject, topic, answer_type):

    prompt = f"""
Subject: {subject}
Topic: {topic}
Required Answer Type: {answer_type}

Prepare an exam-ready academic answer.
"""

    instruction = """
You are an expert university exam preparation assistant.

Write an accurate answer.

For 2 Marks:
Give a short definition and key point.

For 5 Marks:
Give definition, explanation and important points.

For 10 Marks:
Give detailed explanation, headings, applications and conclusion.

Use simple English.
"""

    result = ask_ai(
        prompt=prompt,
        system_instruction=instruction
    )

    if result:
        return result

    if answer_type == "2 Marks Answer":
        return f"""
### {topic}

**Definition:**  
{topic} is an important concept in the subject **{subject}**.

It is studied to understand its basic principles, functions and applications.
"""

    elif answer_type == "5 Marks Answer":
        return f"""
## {topic}

### Definition
{topic} is an important concept in **{subject}**.

### Explanation
It involves important principles, functions and practical applications.

### Important Points
1. Basic concept and purpose.
2. Main components or elements.
3. Working principle.
4. Advantages.
5. Applications.

### Conclusion
Understanding {topic} helps students apply theoretical knowledge in practical situations.
"""

    else:
        return f"""
# {topic}

## Introduction
{topic} is an important topic in **{subject}**.

## Definition
It refers to the principles and methods associated with the topic.

## Detailed Explanation
The topic includes fundamental concepts, important components, working methods and practical applications.

## Important Points
1. Basic principles.
2. Components.
3. Working procedure.
4. Advantages.
5. Limitations.
6. Applications.

## Applications
The concept is useful in education, research, industry and professional applications.

## Conclusion
A proper understanding of {topic} helps students develop theoretical and practical knowledge.
"""


# ============================================================
# EVENT PLANNER
# ============================================================

def local_event_plan(event_name, event_type, audience):

    return f"""
# 📋 Event Plan: {event_name}

## 🎯 Event Type
{event_type}

## 👥 Target Audience
{audience}

## 🎯 Objective
To provide knowledge, practical exposure and interactive learning opportunities for participants.

## 🕘 Suggested Schedule

### 9:00 AM – Registration
Participant registration and welcome.

### 9:30 AM – Inauguration
Welcome speech and introduction.

### 10:00 AM – Technical Session
Introduction to the main event topic.

### 11:30 AM – Break

### 12:00 PM – Practical Session
Hands-on learning and demonstration.

### 1:30 PM – Lunch Break

### 2:30 PM – Interactive Session
Student activities, questions and discussion.

### 4:00 PM – Feedback
Collect participant feedback.

### 4:30 PM – Certificate Distribution

## 📌 Requirements
- Venue
- Projector
- Internet connection
- Registration desk
- Faculty coordinators
- Student volunteers
- Certificates

## 📢 Promotion
Promote the event using:
- College WhatsApp groups
- Posters
- Social media
- Department announcements

## 🏁 Conclusion
The event will help participants improve practical knowledge, communication and technical skills.
"""


def generate_event_plan(event_name, event_type, audience):

    prompt = f"""
Event Name: {event_name}
Event Type: {event_type}
Target Audience: {audience}

Create a complete college event plan.
"""

    instruction = """
You are an expert college event planner.

Create a practical event plan.

Include:
- Event objective
- Target audience
- Detailed schedule
- Required resources
- Team responsibilities
- Budget categories
- Promotion plan
- Certificate plan
- Feedback process

Use clear headings and bullet points.
"""

    result = ask_ai(
        prompt=prompt,
        system_instruction=instruction
    )

    if result:
        return result

    return local_event_plan(event_name, event_type, audience)


# ============================================================
# EVENT IMAGE PROMPT
# ============================================================

def local_event_image_prompt(event_name, event_type, audience):

    return f"""
Create a professional and modern college event poster for "{event_name}".

Event Type: {event_type}
Target Audience: {audience}

Design style:
Modern educational technology poster, professional college atmosphere,
students participating in a technical event, clean typography space,
cinematic lighting, realistic details, high quality,
professional event branding, 4K quality,
vertical poster composition.
"""


# ============================================================
# CREATE LOCAL EVENT POSTER
# ============================================================

def create_event_poster(event_name, event_type, audience):

    width = 1080
    height = 1350

    image = Image.new("RGB", (width, height), (25, 35, 55))

    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
        sub_font = ImageFont.truetype("DejaVuSans.ttf", 38)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 30)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    draw.rectangle(
        [(0, 0), (width, 250)],
        fill=(35, 75, 140)
    )

    draw.text(
        (70, 70),
        "TECH MITHRA EVENT",
        font=small_font,
        fill="white"
    )

    wrapped_title = textwrap.fill(event_name.upper(), width=20)

    draw.multiline_text(
        (70, 320),
        wrapped_title,
        font=title_font,
        fill="white",
        spacing=15
    )

    draw.text(
        (70, 750),
        f"EVENT TYPE: {event_type}",
        font=sub_font,
        fill=(180, 220, 255)
    )

    draw.text(
        (70, 850),
        "TARGET AUDIENCE:",
        font=small_font,
        fill=(255, 210, 120)
    )

    audience_text = textwrap.fill(audience, width=40)

    draw.multiline_text(
        (70, 900),
        audience_text,
        font=sub_font,
        fill="white",
        spacing=10
    )

    draw.text(
        (70, 1180),
        "LEARN • CONNECT • INNOVATE",
        font=small_font,
        fill=(120, 230, 180)
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer


# ============================================================
# PLACEMENT PREP
# ============================================================

def placement_answer(role):

    prompt = f"""
Target Job Role or Technology: {role}

Create a placement preparation guide.
"""

    instruction = """
You are an expert placement preparation mentor.

Create a practical placement roadmap.

Include:
1. Required technical skills
2. Important concepts
3. Interview questions
4. HR questions
5. Resume tips
6. Preparation roadmap

Use simple English.
"""

    result = ask_ai(
        prompt=prompt,
        system_instruction=instruction
    )

    if result:
        return result

    return f"""
# 🎯 Placement Preparation: {role}

## Required Skills
- Basic technical knowledge
- Problem solving
- Communication
- Teamwork
- Project knowledge

## Important Interview Questions
1. Tell me about yourself.
2. Explain your project.
3. What are your strengths?
4. What technical skills do you have?
5. Why should we hire you?

## Preparation Plan
- Study fundamentals.
- Practice interview questions.
- Improve communication.
- Prepare projects.
- Create a professional resume.
"""


# ============================================================
# LOGIN INITIALIZATION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# RESTORE LOGIN FROM URL
# ============================================================

try:
    saved_user = st.query_params.get("user", "")

    if saved_user and not st.session_state.logged_in:
        st.session_state.logged_in = True
        st.session_state.user_email = saved_user

except Exception:
    pass


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("🚀 Tech Mithra AI Pro")

    st.subheader("🔐 Login")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email = st.text_input(
            "📧 Email Address"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if email.strip() and password.strip():

                st.session_state.logged_in = True
                st.session_state.user_email = email.strip()

                st.query_params["user"] = email.strip()

                st.rerun()

            else:

                st.error(
                    "Please enter email and password."
                )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(APP_NAME)

    st.success(
        f"Logged in as: {st.session_state.user_email}"
    )

    st.divider()

    education_stream = st.selectbox(
        "📚 Select Stream",
        STREAMS
    )

    st.divider()

    app_mode = st.radio(
        "Select Feature",
        [
            "🤖 Project & Lab Guide",
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
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.title("🤖 Project & Lab Guide")

    st.caption(
        "Ask any academic, technical or general question."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Text Chat",
            "🖼️ Upload Photo",
            "📸 Camera Photo"
        ]
    )

    uploaded_image = None
    user_question = ""

    with tab1:

        user_question = st.text_input(
            "Ask your question",
            placeholder="Example: What is IoT?"
        )

    with tab2:

        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:

            uploaded_image = Image.open(uploaded_file)

            st.image(
                uploaded_image,
                width=350
            )

            user_question = st.text_input(
                "Ask question about this image",
                key="upload_question"
            )

    with tab3:

        camera_file = st.camera_input(
            "Take a photo"
        )

        if camera_file:

            uploaded_image = Image.open(camera_file)

            st.image(
                uploaded_image,
                width=350
            )

            user_question = st.text_input(
                "Ask question about this photo",
                key="camera_question"
            )

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    if st.button(
        "🚀 Get Answer",
        use_container_width=True
    ):

        if user_question.strip():

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_question
                }
            )

            with st.chat_message("user"):

                st.markdown(user_question)

            with st.chat_message("assistant"):

                with st.spinner(
                    "Preparing answer..."
                ):

                    answer = project_answer(
                        education_stream,
                        user_question,
                        uploaded_image
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

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    st.title("🎪 Event Planner")

    st.caption(
        "Generate event plans, image prompts and event posters."
    )

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
            "Cultural Event",
            "College Fest",
            "Project Exhibition",
            "Awareness Program"
        ]
    )

    target_audience = st.text_input(
        "Target Audience",
        placeholder="Example: Final Year EEE Students"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        generate_plan = st.button(
            "📋 Generate Event Plan",
            use_container_width=True
        )

    with col2:

        generate_prompt = st.button(
            "🎨 Generate Image Prompt",
            use_container_width=True
        )

    with col3:

        generate_poster = st.button(
            "🖼️ Generate Event Poster",
            use_container_width=True
        )

    if generate_plan:

        if event_name.strip():

            with st.spinner(
                "Generating event plan..."
            ):

                plan = generate_event_plan(
                    event_name,
                    event_type,
                    target_audience
                )

            st.markdown(plan)

        else:

            st.warning(
                "Please enter Event Name."
            )

    if generate_prompt:

        if event_name.strip():

            prompt = f"""
Create a professional event poster image.

Event Name: {event_name}
Event Type: {event_type}
Target Audience: {target_audience}

Style:
Modern, professional, realistic,
college event atmosphere,
high quality,
cinematic lighting,
clean composition,
space for event information,
4K quality,
vertical poster.
"""

            ai_prompt = ask_ai(
                prompt=prompt,
                system_instruction="""
You are an expert AI image prompt engineer.

Create one detailed professional image generation prompt.
Only give the final prompt.
"""
            )

            if not ai_prompt:
                ai_prompt = local_event_image_prompt(
                    event_name,
                    event_type,
                    target_audience
                )

            st.subheader(
                "🎨 AI Image Generation Prompt"
            )

            st.code(
                ai_prompt,
                language=None
            )

        else:

            st.warning(
                "Please enter Event Name."
            )

    if generate_poster:

        if event_name.strip():

            poster = create_event_poster(
                event_name,
                event_type,
                target_audience
            )

            st.subheader(
                "🖼️ Generated Event Poster"
            )

            st.image(
                poster,
                use_container_width=True
            )

            st.download_button(
                "⬇️ Download Poster",
                data=poster,
                file_name="tech_mithra_event_poster.png",
                mime="image/png"
            )

        else:

            st.warning(
                "Please enter Event Name."
            )


# ============================================================
# EXAM PREPARATION
# ============================================================

elif app_mode == "📚 Exam Preparation":

    st.title("📚 Exam Preparation")

    subject_name = st.text_input(
        "Subject Name",
        placeholder="Example: Fundamentals of Management"
    )

    topic_name = st.text_input(
        "Topic / Chapter",
        placeholder="Example: Levels of Management"
    )

    answer_type = st.selectbox(
        "Select Type",
        [
            "2 Marks Answer",
            "5 Marks Answer",
            "10 Marks Answer"
        ]
    )

    if st.button(
        "📝 Generate Answer",
        use_container_width=True
    ):

        if subject_name.strip() and topic_name.strip():

            with st.spinner(
                "Preparing exam answer..."
            ):

                answer = exam_answer(
                    subject_name,
                    topic_name,
                    answer_type
                )

            st.markdown(answer)

        else:

            st.warning(
                "Please enter Subject Name and Topic."
            )


# ============================================================
# PLACEMENT PREP
# ============================================================

elif app_mode == "💼 Placement Prep":

    st.title("💼 Placement & Career Preparation")

    role_name = st.text_input(
        "Target Job Role / Technology",
        placeholder="Example: Electrical Engineer"
    )

    if st.button(
        "🎯 Generate Placement Guide",
        use_container_width=True
    ):

        if role_name.strip():

            with st.spinner(
                "Preparing placement guide..."
            ):

                answer = placement_answer(
                    role_name
                )

            st.markdown(answer)

        else:

            st.warning(
                "Please enter a Job Role or Technology."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
<center>
<h3>🚀 Tech Mithra AI Pro</h3>
<p>AI Academic Assistant | Project Guide | Event Planner | Exam Preparation | Placement Preparation</p>
</center>
""",
    unsafe_allow_html=True
)
