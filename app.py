import streamlit as st
import json
from datetime import datetime
from PIL import Image
from google import genai
from google.genai import types

# =========================================================
# TECH MITHRA AI PRO
# Complete Single-Page Streamlit App
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro 🎓",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# CONFIG
# =========================================================

APP_NAME = "Tech Mithra AI Pro"
DEFAULT_ADMIN_EMAIL = "madhukrishnamogili@gmail.com"

# Better: put these in Streamlit Secrets
ADMIN_EMAIL = st.secrets.get("ADMIN_EMAIL", DEFAULT_ADMIN_EMAIL)
ADMIN_PASSWORD = st.secrets.get(
    "ADMIN_PASSWORD",
    "ChangeThisAdminPassword123!"
)

TEXT_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
]

IMAGE_MODEL = "gemini-2.5-flash-image"

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "admin_verified" not in st.session_state:
    st.session_state.admin_verified = False

if "show_attachments" not in st.session_state:
    st.session_state.show_attachments = False

if "mcq_data" not in st.session_state:
    st.session_state.mcq_data = []

if "mcq_answers" not in st.session_state:
    st.session_state.mcq_answers = {}

if "mcq_submitted" not in st.session_state:
    st.session_state.mcq_submitted = False

if "mcq_score" not in st.session_state:
    st.session_state.mcq_score = 0


# =========================================================
# GEMINI CLIENT
# =========================================================

@st.cache_resource
def get_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=api_key)
    except Exception:
        return None


client = get_client()


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def add_history(mode, question, answer):
    st.session_state.history.insert(
        0,
        {
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "mode": mode,
            "question": question,
            "answer": answer
        }
    )


def ask_ai(prompt, model=None, extra_content=None):
    if client is None:
        return "⚠️ Gemini API key setup cheyyali. `.streamlit/secrets.toml` lo GEMINI_API_KEY add cheyyandi."

    if model is None:
        model = TEXT_MODELS[0]

    try:
        contents = [prompt]

        if extra_content:
            contents.extend(extra_content)

        response = client.models.generate_content(
            model=model,
            contents=contents
        )

        if response.text:
            return response.text

        return "AI response empty ga vachindi."

    except Exception as e:
        return f"❌ AI Error: {str(e)}"


def generate_image(prompt):
    if client is None:
        st.error("Gemini API key setup cheyyali.")
        return

    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["Image"]
            )
        )

        found = False

        for part in response.parts:
            if part.inline_data:
                image = part.as_image()
                st.image(image, use_container_width=True)
                found = True

        if not found:
            st.warning("Image generate avvaledu.")

    except Exception as e:
        st.error(f"Image generation error: {e}")


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🚀 Tech Mithra AI Pro")

menu_items = [
    "💬 AI Chat",
    "💡 Doubt Solver",
    "🔬 Project & Lab Guide",
    "🎉 Event Planner",
    "📚 Exam Hacker",
    "💼 Placement Prep",
    "📜 History"
]

if st.session_state.admin_verified:
    menu_items.append("⚙️ Admin Settings")

selected = st.sidebar.radio(
    "Select Option",
    menu_items
)

st.sidebar.divider()

# =========================================================
# ADMIN LOGIN
# =========================================================

with st.sidebar.expander("🔐 Admin Login"):

    admin_email_input = st.text_input(
        "Admin Email",
        key="admin_email_input"
    )

    admin_password_input = st.text_input(
        "Admin Password",
        type="password",
        key="admin_password_input"
    )

    if st.button("Login as Admin", use_container_width=True):

        if (
            admin_email_input == ADMIN_EMAIL
            and admin_password_input == ADMIN_PASSWORD
        ):
            st.session_state.admin_verified = True
            st.success("Admin login successful!")
            st.rerun()

        else:
            st.error("Invalid admin credentials.")

    if st.session_state.admin_verified:

        if st.button("Logout Admin", use_container_width=True):
            st.session_state.admin_verified = False
            st.rerun()


# =========================================================
# AI CHAT
# =========================================================

if selected == "💬 AI Chat":

    st.title("💬 Tech Mithra AI")

    st.caption(
        "Ask doubts, upload photos/files, or use your camera."
    )

    # Display previous chat
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):

            if message.get("image"):
                st.image(
                    message["image"],
                    width=300
                )

            if message.get("content"):
                st.markdown(message["content"])

    # =====================================================
    # PLUS ATTACHMENT BUTTON
    # =====================================================

    col1, col2 = st.columns([1, 8])

    with col1:

        if st.button(
            "➕",
            help="Upload Photo / Camera / Files"
        ):
            st.session_state.show_attachments = (
                not st.session_state.show_attachments
            )

    # =====================================================
    # ATTACHMENTS
    # =====================================================

    uploaded_files = []
    camera_image = None

    if st.session_state.show_attachments:

        st.info(
            "📎 Attachments"
        )

        close_col, empty_col = st.columns([1, 7])

        with close_col:

            if st.button("❌ Close"):
                st.session_state.show_attachments = False
                st.rerun()

        uploaded_files = st.file_uploader(
            "📁 Upload Photo / Files",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
                "txt",
                "py",
                "java",
                "c",
                "cpp",
                "html",
                "css",
                "js",
                "json",
                "csv",
                "md",
                "pdf"
            ],
            accept_multiple_files=True
        )

        camera_image = st.camera_input(
            "📸 Camera"
        )

        if uploaded_files:

            st.write("Selected files:")

            for file in uploaded_files:
                st.write(
                    f"📎 {file.name}"
                )

        if camera_image:
            st.image(
                camera_image,
                caption="Camera Image",
                width=250
            )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    user_prompt = st.chat_input(
        "Message Tech Mithra..."
    )

    if user_prompt is not None:

        # User message
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        extra_content = []
        display_image = None

        # Camera image
        if camera_image:

            try:

                image = Image.open(camera_image)

                extra_content.append(image)

                display_image = image

            except Exception:
                pass

        # Uploaded files
        for file in uploaded_files:

            try:

                file_type = file.type or ""

                # Images
                if file_type.startswith("image/"):

                    image = Image.open(file)

                    extra_content.append(image)

                    if display_image is None:
                        display_image = image

                # Text/code files
                elif file_type.startswith("text/") or file.name.endswith(
                    (
                        ".py",
                        ".java",
                        ".c",
                        ".cpp",
                        ".html",
                        ".css",
                        ".js",
                        ".json",
                        ".csv",
                        ".md",
                        ".txt"
                    )
                ):

                    text_data = file.read().decode(
                        "utf-8",
                        errors="ignore"
                    )

                    extra_content.append(
                        f"\n\n--- FILE: {file.name} ---\n{text_data}"
                    )

                else:

                    extra_content.append(
                        f"\n[File attached: {file.name}]"
                    )

            except Exception:
                extra_content.append(
                    f"\n[File attached: {file.name}]"
                )

        if not user_prompt.strip():

            user_prompt = (
                "Analyze the attached photo/files and explain "
                "the important information in a simple way."
            )

        answer = ask_ai(
            user_prompt,
            extra_content=extra_content
        )

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        add_history(
            "AI Chat",
            user_prompt,
            answer
        )

        st.rerun()


# =========================================================
# DOUBT SOLVER
# =========================================================

elif selected == "💡 Doubt Solver":

    st.title("💡 Doubt Solver")

    question = st.text_area(
        "Enter your doubt",
        placeholder="Example: Explain transformer working..."
    )

    image_file = st.file_uploader(
        "📷 Upload question image",
        type=["png", "jpg", "jpeg"]
    )

    camera = st.camera_input(
        "📸 Take a photo of your question"
    )

    if st.button(
        "🤖 Solve Doubt",
        use_container_width=True
    ):

        extra = []

        if image_file:

            try:
                extra.append(
                    Image.open(image_file)
                )
            except Exception:
                pass

        if camera:

            try:
                extra.append(
                    Image.open(camera)
                )
            except Exception:
                pass

        if not question.strip() and not extra:

            st.warning(
                "Question enter cheyyandi or image upload cheyyandi."
            )

        else:

            prompt = f"""
You are Tech Mithra AI, a helpful college student assistant.

Solve the student's doubt clearly.

Question:
{question}

Give:
1. Simple definition
2. Explanation
3. Important points
4. Example if useful
5. Exam-friendly answer
"""

            answer = ask_ai(
                prompt,
                extra_content=extra
            )

            st.markdown(answer)

            add_history(
                "Doubt Solver",
                question if question else "Image Question",
                answer
            )


# =========================================================
# PROJECT & LAB GUIDE
# =========================================================

elif selected == "🔬 Project & Lab Guide":

    st.title("🔬 Project & Lab Guide")

    project = st.text_input(
        "Project / Lab Topic",
        placeholder="Example: Solar Tracking System"
    )

    project_image = st.file_uploader(
        "📷 Upload project image",
        type=["png", "jpg", "jpeg"]
    )

    if st.button(
        "🚀 Generate Project Guide",
        use_container_width=True
    ):

        if not project.strip():

            st.warning(
                "Project topic enter cheyyandi."
            )

        else:

            extra = []

            if project_image:

                try:
                    extra.append(
                        Image.open(project_image)
                    )
                except Exception:
                    pass

            prompt = f"""
Create a complete college project/lab guide.

Topic:
{project}

Include:
1. Introduction
2. Objective
3. Components / Requirements
4. Block diagram explanation
5. Working principle
6. Step-by-step procedure
7. Advantages
8. Disadvantages
9. Applications
10. Result
11. Viva questions and answers

Use simple student-friendly language.
"""

            answer = ask_ai(
                prompt,
                extra_content=extra
            )

            st.markdown(answer)

            add_history(
                "Project & Lab Guide",
                project,
                answer
            )


# =========================================================
# EVENT PLANNER
# =========================================================

elif selected == "🎉 Event Planner":

    st.title("🎉 Event Planner")

    event_name = st.text_input(
        "Event Name"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "College Event",
            "Technical Event",
            "Workshop",
            "Seminar",
            "Fest",
            "Cultural Event",
            "Sports Event"
        ]
    )

    audience = st.text_input(
        "Target Audience"
    )

    if st.button(
        "🎯 Create Event Plan",
        use_container_width=True
    ):

        prompt = f"""
Create a professional college event plan.

Event:
{event_name}

Type:
{event_type}

Audience:
{audience}

Include:
- Event objective
- Schedule
- Activities
- Required resources
- Team responsibilities
- Budget categories
- Promotion ideas
- Risk management
- Closing plan
"""

        answer = ask_ai(prompt)

        st.markdown(answer)

        add_history(
            "Event Planner",
            event_name,
            answer
        )

    st.divider()

    st.subheader("🎨 Event Poster Image Prompt")

    poster_prompt = st.text_area(
        "Enter poster idea"
    )

    if st.button(
        "🖼️ Generate Event Image"
    ):

        if poster_prompt:

            generate_image(
                f"""
Create a professional college event poster.

Event:
{poster_prompt}

Modern educational design,
clean typography,
professional college atmosphere,
high quality.
"""
            )


# =========================================================
# EXAM HACKER
# =========================================================

elif selected == "📚 Exam Hacker":

    st.title("📚 Exam Hacker")

    st.caption(
        "MCQs + Answers + Explanations + Score"
    )

    tab1, tab2 = st.tabs(
        [
            "📝 Answer Generator",
            "🎯 MCQ Quiz"
        ]
    )

    # =====================================================
    # ANSWER GENERATOR
    # =====================================================

    with tab1:

        exam_question = st.text_area(
            "Enter exam question",
            placeholder="Example: Explain working of induction motor."
        )

        marks = st.selectbox(
            "Marks",
            [
                "2 Marks",
                "5 Marks",
                "10 Marks",
                "15 Marks"
            ]
        )

        if st.button(
            "✍️ Generate Exam Answer",
            use_container_width=True
        ):

            if not exam_question.strip():

                st.warning(
                    "Question enter cheyyandi."
                )

            else:

                prompt = f"""
You are an expert college exam assistant.

Question:
{exam_question}

Marks:
{marks}

Create a clear exam answer.

Include:
- Definition
- Main explanation
- Important points
- Examples if needed
- Conclusion

Make it easy to write in an examination.
"""

                answer = ask_ai(prompt)

                st.markdown(answer)

                add_history(
                    "Exam Hacker",
                    exam_question,
                    answer
                )

    # =====================================================
    # MCQ QUIZ
    # =====================================================

    with tab2:

        st.subheader("🎯 MCQ Practice Quiz")

        subject = st.text_input(
            "Subject / Topic",
            placeholder="Example: Management, IoT, Electrical Machines"
        )

        number_of_questions = st.selectbox(
            "Number of MCQs",
            [5, 10, 15, 20]
        )

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ]
        )

        # -------------------------------------------------
        # GENERATE MCQS
        # -------------------------------------------------

        if st.button(
            "🚀 Generate MCQs",
            use_container_width=True
        ):

            if not subject.strip():

                st.warning(
                    "Subject / topic enter cheyyandi."
                )

            else:

                prompt = f"""
Generate exactly {number_of_questions} multiple-choice
questions for college students.

Subject:
{subject}

Difficulty:
{difficulty}

Return ONLY valid JSON.

Use this exact format:

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

Rules:
- Every question must have exactly A, B, C, D.
- answer must be only A, B, C or D.
- Make sure the correct answer matches the option.
- Do not add markdown.
- Do not add extra text outside JSON.
"""

                try:

                    response_text = ask_ai(prompt)

                    # Remove accidental markdown fences
                    response_text = response_text.strip()

                    if response_text.startswith("```"):

                        response_text = (
                            response_text
                            .replace("```json", "")
                            .replace("```", "")
                            .strip()
                        )

                    mcqs = json.loads(
                        response_text
                    )

                    if isinstance(mcqs, list):

                        st.session_state.mcq_data = mcqs
                        st.session_state.mcq_answers = {}
                        st.session_state.mcq_submitted = False
                        st.session_state.mcq_score = 0

                        st.success(
                            f"✅ {len(mcqs)} MCQs generated!"
                        )

                    else:

                        st.error(
                            "MCQ format incorrect."
                        )

                except Exception as e:

                    st.error(
                        f"MCQ generation error: {e}"
                    )

        # -------------------------------------------------
        # SHOW MCQS
        # -------------------------------------------------

        if st.session_state.mcq_data:

            st.divider()

            st.subheader(
                "📝 Choose the correct answer"
            )

            # -------------------------------------------------
            # MCQ OPTIONS
            # -------------------------------------------------

            for index, mcq in enumerate(
                st.session_state.mcq_data
            ):

                st.markdown(
                    f"### Q{index + 1}. {mcq.get('question', '')}"
                )

                options = mcq.get(
                    "options",
                    {}
                )

                option_list = [
                    "A",
                    "B",
                    "C",
                    "D"
                ]

                option_text = []

                for letter in option_list:

                    option_text.append(
                        f"{letter}. {options.get(letter, '')}"
                    )

                selected_answer = st.radio(
                    "Select your answer:",
                    option_list,
                    format_func=lambda x,
                    opts=options: (
                        f"{x}. {opts.get(x, '')}"
                    ),
                    key=f"mcq_option_{index}",
                    disabled=st.session_state.mcq_submitted
                )

                # Save selected answer
                st.session_state.mcq_answers[
                    index
                ] = selected_answer

                st.divider()

            # -------------------------------------------------
            # SUBMIT QUIZ
            # -------------------------------------------------

            if not st.session_state.mcq_submitted:

                if st.button(
                    "✅ Submit Quiz",
                    use_container_width=True
                ):

                    score = 0

                    for index, mcq in enumerate(
                        st.session_state.mcq_data
                    ):

                        correct_answer = str(
                            mcq.get("answer", "")
                        ).upper().strip()

                        user_answer = st.session_state.mcq_answers.get(
                            index
                        )

                        if user_answer == correct_answer:
                            score += 1

                    st.session_state.mcq_score = score
                    st.session_state.mcq_submitted = True

                    total = len(
                        st.session_state.mcq_data
                    )

                    percentage = (
                        score / total * 100
                        if total > 0
                        else 0
                    )

                    if percentage >= 80:
                        performance = "🏆 Excellent!"

                    elif percentage >= 60:
                        performance = "👏 Good!"

                    elif percentage >= 40:
                        performance = "📖 Need More Practice"

                    else:
                        performance = "💪 Keep Practicing!"

                    result_text = f"""
MCQ Quiz completed.

Score: {score}/{total}
Percentage: {percentage:.1f}%
Performance: {performance}
"""

                    add_history(
                        "Exam Hacker MCQ Quiz",
                        subject,
                        result_text
                    )

                    st.rerun()

            # -------------------------------------------------
            # RESULT
            # -------------------------------------------------

            if st.session_state.mcq_submitted:

                total = len(
                    st.session_state.mcq_data
                )

                score = st.session_state.mcq_score

                percentage = (
                    score / total * 100
                    if total > 0
                    else 0
                )

                if percentage >= 80:
                    performance = "🏆 Excellent!"

                elif percentage >= 60:
                    performance = "👏 Good!"

                elif percentage >= 40:
                    performance = "📖 Need More Practice"

                else:
                    performance = "💪 Keep Practicing!"

                st.success(
                    f"🎯 Score: {score}/{total}"
                )

                st.info(
                    f"📊 Percentage: {percentage:.1f}%"
                )

                st.warning(
                    f"Performance: {performance}"
                )

                st.divider()

                st.subheader(
                    "📋 Answers & Explanations"
                )

                # -------------------------------------------------
                # SHOW CORRECT ANSWERS
                # -------------------------------------------------

                for index, mcq in enumerate(
                    st.session_state.mcq_data
                ):

                    question = mcq.get(
                        "question",
                        ""
                    )

                    options = mcq.get(
                        "options",
                        {}
                    )

                    correct = str(
                        mcq.get("answer", "")
                    ).upper()

                    user_answer = st.session_state.mcq_answers.get(
                        index,
                        "Not Answered"
                    )

                    explanation = mcq.get(
                        "explanation",
                        "No explanation available."
                    )

                    st.markdown(
                        f"### Q{index + 1}. {question}"
                    )

                    st.write(
                        f"**Your Answer:** {user_answer}"
                    )

                    st.write(
                        f"**Correct Answer:** {correct}. "
                        f"{options.get(correct, '')}"
                    )

                    if user_answer == correct:

                        st.success(
                            "✅ Correct"
                        )

                    else:

                        st.error(
                            "❌ Incorrect"
                        )

                    st.info(
                        f"💡 Explanation: {explanation}"
                    )

                    st.divider()

                # -------------------------------------------------
                # RETAKE QUIZ
                # -------------------------------------------------

                if st.button(
                    "🔄 Retake / New Quiz",
                    use_container_width=True
                ):

                    st.session_state.mcq_data = []
                    st.session_state.mcq_answers = {}
                    st.session_state.mcq_submitted = False
                    st.session_state.mcq_score = 0

                    st.rerun()


# =========================================================
# PLACEMENT PREP
# =========================================================

elif selected == "💼 Placement Prep":

    st.title("💼 Placement Prep")

    role = st.selectbox(
        "Target Role",
        [
            "Software Developer",
            "Electrical Engineer",
            "Electronics Engineer",
            "Data Analyst",
            "AI / ML",
            "Embedded Engineer",
            "General Placement"
        ]
    )

    preparation = st.selectbox(
        "Preparation Type",
        [
            "Interview Questions",
            "Technical Questions",
            "HR Questions",
            "Aptitude",
            "Mock Interview"
        ]
    )

    placement_question = st.text_area(
        "Question / Topic"
    )

    if st.button(
        "🚀 Start Preparation",
        use_container_width=True
    ):

        prompt = f"""
You are a college placement preparation assistant.

Role:
{role}

Preparation:
{preparation}

Student topic/question:
{placement_question}

Give useful placement preparation content.

Include:
- Question
- Best answer
- Explanation
- Interview tips
- Common mistakes
"""

        answer = ask_ai(prompt)

        st.markdown(answer)

        add_history(
            "Placement Prep",
            placement_question,
            answer
        )


# =========================================================
# HISTORY
# =========================================================

elif selected == "📜 History":

    st.title("📜 History")

    if not st.session_state.history:

        st.info(
            "No history available yet."
        )

    else:

        st.write(
            f"Total conversations: "
            f"{len(st.session_state.history)}"
        )

        if st.button(
            "🗑️ Clear History"
        ):

            st.session_state.history = []

            st.success(
                "History cleared."
            )

            st.rerun()

        for item in st.session_state.history:

            with st.expander(
                f"{item['mode']} • {item['time']}"
            ):

                st.markdown(
                    f"**Question:**\n{item['question']}"
                )

                st.markdown(
                    f"**Answer:**\n{item['answer']}"
                )


# =========================================================
# ADMIN SETTINGS
# =========================================================

elif selected == "⚙️ Admin Settings":

    # Extra security check
    if not st.session_state.admin_verified:

        st.error(
            "🔒 Admin access only."
        )

    else:

        st.title("⚙️ Admin Settings")

        st.success(
            "🔐 Admin verified"
        )

        st.divider()

        app_title = st.text_input(
            "App Title",
            value=APP_NAME
        )

        welcome_message = st.text_area(
            "Welcome Message",
            value="Welcome to Tech Mithra AI Pro!"
        )

        ai_enabled = st.toggle(
            "Enable AI",
            value=True
        )

        preferred_model = st.selectbox(
            "Preferred AI Model",
            TEXT_MODELS
        )

        st.write(
            f"**Current App Title:** {app_title}"
        )

        st.write(
            f"**AI Enabled:** {ai_enabled}"
        )

        st.write(
            f"**Preferred Model:** {preferred_model}"
        )

        st.divider()

        if st.button(
            "🗑️ Clear All Session History",
            use_container_width=True
        ):

            st.session_state.history = []
            st.session_state.chat_messages = []

            st.success(
                "History cleared successfully."
            )

        st.divider()

        st.info(
            "⚠️ Admin Settings normal users ki sidebar lo kanipinchavu. "
            "Admin login successful ayyaka matrame menu kanipistundi."
        )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "🚀 Tech Mithra AI Pro"
)

st.sidebar.caption(
    "AI Study • Projects • Exams • Placements"
)
