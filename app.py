import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from datetime import datetime
import time
import json
import re

# ============================================================
# TECH MITHRA AI PRO
# Complete Student AI App
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro 🎓",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# CONFIG
# ============================================================

ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

# Change this password before deployment
ADMIN_PASSWORD = "ChangeThisAdminPassword123!"

TEXT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
]

IMAGE_MODEL = "gemini-3.1-flash-image"


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "history": [],
    "admin_verified": False,
    "admin_login_requested": False,
    "app_title": "Tech Mithra AI Pro 🎓",
    "welcome_message": "Welcome to Tech Mithra AI Pro 🚀",
    "ai_enabled": True,
    "selected_model": TEXT_MODELS[0],
    "mcq_data": [],
    "mcq_answers": {},
    "mcq_submitted": False,
    "mcq_score": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


# ============================================================
# HISTORY
# ============================================================

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

    if not st.session_state.history:

        st.info(
            "No history yet. Your questions and answers "
            "will appear here."
        )

        return

    col1, col2 = st.columns([4, 1])

    with col1:
        st.success(
            f"Total conversations: "
            f"{len(st.session_state.history)}"
        )

    with col2:

        if st.button(
            "🗑️ Clear",
            use_container_width=True
        ):

            st.session_state.history = []

            st.rerun()

    st.divider()

    for item in reversed(st.session_state.history):

        question_short = (
            item["question"]
            .replace("\n", " ")
            [:70]
        )

        with st.expander(
            f"🕒 {item['time']} | "
            f"{item['mode']} | "
            f"{question_short}"
        ):

            st.markdown("### ❓ Question")
            st.write(item["question"])

            st.markdown("### 🤖 Answer")
            st.markdown(item["answer"])


# ============================================================
# AI RESPONSE
# ============================================================

def get_ai_response(
    question,
    mode="General",
    image=None
):

    if not st.session_state.ai_enabled:

        return "⚠️ AI is currently disabled by Admin."

    api_key = get_api_key()

    if not api_key:

        return (
            "⚠️ Gemini API key not found.\n\n"
            "Please add `GEMINI_API_KEY` in "
            "Streamlit Secrets."
        )

    try:

        client = get_client(api_key)

        if mode == "Doubt Solver":

            system_prompt = """
You are Tech Mithra AI Doubt Solver.

Help college students solve academic doubts.

Give:
1. Direct answer
2. Simple explanation
3. Step-by-step solution when useful
4. Example when useful
5. Important exam point

Keep the answer clear and student-friendly.
"""

        elif mode == "Project & Lab Guide":

            system_prompt = """
You are Tech Mithra AI Project and Laboratory Guide.

Help students with engineering projects and laboratory work.

Give:
1. Aim
2. Components
3. Theory
4. Working principle
5. Procedure
6. Circuit/block diagram explanation
7. Result
8. Applications
9. Viva questions

Keep explanations simple.
"""

        elif mode == "Event Planner":

            system_prompt = """
You are an expert college event planner.

Create practical event plans including:
1. Objective
2. Event concept
3. Target audience
4. Venue
5. Materials
6. Team responsibilities
7. Schedule
8. Budget
9. Promotion
10. Safety
"""

        elif mode == "Exam Hacker":

            system_prompt = """
You are an expert exam preparation assistant.

Give exam-ready answers.

2 marks:
Short and direct.

5 marks:
Medium detailed answer with headings.

10 marks:
Detailed answer with headings, points and examples.

Use simple student-friendly language.
"""

        elif mode == "Placement Prep":

            system_prompt = """
You are a placement preparation mentor.

Help students with:
- Technical interviews
- HR interviews
- Aptitude
- Resume preparation
- Communication
- Mock interviews
- Company preparation

Give practical answers.
"""

        else:

            system_prompt = """
You are Tech Mithra AI, a helpful student assistant.

Answer clearly and accurately.
Use simple language.
"""

        prompt = f"""
{system_prompt}

Student Request:

{question}

Important:
- Answer directly.
- Avoid unnecessary information.
- Use headings and bullet points.
"""

        contents = [prompt]

        if image is not None:
            contents.append(image)

        models_to_try = [
            st.session_state.selected_model
        ]

        for model in TEXT_MODELS:

            if model not in models_to_try:
                models_to_try.append(model)

        for model in models_to_try:

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

            except Exception:
                time.sleep(0.5)
                continue

        return (
            "⚠️ AI is temporarily unavailable. "
            "Please try again."
        )

    except Exception:

        return (
            "⚠️ Unable to connect to Gemini. "
            "Please check your API key."
        )


# ============================================================
# GENERATE MCQs
# ============================================================

def generate_mcqs(subject, topic, number):

    api_key = get_api_key()

    if not api_key:
        return None, "Gemini API key not found."

    try:

        client = get_client(api_key)

        prompt = f"""
Create exactly {number} multiple choice questions.

Subject:
{subject}

Topic:
{topic}

Rules:

- Each question must have exactly 4 options.
- Options must be A, B, C and D.
- Only one option must be correct.
- Questions should be useful for college students.
- Include different difficulty levels.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not add explanations.

JSON format:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "A",
    "explanation": "Short explanation"
  }}
]
"""

        models_to_try = [
            st.session_state.selected_model
        ]

        for model in TEXT_MODELS:
            if model not in models_to_try:
                models_to_try.append(model)

        for model in models_to_try:

            try:

                response = client.models.generate_content(

                    model=model,

                    contents=prompt,

                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=3000
                    )
                )

                if not response or not response.text:
                    continue

                text = response.text.strip()

                # Remove markdown code fences if present
                text = re.sub(
                    r"```json",
                    "",
                    text,
                    flags=re.IGNORECASE
                )

                text = text.replace(
                    "```",
                    ""
                ).strip()

                data = json.loads(text)

                if isinstance(data, list) and len(data) > 0:

                    valid_data = []

                    for item in data:

                        if not isinstance(item, dict):
                            continue

                        if (
                            "question" not in item
                            or "options" not in item
                            or "answer" not in item
                        ):
                            continue

                        options = item["options"]

                        if not all(
                            x in options
                            for x in ["A", "B", "C", "D"]
                        ):
                            continue

                        if item["answer"] not in [
                            "A", "B", "C", "D"
                        ]:
                            continue

                        valid_data.append(item)

                    if valid_data:
                        return valid_data, None

            except Exception:
                time.sleep(0.5)
                continue

        return None, (
            "⚠️ Could not generate MCQs right now. "
            "Please try again."
        )

    except Exception:

        return None, (
            "⚠️ MCQ generation failed. "
            "Please try again."
        )


# ============================================================
# IMAGE GENERATION
# ============================================================

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

    except Exception:

        return (
            None,
            "⚠️ Image generation is temporarily unavailable."
        )


# ============================================================
# ADMIN SETTINGS
# ============================================================

def show_admin_settings():

    st.title("⚙️ Admin Settings")

    if not st.session_state.admin_verified:

        st.subheader("🔐 Admin Verification")

        email = st.text_input(
            "Admin Email"
        )

        password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button(
            "🔓 Verify Admin",
            type="primary"
        ):

            if (
                email.strip().lower()
                == ADMIN_EMAIL.lower()
                and
                password
                == ADMIN_PASSWORD
            ):

                st.session_state.admin_verified = True

                st.success(
                    "✅ Admin verified."
                )

                time.sleep(0.5)

                st.rerun()

            else:

                st.error(
                    "❌ Invalid admin credentials."
                )

        return

    # --------------------------------------------------------
    # VERIFIED ADMIN
    # --------------------------------------------------------

    st.success(
        "🟢 Admin Access Active"
    )

    if st.button(
        "🔒 Logout Admin"
    ):

        st.session_state.admin_verified = False

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # APP SETTINGS
    # --------------------------------------------------------

    st.subheader("🎨 App Settings")

    title = st.text_input(
        "App Title",
        value=st.session_state.app_title
    )

    welcome = st.text_area(
        "Welcome Message",
        value=st.session_state.welcome_message
    )

    if st.button(
        "💾 Save App Settings"
    ):

        st.session_state.app_title = title

        st.session_state.welcome_message = welcome

        st.success(
            "✅ App settings saved."
        )

    st.divider()

    # --------------------------------------------------------
    # AI SETTINGS
    # --------------------------------------------------------

    st.subheader("🤖 AI Settings")

    model = st.selectbox(
        "Preferred AI Model",
        TEXT_MODELS,

        index=(
            TEXT_MODELS.index(
                st.session_state.selected_model
            )
            if st.session_state.selected_model
            in TEXT_MODELS
            else 0
        )
    )

    ai_enabled = st.toggle(
        "Enable AI",
        value=st.session_state.ai_enabled
    )

    if st.button(
        "💾 Save AI Settings"
    ):

        st.session_state.selected_model = model

        st.session_state.ai_enabled = ai_enabled

        st.success(
            "✅ AI settings updated."
        )

    st.divider()

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    st.subheader("📜 History Management")

    st.write(
        f"Current history: "
        f"**{len(st.session_state.history)}**"
    )

    if st.button(
        "🗑️ Delete All History"
    ):

        st.session_state.history = []

        st.success(
            "✅ All history deleted."
        )

        st.rerun()

    st.divider()

    st.subheader("ℹ️ App Information")

    st.write("**Application:** Tech Mithra AI Pro")
    st.write("**Version:** 3.0")
    st.write("**AI:** Google Gemini")
    st.write("**Platform:** Streamlit")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra")

    st.caption(
        "AI Student Assistant"
    )

    st.divider()

    menu_items = [

        "🏠 Home",

        "💬 Doubt Solver",

        "🔬 Project & Lab Guide",

        "🎉 Event Planner",

        "📚 Exam Hacker",

        "💼 Placement Prep",

        "📜 History"
    ]

    # Admin Settings appears ONLY after admin verification
    if st.session_state.admin_verified:

        menu_items.append(
            "⚙️ Admin Settings"
        )

    menu = st.radio(
        "📚 Select Feature",
        menu_items
    )

    st.divider()

    st.metric(
        "📜 History",
        len(st.session_state.history)
    )

    st.divider()

    if st.button(
        "🔐 Admin Login",
        use_container_width=True
    ):

        st.session_state.admin_login_requested = True

        st.rerun()

    st.caption(
        "Powered by Google Gemini 🤖"
    )


# ============================================================
# SIDEBAR ADMIN LOGIN
# ============================================================

if (
    st.session_state.admin_login_requested
    and
    not st.session_state.admin_verified
):

    st.title("🔐 Admin Login")

    st.info(
        "Admin Settings are hidden from normal users."
    )

    email = st.text_input(
        "Admin Email",
        key="login_email"
    )

    password = st.text_input(
        "Admin Password",
        type="password",
        key="login_password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔓 Login",
            type="primary"
        ):

            if (
                email.strip().lower()
                == ADMIN_EMAIL.lower()
                and
                password
                == ADMIN_PASSWORD
            ):

                st.session_state.admin_verified = True

                st.session_state.admin_login_requested = False

                st.success(
                    "✅ Admin login successful!"
                )

                time.sleep(0.5)

                st.rerun()

            else:

                st.error(
                    "❌ Wrong email or password."
                )

    with col2:

        if st.button("❌ Cancel"):

            st.session_state.admin_login_requested = False

            st.rerun()


# ============================================================
# HOME
# ============================================================

elif menu == "🏠 Home":

    st.title(
        st.session_state.app_title
    )

    st.success(
        st.session_state.welcome_message
    )

    st.markdown(
        """
## 🎓 Your AI Student Assistant

### 💬 Doubt Solver
Ask academic doubts and get simple explanations.

### 🔬 Project & Lab Guide
Get project ideas, procedures, viva questions and lab guidance.

### 🎉 Event Planner
Create college event plans, schedules, budgets and image prompts.

### 📚 Exam Hacker
Prepare 2, 5 and 10 mark answers and practice with MCQs.

### 💼 Placement Prep
Prepare for technical and HR interviews.

### 📜 History
View your previous AI questions and answers.

---

💡 Select a feature from the sidebar.
"""
    )


# ============================================================
# DOUBT SOLVER
# ============================================================

elif menu == "💬 Doubt Solver":

    st.title("💬 AI Doubt Solver")

    doubt = st.text_area(
        "Your Doubt",
        placeholder=(
            "Example: What is bounded rationality?"
        ),
        height=150
    )

    uploaded_image = st.file_uploader(
        "📷 Upload question image (optional)",
        type=["png", "jpg", "jpeg"]
    )

    camera_image = st.camera_input(
        "📸 Take a photo of your question"
    )

    selected_image = None

    if uploaded_image:

        selected_image = Image.open(
            uploaded_image
        )

    if camera_image:

        selected_image = Image.open(
            camera_image
        )

    if selected_image:

        st.image(
            selected_image,
            caption="Question Image",
            width=350
        )

    if st.button(
        "🤖 Solve My Doubt",
        type="primary"
    ):

        if (
            not doubt.strip()
            and selected_image is None
        ):

            st.warning(
                "Please enter a doubt or upload an image."
            )

        else:

            question = (
                doubt.strip()
                if doubt.strip()
                else
                "Question from uploaded image"
            )

            with st.spinner(
                "🤖 Solving..."
            ):

                answer = get_ai_response(
                    question,
                    "Doubt Solver",
                    selected_image
                )

            st.markdown("## 🤖 Answer")

            st.markdown(answer)

            add_history(
                "Doubt Solver",
                question,
                answer
            )


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif menu == "🔬 Project & Lab Guide":

    st.title(
        "🔬 Project & Lab Guide"
    )

    question = st.text_area(
        "Ask your project/lab question",
        placeholder=(
            "Example: Explain 3 phase induction motor experiment"
        ),
        height=150
    )

    uploaded_image = st.file_uploader(
        "📷 Upload image (optional)",
        type=["png", "jpg", "jpeg"]
    )

    camera_image = st.camera_input(
        "📸 Take a photo (optional)"
    )

    selected_image = None

    if uploaded_image:

        selected_image = Image.open(
            uploaded_image
        )

    if camera_image:

        selected_image = Image.open(
            camera_image
        )

    if selected_image:

        st.image(
            selected_image,
            caption="Selected Image",
            width=350
        )

    if st.button(
        "🤖 Ask AI",
        type="primary"
    ):

        if (
            not question.strip()
            and selected_image is None
        ):

            st.warning(
                "Please enter a question or upload an image."
            )

        else:

            history_question = (
                question.strip()
                if question.strip()
                else
                "Question from uploaded image"
            )

            with st.spinner(
                "🤖 Thinking..."
            ):

                answer = get_ai_response(
                    history_question,
                    "Project & Lab Guide",
                    selected_image
                )

            st.markdown("## 🤖 AI Answer")

            st.markdown(answer)

            add_history(
                "Project & Lab Guide",
                history_question,
                answer
            )


# ============================================================
# EVENT PLANNER
# ============================================================

elif menu == "🎉 Event Planner":

    st.title(
        "🎉 AI Event Planner"
    )

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
        placeholder="Example: Engineering Students"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📋 Generate Event Plan",
            use_container_width=True
        ):

            if not event_name.strip():

                st.warning(
                    "Please enter event name."
                )

            else:

                prompt = f"""
Create a complete college event plan.

Event Name:
{event_name}

Event Type:
{event_type}

Target Audience:
{audience}

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

                with st.spinner(
                    "Creating event plan..."
                ):

                    answer = get_ai_response(
                        prompt,
                        "Event Planner"
                    )

                st.markdown(
                    "## 📋 Event Plan"
                )

                st.markdown(answer)

                add_history(
                    "Event Planner",
                    event_name,
                    answer
                )

    with col2:

        if st.button(
            "🎨 Generate Image Prompt",
            use_container_width=True
        ):

            if not event_name.strip():

                st.warning(
                    "Please enter event name."
                )

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

Make it cinematic, realistic,
professional and attractive.
"""

                with st.spinner(
                    "Creating prompt..."
                ):

                    answer = get_ai_response(
                        prompt,
                        "Event Planner"
                    )

                st.markdown(
                    "## 🎨 Image Prompt"
                )

                st.code(answer)

                add_history(
                    "Event Image Prompt",
                    event_name,
                    answer
                )

    st.divider()

    st.subheader(
        "🖼️ Text to Image"
    )

    image_prompt = st.text_area(
        "Enter image prompt",
        placeholder=(
            "Example: Cinematic college technical fest "
            "with futuristic technology and students"
        )
    )

    if st.button(
        "✨ Generate Image",
        type="primary"
    ):

        if not image_prompt.strip():

            st.warning(
                "Please enter image prompt."
            )

        else:

            with st.spinner(
                "🎨 Generating image..."
            ):

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


# ============================================================
# EXAM HACKER
# ============================================================

elif menu == "📚 Exam Hacker":

    st.title(
        "📚 Exam Hacker"
    )

    exam_tab1, exam_tab2 = st.tabs(
        [
            "📝 Answers",
            "🎯 MCQ Quiz"
        ]
    )

    # ========================================================
    # ANSWERS
    # ========================================================

    with exam_tab1:

        st.subheader(
            "📝 Exam Answer Generator"
        )

        subject = st.text_input(
            "Subject",
            placeholder="Example: Management",
            key="exam_subject"
        )

        topic = st.text_area(
            "Question / Topic",
            placeholder=(
                "Example: Explain evolution of management"
            ),
            height=150,
            key="exam_topic"
        )

        answer_type = st.selectbox(
            "Answer Type",
            [
                "2 Marks",
                "5 Marks",
                "10 Marks",
                "Easy Explanation"
            ],
            key="answer_type"
        )

        if st.button(
            "📝 Generate Answer",
            type="primary"
        ):

            if not topic.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                prompt = f"""
Subject:
{subject}

Question:
{topic}

Required Answer:
{answer_type}

Give an exam-ready answer.
"""

                with st.spinner(
                    "📝 Preparing answer..."
                ):

                    answer = get_ai_response(
                        prompt,
                        "Exam Hacker"
                    )

                st.markdown(
                    "## 📝 Answer"
                )

                st.markdown(answer)

                add_history(
                    "Exam Hacker",
                    topic,
                    answer
                )

    # ========================================================
    # MCQ QUIZ
    # ========================================================

    with exam_tab2:

        st.subheader(
            "🎯 AI MCQ Quiz"
        )

        st.write(
            "Generate MCQs and test your knowledge."
        )

        mcq_subject = st.text_input(
            "MCQ Subject",
            placeholder="Example: Electrical Machines",
            key="mcq_subject"
        )

        mcq_topic = st.text_input(
            "MCQ Topic",
            placeholder="Example: Induction Motor",
            key="mcq_topic"
        )

        number_of_mcqs = st.selectbox(
            "Number of MCQs",
            [5, 10, 15, 20],
            index=0
        )

        if st.button(
            "🎯 Generate MCQ Quiz",
            type="primary"
        ):

            if not mcq_subject.strip():

                st.warning(
                    "Please enter subject."
                )

            elif not mcq_topic.strip():

                st.warning(
                    "Please enter topic."
                )

            else:

                with st.spinner(
                    "🤖 Creating MCQ quiz..."
                ):

                    data, error = generate_mcqs(
                        mcq_subject,
                        mcq_topic,
                        number_of_mcqs
                    )

                if data:

                    st.session_state.mcq_data = data

                    st.session_state.mcq_answers = {}

                    st.session_state.mcq_submitted = False

                    st.session_state.mcq_score = 0

                    st.success(
                        f"✅ {len(data)} MCQs generated!"
                    )

                    st.rerun()

                else:

                    st.error(error)

        # ----------------------------------------------------
        # SHOW MCQS
        # ----------------------------------------------------

        if st.session_state.mcq_data:

            st.divider()

            st.markdown(
                "### 📝 Answer all questions"
            )

            for i, mcq in enumerate(
                st.session_state.mcq_data
            ):

                st.markdown(
                    f"### Q{i + 1}. "
                    f"{mcq['question']}"
                )

                options = mcq["options"]

                selected = st.radio(
                    "Choose answer:",
                    [
                        f"A. {options['A']}",
                        f"B. {options['B']}",
                        f"C. {options['C']}",
                        f"D. {options['D']}"
                    ],
                    key=f"mcq_{i}",
                    index=None
                )

                if selected:

                    answer_letter = selected[0]

                    st.session_state.mcq_answers[i] = (
                        answer_letter
                    )

                st.divider()

            # ------------------------------------------------
            # SUBMIT
            # ------------------------------------------------

            if st.button(
                "✅ Submit Quiz",
                type="primary"
            ):

                score = 0

                for i, mcq in enumerate(
                    st.session_state.mcq_data
                ):

                    user_answer = (
                        st.session_state.mcq_answers
                        .get(i)
                    )

                    correct_answer = (
                        mcq["answer"]
                    )

                    if user_answer == correct_answer:

                        score += 1

                st.session_state.mcq_score = score

                st.session_state.mcq_submitted = True

                st.rerun()

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if (
            st.session_state.mcq_submitted
            and
            st.session_state.mcq_data
        ):

            total = len(
                st.session_state.mcq_data
            )

            score = st.session_state.mcq_score

            percentage = (
                score / total * 100
            )

            st.divider()

            st.subheader(
                "🏆 Quiz Result"
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:

                st.metric(
                    "Score",
                    f"{score}/{total}"
                )

            with result_col2:

                st.metric(
                    "Percentage",
                    f"{percentage:.0f}%"
                )

            with result_col3:

                if percentage >= 80:
                    result = "Excellent 🏆"
                elif percentage >= 60:
                    result = "Good 👍"
                elif percentage >= 40:
                    result = "Keep Practicing 📚"
                else:
                    result = "Need More Practice 💪"

                st.metric(
                    "Performance",
                    result
                )

            st.divider()

            st.subheader(
                "📖 Answers & Explanations"
            )

            for i, mcq in enumerate(
                st.session_state.mcq_data
            ):

                correct = mcq["answer"]

                user = (
                    st.session_state.mcq_answers
                    .get(i, "Not Answered")
                )

                if user == correct:

                    st.success(
                        f"Q{i + 1}: ✅ Correct — "
                        f"Answer: {correct}"
                    )

                else:

                    st.error(
                        f"Q{i + 1}: ❌ Wrong — "
                        f"Correct Answer: {correct}"
                    )

                st.write(
                    mcq.get(
                        "explanation",
                        "No explanation available."
                    )
                )

            # Save result to history

            quiz_summary = (
                f"MCQ Quiz: "
                f"{mcq_subject} - {mcq_topic}"
            )

            quiz_result = (
                f"Score: {score}/{total}\n\n"
                f"Percentage: {percentage:.0f}%\n\n"
                f"Performance: {result}"
            )

            # Avoid repeatedly adding same result
            if not st.session_state.get(
                "quiz_saved",
                False
            ):

                add_history(
                    "MCQ Quiz",
                    quiz_summary,
                    quiz_result
                )

                st.session_state.quiz_saved = True

            st.divider()

            if st.button(
                "🔄 Start New Quiz"
            ):

                st.session_state.mcq_data = []

                st.session_state.mcq_answers = {}

                st.session_state.mcq_submitted = False

                st.session_state.mcq_score = 0

                st.session_state.quiz_saved = False

                st.rerun()


# ============================================================
# PLACEMENT PREP
# ============================================================

elif menu == "💼 Placement Prep":

    st.title(
        "💼 Placement Preparation"
    )

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
        placeholder=(
            "Example: Give 20 interview questions for EEE students"
        ),
        height=150
    )

    if st.button(
        "🚀 Start Preparation",
        type="primary"
    ):

        if not user_question.strip():

            st.warning(
                "Please enter your question."
            )

        else:

            prompt = f"""
Target Role:
{role}

Preparation Type:
{preparation_type}

Student Request:
{user_question}
"""

            with st.spinner(
                "💼 Preparing..."
            ):

                answer = get_ai_response(
                    prompt,
                    "Placement Prep"
                )

            st.markdown(
                "## 💼 AI Preparation"
            )

            st.markdown(answer)

            add_history(
                "Placement Prep",
                user_question,
                answer
            )


# ============================================================
# HISTORY
# ============================================================

elif menu == "📜 History":

    show_history()


# ============================================================
# ADMIN SETTINGS
# ============================================================

elif (
    menu == "⚙️ Admin Settings"
    and
    st.session_state.admin_verified
):

    show_admin_settings()
