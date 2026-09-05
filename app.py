import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from datetime import datetime
import time

# =========================================================
# TECH MITHRA AI PRO
# History + Admin Settings
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro 🎓",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# CONFIG
# =========================================================

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

TEXT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
]

IMAGE_MODEL = "gemini-3.1-flash-image"

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "app_title" not in st.session_state:
    st.session_state.app_title = "Tech Mithra AI Pro 🎓"

if "welcome_message" not in st.session_state:
    st.session_state.welcome_message = (
        "Welcome to Tech Mithra AI Pro 🚀"
    )

if "admin_email" not in st.session_state:
    st.session_state.admin_email = ADMIN_EMAIL

if "selected_model" not in st.session_state:
    st.session_state.selected_model = TEXT_MODELS[0]

if "ai_enabled" not in st.session_state:
    st.session_state.ai_enabled = True


# =========================================================
# API KEY
# =========================================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


# =========================================================
# GEMINI CLIENT
# =========================================================

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


# =========================================================
# HISTORY
# =========================================================

def add_history(mode, question, answer):
    if not question or not answer:
        return

    st.session_state.history.append({
        "time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        "mode": mode,
        "question": str(question),
        "answer": str(answer)
    })


def show_history():
    st.title("📜 History")

    history = st.session_state.history

    if not history:
        st.info("No history yet. Your AI conversations will appear here.")
        return

    col1, col2 = st.columns([4, 1])

    with col1:
        st.success(f"Total conversations: {len(history)}")

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    st.divider()

    # Newest first
    for index, item in enumerate(reversed(history)):
        question_short = item["question"].replace("\n", " ")[:70]

        with st.expander(
            f"🕒 {item['time']}  |  {item['mode']}  |  {question_short}"
        ):
            st.markdown("### ❓ Question")
            st.write(item["question"])

            st.markdown("### 🤖 AI Answer")
            st.markdown(item["answer"])

            st.caption(item["time"])


# =========================================================
# AI RESPONSE
# =========================================================

def get_ai_response(question, mode="General", image=None):

    api_key = get_api_key()

    if not api_key:
        return (
            "⚠️ Gemini API key not found.\n\n"
            "Please add `GEMINI_API_KEY` in Streamlit Secrets."
        )

    try:
        client = get_client(api_key)

        if mode == "Project & Lab Guide":
            system_prompt = """
You are Tech Mithra AI, an expert engineering project and laboratory guide.

Give:
1. Simple explanation
2. Components/tools
3. Working principle
4. Step-by-step procedure
5. Circuit/block diagram description when useful
6. Expected result
7. Applications
8. Viva questions

Keep the answer student-friendly.
"""

        elif mode == "Event Planner":
            system_prompt = """
You are an expert college event planner.

Create:
1. Event idea
2. Objective
3. Target audience
4. Venue
5. Required materials
6. Team responsibilities
7. Schedule
8. Budget idea
9. Promotion plan
10. Safety/management points

Keep it practical and easy for students.
"""

        elif mode == "Exam Hacker":
            system_prompt = """
You are an expert exam preparation assistant.

Give:
1. Direct answer
2. Important points
3. Easy explanation
4. Examples if useful
5. Exam-ready format

For 2 marks give a short answer.
For 5 marks give a medium answer.
For 10 marks give a detailed answer.
"""

        elif mode == "Placement Prep":
            system_prompt = """
You are a placement preparation mentor.

Help students with:
- Technical interview questions
- HR questions
- Aptitude
- Communication
- Resume preparation
- Company preparation
- Mock interview questions

Give simple and practical answers.
"""

        else:
            system_prompt = """
You are Tech Mithra AI, a helpful student assistant.

Answer clearly and accurately.
Keep answers simple unless the student asks for detailed information.
"""

        prompt = f"""
{system_prompt}

User request:
{question}

Important:
- Do not unnecessarily make the answer very long.
- Use headings and bullet points where useful.
- Explain difficult concepts in simple language.
"""

        contents = [prompt]

        if image is not None:
            contents.append(image)

        # Try models one by one
        last_error = None

        for model in TEXT_MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        max_output_tokens=1200
                    )
                )

                if response and response.text:
                    return response.text

            except Exception as e:
                last_error = e
                time.sleep(0.5)
                continue

        return (
            "⚠️ AI is temporarily unavailable.\n\n"
            "Please try again in a few seconds."
        )

    except Exception:
        return (
            "⚠️ Unable to connect to Gemini right now.\n\n"
            "Please check your API key and try again."
        )


# =========================================================
# IMAGE GENERATION
# =========================================================

def generate_image(prompt):

    api_key = get_api_key()

    if not api_key:
        return None, "Gemini API key not found."

    try:
        client = get_client(api_key)

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["Image"]
            )
        )

        for part in response.parts:
            if part.inline_data:
                image = part.as_image()
                return image, None

        return None, "No image was generated."

    except Exception as e:
        return None, "Image generation is temporarily unavailable."


# =========================================================
# ADMIN SETTINGS
# =========================================================

def show_admin_settings():

    st.title("⚙️ Admin Settings")
    st.caption("Manage Tech Mithra AI Pro")

    st.info(
        "Admin settings are available only when the entered admin email "
        "matches the configured admin email."
    )

    st.divider()

    # -----------------------------------------------------
    # ADMIN EMAIL
    # -----------------------------------------------------

    st.subheader("👤 Admin Access")

    admin_email_input = st.text_input(
        "Admin Email",
        placeholder="Enter admin email"
    )

    if admin_email_input.strip().lower() != st.session_state.admin_email.lower():
        st.warning("Enter the correct admin email to access settings.")
        return

    st.success("✅ Admin verified")

    st.divider()

    # -----------------------------------------------------
    # APP SETTINGS
    # -----------------------------------------------------

    st.subheader("🎨 App Settings")

    new_title = st.text_input(
        "App Title",
        value=st.session_state.app_title
    )

    new_welcome = st.text_area(
        "Welcome Message",
        value=st.session_state.welcome_message
    )

    if st.button("💾 Save App Settings"):
        st.session_state.app_title = new_title
        st.session_state.welcome_message = new_welcome
        st.success("Settings saved successfully!")
        time.sleep(0.5)
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # AI SETTINGS
    # -----------------------------------------------------

    st.subheader("🤖 AI Settings")

    selected_model = st.selectbox(
        "Preferred AI Model",
        TEXT_MODELS,
        index=TEXT_MODELS.index(st.session_state.selected_model)
        if st.session_state.selected_model in TEXT_MODELS
        else 0
    )

    ai_status = st.toggle(
        "Enable AI",
        value=st.session_state.ai_enabled
    )

    if st.button("💾 Save AI Settings"):
        st.session_state.selected_model = selected_model
        st.session_state.ai_enabled = ai_status
        st.success("AI settings updated!")

    st.divider()

    # -----------------------------------------------------
    # HISTORY MANAGEMENT
    # -----------------------------------------------------

    st.subheader("📜 History Management")

    st.write(
        f"Current session history: "
        f"**{len(st.session_state.history)} conversations**"
    )

    if st.button("🗑️ Delete All History", type="secondary"):
        st.session_state.history = []
        st.success("All history deleted.")
        time.sleep(0.5)
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # APP INFORMATION
    # -----------------------------------------------------

    st.subheader("ℹ️ App Information")

    st.write("**App:** Tech Mithra AI Pro")
    st.write("**Version:** 2.0")
    st.write("**AI:** Google Gemini")
    st.write("**Platform:** Streamlit")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI Pro")

    st.caption("Your AI Student Assistant")

    st.divider()

    menu = st.radio(
        "📚 Select Feature",
        [
            "🏠 Home",
            "🔬 Project & Lab Guide",
            "🎉 Event Planner",
            "📚 Exam Hacker",
            "💼 Placement Prep",
            "📜 History",
            "⚙️ Admin Settings"
        ]
    )

    st.divider()

    st.metric(
        "📜 History",
        len(st.session_state.history)
    )

    st.divider()

    st.caption(
        "Powered by Google Gemini 🤖"
    )


# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.title(st.session_state.app_title)

    st.success(st.session_state.welcome_message)

    st.markdown("""
    ### 🎓 What can Tech Mithra AI do?

    🔬 **Project & Lab Guide**  
    Get project ideas, procedures, viva questions and lab guidance.

    🎉 **Event Planner**  
    Plan college events, schedules, budgets and promotional ideas.

    📚 **Exam Hacker**  
    Get exam-ready answers for 2, 5 and 10 marks.

    💼 **Placement Prep**  
    Prepare for technical and HR interviews.

    📜 **History**  
    View your previous AI questions and answers.

    ⚙️ **Admin Settings**  
    Manage app settings and history.
    """)

    st.info(
        "💡 Select a feature from the left sidebar to get started."
    )


# =========================================================
# PROJECT & LAB GUIDE
# =========================================================

elif menu == "🔬 Project & Lab Guide":

    st.title("🔬 Project & Lab Guide")

    question = st.text_area(
        "Ask your project/lab question",
        placeholder="Example: Explain 3 phase induction motor experiment"
    )

    uploaded_image = st.file_uploader(
        "📷 Upload an image (optional)",
        type=["png", "jpg", "jpeg"]
    )

    camera_image = st.camera_input(
        "📸 Take a photo (optional)"
    )

    selected_image = None

    if uploaded_image:
        selected_image = Image.open(uploaded_image)

    if camera_image:
        selected_image = Image.open(camera_image)

    if selected_image:
        st.image(
            selected_image,
            caption="Selected Image",
            width=300
        )

    if st.button("🤖 Ask AI", type="primary"):

        if not question.strip():
            st.warning("Please enter your question.")
        elif not st.session_state.ai_enabled:
            st.warning("AI is disabled by Admin.")
        else:
            with st.spinner("Thinking..."):
                answer = get_ai_response(
                    question,
                    "Project & Lab Guide",
                    selected_image
                )

            st.markdown("## 🤖 AI Answer")
            st.markdown(answer)

            add_history(
                "Project & Lab Guide",
                question,
                answer
            )


# =========================================================
# EVENT PLANNER
# =========================================================

elif menu == "🎉 Event Planner":

    st.title("🎉 AI Event Planner")

    event_name = st.text_input(
        "Event Name",
        placeholder="Example: Tech Fest 2026"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Technical Fest",
            "Cultural Event",
            "Workshop",
            "Seminar",
            "Hackathon",
            "Sports Event",
            "College Function",
            "Other"
        ]
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="Example: Engineering students"
    )

    st.divider()

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # EVENT PLAN
    # -----------------------------------------------------

    with col1:

        if st.button(
            "📋 Generate Event Plan",
            use_container_width=True
        ):

            if not event_name.strip():
                st.warning("Enter event name.")
            else:

                prompt = f"""
Create a complete college event plan.

Event Name: {event_name}
Event Type: {event_type}
Target Audience: {audience}

Include:
- Objective
- Event concept
- Schedule
- Activities
- Team roles
- Required materials
- Budget
- Promotion
- Safety
- Success measurement
"""

                with st.spinner("Creating event plan..."):
                    answer = get_ai_response(
                        prompt,
                        "Event Planner"
                    )

                st.markdown("## 📋 Event Plan")
                st.markdown(answer)

                add_history(
                    "Event Planner",
                    event_name,
                    answer
                )

    # -----------------------------------------------------
    # IMAGE PROMPT
    # -----------------------------------------------------

    with col2:

        if st.button(
            "🎨 Generate Image Prompt",
            use_container_width=True
        ):

            if not event_name.strip():
                st.warning("Enter event name.")
            else:

                prompt = f"""
Create a professional AI image-generation prompt
for a college event poster.

Event:
{event_name}

Type:
{event_type}

Audience:
{audience}

Make it cinematic, realistic, attractive and suitable
for a college promotional poster.
"""

                with st.spinner("Creating image prompt..."):
                    answer = get_ai_response(
                        prompt,
                        "Event Planner"
                    )

                st.markdown("## 🎨 Image Prompt")
                st.code(answer)

                add_history(
                    "Event Image Prompt",
                    event_name,
                    answer
                )

    # -----------------------------------------------------
    # TEXT TO IMAGE
    # -----------------------------------------------------

    st.divider()

    st.subheader("🖼️ Text to Image")

    image_prompt = st.text_area(
        "Enter image prompt",
        placeholder=(
            "Example: A cinematic college technical fest "
            "with futuristic technology, students and stage lights"
        )
    )

    if st.button(
        "✨ Generate Image",
        type="primary"
    ):

        if not image_prompt.strip():
            st.warning("Enter an image prompt.")
        else:

            with st.spinner("Generating image..."):
                generated_image, error = generate_image(
                    image_prompt
                )

            if generated_image:

                st.image(
                    generated_image,
                    caption="Generated by Gemini"
                )

                add_history(
                    "Text to Image",
                    image_prompt,
                    "Image generated successfully."
                )

            else:
                st.error(error)


# =========================================================
# EXAM HACKER
# =========================================================

elif menu == "📚 Exam Hacker":

    st.title("📚 Exam Hacker")

    subject = st.text_input(
        "Subject",
        placeholder="Example: Management"
    )

    topic = st.text_area(
        "Question / Topic",
        placeholder="Example: Explain evolution of management"
    )

    answer_type = st.selectbox(
        "Answer Type",
        [
            "2 Marks",
            "5 Marks",
            "10 Marks",
            "Easy Explanation"
        ]
    )

    if st.button(
        "📝 Generate Answer",
        type="primary"
    ):

        if not topic.strip():
            st.warning("Enter a question or topic.")
        else:

            prompt = f"""
Subject: {subject}
Question: {topic}
Required answer type: {answer_type}

Give an exam-ready answer.
"""

            with st.spinner("Preparing answer..."):
                answer = get_ai_response(
                    prompt,
                    "Exam Hacker"
                )

            st.markdown("## 📝 Answer")
            st.markdown(answer)

            add_history(
                "Exam Hacker",
                topic,
                answer
            )


# =========================================================
# PLACEMENT PREP
# =========================================================

elif menu == "💼 Placement Prep":

    st.title("💼 Placement Preparation")

    role = st.text_input(
        "Target Role",
        placeholder="Example: Electrical Engineer"
    )

    preparation_type = st.selectbox(
        "Preparation Type",
        [
            "Technical Questions",
            "HR Questions",
            "Aptitude",
            "Mock Interview",
            "Resume Preparation",
            "Company Preparation"
        ]
    )

    user_question = st.text_area(
        "Your Question",
        placeholder="Example: Give 20 interview questions for an EEE student"
    )

    if st.button(
        "🚀 Start Preparation",
        type="primary"
    ):

        if not user_question.strip():
            st.warning("Enter your question.")
        else:

            prompt = f"""
Target Role: {role}
Preparation Type: {preparation_type}

Student Request:
{user_question}
"""

            with st.spinner("Preparing..."):
                answer = get_ai_response(
                    prompt,
                    "Placement Prep"
                )

            st.markdown("## 💼 AI Preparation")
            st.markdown(answer)

            add_history(
                "Placement Prep",
                user_question,
                answer
            )


# =========================================================
# HISTORY PAGE
# =========================================================

elif menu == "📜 History":

    show_history()


# =========================================================
# ADMIN PAGE
# =========================================================

elif menu == "⚙️ Admin Settings":

    show_admin_settings()
