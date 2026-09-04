import streamlit as st
import os
import base64
from google import genai
from PIL import Image


# ============================================================
# TECH MITHRA AI PRO - COMPLETE APP
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "🚀 Tech Mithra AI Pro"

# ONLY NEW MODELS - NO gemini-2.5-flash
TEXT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]

IMAGE_MODEL = "gemini-3.1-flash-image"


# ============================================================
# GET API KEY
# ============================================================

def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY", "")


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

def get_client():
    api_key = get_api_key()

    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# ============================================================
# GENERATE TEXT WITH MODEL FALLBACK
# ============================================================

def ask_ai(question, instruction="You are a helpful AI assistant."):

    client = get_client()

    if client is None:
        return (
            "❌ API Key not found.\n\n"
            "Add GEMINI_API_KEY in Streamlit Secrets."
        )

    errors = []

    full_prompt = f"""
{instruction}

User Question:
{question}
"""

    for model_name in TEXT_MODELS:

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )

            if response and response.text:
                return response.text

        except Exception as e:
            errors.append(
                f"{model_name}: {str(e)}"
            )

    return (
        "❌ AI service is temporarily unavailable.\n\n"
        "Models tried:\n"
        + "\n".join(errors)
    )


# ============================================================
# ANALYZE IMAGE
# ============================================================

def analyze_image(question, image):

    client = get_client()

    if client is None:
        return "❌ API Key not found."

    errors = []

    for model_name in TEXT_MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=[
                    question,
                    image
                ]
            )

            if response and response.text:
                return response.text

        except Exception as e:
            errors.append(
                f"{model_name}: {str(e)}"
            )

    return (
        "❌ Image analysis failed.\n\n"
        + "\n".join(errors)
    )


# ============================================================
# GENERATE IMAGE
# ============================================================

def generate_ai_image(prompt):

    client = get_client()

    if client is None:
        return None, "API Key not found."

    try:

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt
        )

        for part in response.parts:

            if part.inline_data is not None:

                image_data = part.inline_data.data

                if isinstance(image_data, str):
                    image_data = base64.b64decode(
                        image_data
                    )

                return image_data, None

            try:
                image = part.as_image()

                if image is not None:

                    from io import BytesIO

                    buffer = BytesIO()

                    image.save(
                        buffer,
                        format="PNG"
                    )

                    return (
                        buffer.getvalue(),
                        None
                    )

            except Exception:
                pass

        return None, "No image was returned."

    except Exception as e:

        return None, str(e)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "app_name" not in st.session_state:
    st.session_state.app_name = APP_NAME


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("🔐 Tech Mithra AI Pro")

    st.subheader("Login")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        email = st.text_input(
            "📧 Email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if email and password:

                st.session_state.logged_in = True
                st.session_state.user_email = email

                st.rerun()

            else:

                st.error(
                    "Enter Email and Password."
                )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI Pro")

    st.success(
        f"Logged in as:\n\n"
        f"{st.session_state.user_email}"
    )

    st.divider()

    education_stream = st.selectbox(
        "📚 Select Stream",
        [
            "Engineering",
            "Pharmacy",
            "Nursing",
            "MBA",
            "General Learning"
        ]
    )

    st.divider()

    app_mode = st.radio(
        "Select Feature",
        [
            "🤖 Project & Lab Guide",
            "🎪 Event Planner",
            "📚 Exam Preparation",
            "💼 Placement Preparation"
        ]
    )

    st.divider()

    st.caption("Active AI Models")

    st.code("Text: gemini-3.8-flash")

    st.code(
        "Image: gemini-3.1-flash-image"
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


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

if app_mode == "🤖 Project & Lab Guide":

    st.title("🤖 Project & Lab Guide")

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

            instruction = f"""
You are Tech Mithra AI Pro.

You are an expert academic and technical AI assistant.

Student Stream:
{education_stream}

Rules:

1. Answer accurately.
2. Start with a direct definition.
3. Use simple English.
4. Use headings.
5. Use bullet points when useful.
6. Give exam-friendly answers.
7. Explain technical concepts clearly.
8. For programming questions provide correct code.
"""

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "🤖 AI is thinking..."
                ):

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
            "🖼️ Upload Question Image"
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
                use_container_width=True
            )

            question = st.text_input(
                "Question about this image",
                placeholder=(
                    "Example: Give the correct answer"
                )
            )

            if st.button(
                "🤖 Analyze Image"
            ):

                if not question:

                    question = """
Analyze this image carefully.
Read any question present in the image.
Give the correct answer with explanation.
"""

                with st.spinner(
                    "Analyzing image..."
                ):

                    result = analyze_image(
                        question,
                        image
                    )

                    st.markdown(result)


    # --------------------------------------------------------
    # CAMERA PHOTO
    # --------------------------------------------------------

    with tab3:

        camera_photo = st.camera_input(
            "Take a photo"
        )

        if camera_photo:

            image = Image.open(
                camera_photo
            )

            st.image(
                image,
                use_container_width=True
            )

            question = st.text_input(
                "Ask about this photo",
                placeholder="Solve this question"
            )

            if st.button(
                "🤖 Analyze Camera Photo"
            ):

                if not question:

                    question = """
Read the question from this image.
Give the correct answer.
Explain clearly.
"""

                with st.spinner(
                    "AI is analyzing..."
                ):

                    result = analyze_image(
                        question,
                        image
                    )

                    st.markdown(result)


# ============================================================
# EVENT PLANNER
# ============================================================

elif app_mode == "🎪 Event Planner":

    import time

    st.header(f"🎪 {education_stream.split()[1]} Event & Workshop Planner")

    st.success(
        "ఈ ఆప్షన్ ద్వారా మీరు మీ కాలేజీ ఈవెంట్స్, సెమినార్లు మరియు వర్క్‌షాప్‌ల కోసం ప్లానింగ్ చేసుకోవచ్చు!"
    )

    event_topic = st.text_input(
        "Enter Event Name / Topic:",
        placeholder="Example: PLC Workshop, Technical Fest, AI Seminar"
    )

    event_type = st.selectbox(
        "Select Event Type:",
        [
            "Technical Workshop",
            "Seminar",
            "College Event",
            "Technical Fest",
            "Hackathon",
            "Guest Lecture",
            "Project Expo",
            "Cultural Event"
        ]
    )

    event_duration = st.selectbox(
        "Event Duration:",
        [
            "Half Day",
            "1 Day",
            "2 Days",
            "3 Days"
        ]
    )

    expected_students = st.number_input(
        "Expected Participants:",
        min_value=10,
        max_value=10000,
        value=100
    )


    # ------------------------------------------------
    # EVENT PLAN GENERATION FUNCTION
    # ------------------------------------------------
    def generate_event_plan(topic, event_type, duration, students):

        prompt = f"""
You are an expert college event planner.

Create a complete professional event plan.

Event Name: {topic}
Event Type: {event_type}
Duration: {duration}
Expected Participants: {students}

Give the answer in this format:

1. Event Title
2. Event Objective
3. Target Audience
4. Event Description
5. Complete Schedule / Timeline
6. Required Resources
7. Organizing Committee
8. Budget Categories
9. Promotion Plan
10. Registration Process
11. Certificate Plan
12. Expected Outcomes
13. Safety and Management Plan
14. Social Media Caption
15. Poster / Banner Text

Use simple English and clear headings.
Make the answer suitable for a college event.
"""

        # Your existing Gemini client/function is used here
        # This function tries multiple times so temporary 503 errors
        # do not immediately show to the user.

        models_to_try = [
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.6-flash"
        ]

        errors = []

        for model_name in models_to_try:

            for attempt in range(3):

                try:

                    # ------------------------------------------------
                    # IMPORTANT:
                    # Replace ONLY this call if your existing Gemini
                    # code uses a different client syntax.
                    # ------------------------------------------------

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )

                    if response and response.text:
                        return response.text

                except Exception as e:

                    errors.append(
                        f"{model_name} attempt {attempt + 1}: {str(e)}"
                    )

                    # Wait before retrying
                    time.sleep(2 * (attempt + 1))


        # ------------------------------------------------
        # LOCAL FALLBACK
        # If Gemini is temporarily unavailable,
        # the app STILL gives a complete Event Plan.
        # ------------------------------------------------

        return f"""
# 🎪 EVENT PLAN: {topic}

## 1. Event Title

**{topic}**

**Event Type:** {event_type}  
**Duration:** {duration}  
**Expected Participants:** {students}

---

## 2. Event Objective

The main objective of this event is to provide students with practical knowledge, technical exposure, teamwork experience, communication skills, and awareness about modern technologies.

---

## 3. Target Audience

- Engineering Students
- Faculty Members
- Technical Enthusiasts
- Project Students
- Industry Experts
- College Clubs

---

## 4. Event Description

The **{topic}** event is designed as an interactive academic and technical program.

The event will include:

- Introduction Session
- Expert Lecture
- Technical Demonstration
- Practical Activity
- Student Interaction
- Question and Answer Session
- Feedback Collection
- Certificate Distribution

---

## 5. Suggested Event Schedule

### Opening Session

- Registration
- Welcome Speech
- Introduction of Guests
- Event Overview

### Technical Session

- Expert Presentation
- Topic Explanation
- Live Demonstration
- Practical Examples

### Interactive Session

- Student Questions
- Group Discussion
- Hands-on Activity

### Closing Session

- Feedback Collection
- Vote of Thanks
- Certificate Distribution
- Photography Session

---

## 6. Required Resources

- Seminar Hall or Classroom
- Projector
- Laptop
- Internet Connection
- Microphone
- Speaker System
- Registration Desk
- Certificates
- Event Banners

---

## 7. Organizing Committee

### Faculty Coordinator

Responsible for overall supervision.

### Student Coordinator

Responsible for student communication and event coordination.

### Technical Team

Responsible for:

- Laptop Setup
- Projector
- Internet
- Demonstrations

### Registration Team

Responsible for participant registration.

### Media Team

Responsible for:

- Photography
- Videography
- Social Media Promotion

---

## 8. Budget Categories

Possible expenses include:

- Guest Honorarium
- Certificates
- Printing
- Banners
- Refreshments
- Technical Equipment
- Photography

---

## 9. Promotion Plan

Promote the event using:

- College WhatsApp Groups
- Instagram
- Posters
- College Notice Board
- Department Groups

---

## 10. Registration Process

1. Create Registration Form
2. Collect Student Details
3. Confirm Registration
4. Prepare Participant List
5. Verify Attendance

---

## 11. Certificate Plan

Certificates can be provided to:

- Participants
- Organizing Team
- Faculty Coordinators
- Guest Speakers

---

## 12. Expected Outcomes

Students will gain:

- Practical Knowledge
- Technical Skills
- Communication Skills
- Teamwork Experience
- Industry Awareness

---

## 13. Safety and Management Plan

- Maintain proper seating arrangements.
- Keep technical equipment secure.
- Manage participant attendance.
- Ensure proper electrical safety.
- Keep emergency contact information available.

---

## 14. Social Media Caption

🚀 **{topic}**

Join us for an exciting **{event_type}**!

📚 Learn  
💡 Explore  
🚀 Innovate  
🤝 Connect  

Don't miss this opportunity!

#CollegeEvent #Workshop #Technology #Students #Innovation

---

## 15. Poster Text

🎪 **{topic}**

Organized By  
**{education_stream.split()[1]} Department**

📅 Duration: {duration}

👥 Participants: {students}+

Learn • Explore • Innovate

"""



    # ------------------------------------------------
    # GENERATE EVENT PLAN BUTTON
    # ------------------------------------------------
    if st.button("📋 Generate Complete Event Plan", use_container_width=True):

        if not event_topic.strip():

            st.warning("Please enter an Event Name / Topic.")

        else:

            with st.spinner(
                "Generating your complete event plan... Please wait ⏳"
            ):

                event_plan = generate_event_plan(
                    event_topic,
                    event_type,
                    event_duration,
                    expected_students
                )

                st.session_state["generated_event_plan"] = event_plan

            st.success("✅ Event Plan Generated Successfully!")

            st.markdown(
                st.session_state["generated_event_plan"]
            )



    # ------------------------------------------------
    # PHOTO / IMAGE PROMPT GENERATOR
    # ------------------------------------------------

    st.divider()

    st.subheader("🎨 Event Photo / Poster Prompt Generator")

    image_style = st.selectbox(
        "Select Image Style:",
        [
            "Professional College Poster",
            "Cinematic Event Photo",
            "Modern Technical Poster",
            "Professional Workshop Banner",
            "Instagram Event Poster"
        ]
    )


    if st.button(
        "🎨 Generate Photo Prompt",
        use_container_width=True
    ):

        if not event_topic.strip():

            st.warning(
                "Please enter the Event Name first."
            )

        else:

            photo_prompt = f"""
Create a {image_style} for a college event.

Event Name: {event_topic}
Event Type: {event_type}

Show a modern academic and professional atmosphere.

Include:

- College students
- Modern technology
- Professional event environment
- Stage or workshop setup
- Screens and technical equipment
- Clean academic design
- High quality lighting
- Professional composition

Style: {image_style}

Make the design attractive for a college event poster.
High quality, realistic, professional, detailed.
"""

            st.session_state["event_photo_prompt"] = photo_prompt

            st.success("✅ Photo Generation Prompt Ready!")

            st.code(
                photo_prompt,
                language="text"
            )



    # ------------------------------------------------
    # TEXT TO IMAGE PROMPT SECTION
    # ------------------------------------------------

    st.divider()

    st.subheader("🖼️ Text to Image Prompt")

    custom_image_text = st.text_area(
        "Describe the event image you want:",
        placeholder="Example: Students attending an AI workshop in a modern college auditorium"
    )


    if st.button(
        "✨ Create Image Prompt",
        use_container_width=True
    ):

        if not custom_image_text.strip():

            st.warning(
                "Please describe the image you want."
            )

        else:

            final_image_prompt = f"""
Create a high-quality realistic professional image.

Main Description:
{custom_image_text}

Related Event:
{event_topic}

Event Type:
{event_type}

Image Requirements:

- Professional college environment
- Realistic students
- Modern technology
- Natural lighting
- High quality
- Detailed composition
- Professional photography
- Event atmosphere
- Suitable for poster and social media

Do not include unwanted text.
"""

            st.success(
                "✅ Your Text-to-Image Prompt is Ready!"
            )

            st.code(
                final_image_prompt,
                language="text"
            )


# ============================================================
# EXAM PREPARATION
# ============================================================

elif app_mode == "📚 Exam Preparation":

    st.title(
        "📚 AI Exam Preparation"
    )

    subject = st.text_input(
        "Subject Name"
    )

    topic = st.text_input(
        "Topic / Chapter"
    )

    answer_type = st.selectbox(
        "Select Type",
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
        "📝 Generate"
    ):

        if not subject:

            st.warning(
                "Enter Subject Name."
            )

        else:

            prompt = f"""
Create exam preparation material.

Stream:
{education_stream}

Subject:
{subject}

Topic:
{topic}

Type:
{answer_type}

Make the answer accurate,
easy to understand,
and exam-friendly.
"""

            with st.spinner(
                "Preparing..."
            ):

                result = ask_ai(
                    prompt,
                    "You are an expert academic tutor."
                )

                st.markdown(result)


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif app_mode == "💼 Placement Preparation":

    st.title(
        "💼 AI Placement Preparation"
    )

    company = st.text_input(
        "Target Company"
    )

    role = st.text_input(
        "Target Job Role"
    )

    preparation = st.selectbox(
        "Preparation Type",
        [
            "Technical Interview",
            "HR Interview",
            "Aptitude",
            "Resume",
            "Project Explanation",
            "Complete Placement Roadmap"
        ]
    )

    if st.button(
        "🚀 Generate Placement Guide"
    ):

        if not role:

            st.warning(
                "Enter Job Role."
            )

        else:

            prompt = f"""
Create a placement preparation guide.

Student Stream:
{education_stream}

Target Company:
{company}

Job Role:
{role}

Preparation Type:
{preparation}

Include relevant questions,
answers,
important skills,
and a preparation roadmap.
"""

            with st.spinner(
                "Preparing placement guide..."
            ):

                result = ask_ai(
                    prompt,
                    "You are an expert career mentor."
                )

                st.markdown(result)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <h2>🚀 Tech Mithra AI Pro</h2>
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
