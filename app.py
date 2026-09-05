import streamlit as st
import json
from datetime import datetime
from PIL import Image
from google import genai

# =========================================================
# TECH MITHRA AI PRO
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro 🎓",
    page_icon="🚀",
    layout="wide"
)

APP_NAME = "Tech Mithra AI Pro"

TEXT_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
]


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

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

        return genai.Client(
            api_key=api_key
        )

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
            "time": datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),
            "mode": mode,
            "question": question,
            "answer": answer
        }
    )


def ask_ai(prompt, extra_content=None):

    if client is None:

        return (
            "⚠️ Gemini API key setup cheyyali.\n\n"
            "`.streamlit/secrets.toml` lo "
            "`GEMINI_API_KEY` add cheyyandi."
        )

    try:

        contents = [prompt]

        if extra_content:
            contents.extend(extra_content)

        response = client.models.generate_content(
            model=TEXT_MODELS[0],
            contents=contents
        )

        if response.text:
            return response.text

        return "AI response empty ga vachindi."

    except Exception as e:

        return f"❌ AI Error: {e}"


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🚀 Tech Mithra AI Pro")

menu_items = [
    "💬 AI Chat",
    "🔬 Project & Lab Guide",
    "🎉 Event Planner",
    "📚 Exam Hacker",
    "💼 Placement Prep",
    "📜 History"
]

selected = st.sidebar.radio(
    "Select Option",
    menu_items
)

st.sidebar.divider()

st.sidebar.caption(
    "AI Study • Projects • Exams • Placements"
)


# =========================================================
# AI CHAT
# =========================================================

if selected == "💬 AI Chat":

    st.title("💬 Tech Mithra AI")

    st.caption(
        "Ask anything • Upload Photo • Camera • Files"
    )

    # -----------------------------------------------------
    # PREVIOUS CHAT
    # -----------------------------------------------------

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):

            if message.get("image"):

                st.image(
                    message["image"],
                    width=300
                )

            if message.get("content"):

                st.markdown(
                    message["content"]
                )

    # -----------------------------------------------------
    # PLUS BUTTON
    # -----------------------------------------------------

    col1, col2 = st.columns(
        [1, 10]
    )

    with col1:

        if st.button(
            "➕",
            help="Upload Photo / Camera / Files"
        ):

            st.session_state.show_attachments = (
                not st.session_state.show_attachments
            )

    # -----------------------------------------------------
    # ATTACHMENTS
    # -----------------------------------------------------

    uploaded_files = []
    camera_image = None

    if st.session_state.show_attachments:

        st.info("📎 Attachments")

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

            st.write("📎 Selected Files:")

            for file in uploaded_files:

                st.write(
                    f"• {file.name}"
                )

        if camera_image:

            st.image(
                camera_image,
                caption="Camera Image",
                width=250
            )

    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    user_prompt = st.chat_input(
        "Message Tech Mithra..."
    )

    if user_prompt is not None:

        original_prompt = user_prompt

        extra_content = []

        display_image = None

        # -------------------------------------------------
        # CAMERA IMAGE
        # -------------------------------------------------

        if camera_image:

            try:

                image = Image.open(
                    camera_image
                )

                extra_content.append(
                    image
                )

                display_image = image

            except Exception:
                pass

        # -------------------------------------------------
        # UPLOADED FILES
        # -------------------------------------------------

        for file in uploaded_files:

            try:

                file_type = file.type or ""

                # IMAGE
                if file_type.startswith(
                    "image/"
                ):

                    image = Image.open(
                        file
                    )

                    extra_content.append(
                        image
                    )

                    if display_image is None:

                        display_image = image

                # TEXT / CODE
                elif (
                    file_type.startswith("text/")
                    or file.name.endswith(
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
                    )
                ):

                    text_data = file.read().decode(
                        "utf-8",
                        errors="ignore"
                    )

                    extra_content.append(
                        f"""
--- FILE: {file.name} ---

{text_data}

--- END FILE ---
"""
                    )

                else:

                    extra_content.append(
                        f"""
[File attached: {file.name}]
"""
                    )

            except Exception:

                extra_content.append(
                    f"""
[File attached: {file.name}]
"""
                )

        # -------------------------------------------------
        # ATTACHMENT WITHOUT TEXT
        # -------------------------------------------------

        if not original_prompt.strip():

            original_prompt = (
                "Analyze the attached photo/files "
                "and explain the important information "
                "in simple student-friendly language."
            )

        # -------------------------------------------------
        # SAVE USER MESSAGE
        # -------------------------------------------------

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": original_prompt,
                "image": display_image
            }
        )

        # -------------------------------------------------
        # AI RESPONSE
        # -------------------------------------------------

        answer = ask_ai(
            original_prompt,
            extra_content=extra_content
        )

        # -------------------------------------------------
        # SAVE AI RESPONSE
        # -------------------------------------------------

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        add_history(
            "AI Chat",
            original_prompt,
            answer
        )

        st.rerun()


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
        "📷 Upload Project Image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
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
                        Image.open(
                            project_image
                        )
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
4. Block Diagram Explanation
5. Working Principle
6. Step-by-Step Procedure
7. Advantages
8. Disadvantages
9. Applications
10. Result
11. Viva Questions and Answers

Use simple student-friendly language.
"""

            answer = ask_ai(
                prompt,
                extra_content=extra
            )

            st.markdown(
                answer
            )

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

- Event Objective
- Schedule
- Activities
- Required Resources
- Team Responsibilities
- Budget Categories
- Promotion Ideas
- Risk Management
- Closing Plan
"""

        answer = ask_ai(
            prompt
        )

        st.markdown(
            answer
        )

        add_history(
            "Event Planner",
            event_name,
            answer
        )


# =========================================================
# EXAM HACKER
# =========================================================

elif selected == "📚 Exam Hacker":

    st.title("📚 Exam Hacker")

    st.caption(
        "📝 Answers + 🎯 MCQs + 📊 Score"
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
            "Enter Exam Question",
            placeholder=(
                "Example: Explain working of "
                "three phase induction motor."
            )
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
- Main Explanation
- Important Points
- Examples if needed
- Conclusion

Make it easy to write in examination.
"""

                answer = ask_ai(
                    prompt
                )

                st.markdown(
                    answer
                )

                add_history(
                    "Exam Hacker",
                    exam_question,
                    answer
                )

    # =====================================================
    # MCQ QUIZ
    # =====================================================

    with tab2:

        st.subheader(
            "🎯 MCQ Practice Quiz"
        )

        subject = st.text_input(
            "📚 Subject / Topic",
            placeholder=(
                "Example: Management"
            ),
            key="mcq_subject"
        )

        number_of_questions = st.selectbox(
            "🔢 Number of MCQs",
            [
                5,
                10,
                15,
                20
            ],
            key="mcq_number"
        )

        difficulty = st.selectbox(
            "⚡ Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ],
            key="mcq_difficulty"
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
                    "Subject / Topic enter cheyyandi."
                )

            else:

                prompt = f"""
Generate exactly {number_of_questions}
multiple-choice questions for college students.

Subject:
{subject}

Difficulty:
{difficulty}

Return ONLY valid JSON.

Use exactly this format:

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

1. Every question must have exactly A, B, C, D.
2. Each option must be different.
3. answer must be only A, B, C or D.
4. Correct answer must match the option.
5. Give a short explanation.
6. Do not use Markdown.
7. Do not add text outside JSON.
"""

                try:

                    response_text = ask_ai(
                        prompt
                    )

                    response_text = (
                        response_text
                        .strip()
                    )

                    if response_text.startswith(
                        "```"
                    ):

                        response_text = (
                            response_text
                            .replace(
                                "```json",
                                ""
                            )
                            .replace(
                                "```",
                                ""
                            )
                            .strip()
                        )

                    mcqs = json.loads(
                        response_text
                    )

                    if isinstance(
                        mcqs,
                        list
                    ):

                        st.session_state.mcq_data = mcqs

                        st.session_state.mcq_answers = {}

                        st.session_state.mcq_submitted = False

                        st.session_state.mcq_score = 0

                        st.success(
                            f"✅ {len(mcqs)} MCQs Generated!"
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
        # DISPLAY MCQS
        # -------------------------------------------------

        if st.session_state.mcq_data:

            st.divider()

            st.subheader(
                "📝 Select Your Answers"
            )

            for index, mcq in enumerate(
                st.session_state.mcq_data
            ):

                question = mcq.get(
                    "question",
                    f"Question {index + 1}"
                )

                options = mcq.get(
                    "options",
                    {}
                )

                st.markdown(
                    f"""
### Q{index + 1}. {question}
"""
                )

                selected_answer = st.radio(
                    "Choose one:",
                    [
                        "A",
                        "B",
                        "C",
                        "D"
                    ],
                    format_func=lambda option,
                    opts=options: (
                        f"{option}. "
                        f"{opts.get(option, '')}"
                    ),
                    key=f"answer_{index}",
                    disabled=st.session_state.mcq_submitted
                )

                st.session_state.mcq_answers[
                    index
                ] = selected_answer

                st.divider()

            # -------------------------------------------------
            # SUBMIT
            # -------------------------------------------------

            if not st.session_state.mcq_submitted:

                if st.button(
                    "✅ SUBMIT QUIZ",
                    use_container_width=True
                ):

                    score = 0

                    for index, mcq in enumerate(
                        st.session_state.mcq_data
                    ):

                        correct_answer = str(
                            mcq.get(
                                "answer",
                                ""
                            )
                        ).upper().strip()

                        user_answer = (
                            st.session_state.mcq_answers
                            .get(index)
                        )

                        if (
                            user_answer
                            == correct_answer
                        ):

                            score += 1

                    st.session_state.mcq_score = score

                    st.session_state.mcq_submitted = True

                    total = len(
                        st.session_state.mcq_data
                    )

                    percentage = (
                        score / total * 100
                        if total
                        else 0
                    )

                    if percentage >= 80:

                        performance = (
                            "🏆 Excellent!"
                        )

                    elif percentage >= 60:

                        performance = (
                            "👏 Good!"
                        )

                    elif percentage >= 40:

                        performance = (
                            "📖 Need More Practice"
                        )

                    else:

                        performance = (
                            "💪 Keep Practicing!"
                        )

                    result = f"""
MCQ Quiz Result

Subject: {subject}

Score: {score}/{total}

Percentage: {percentage:.1f}%

Performance: {performance}
"""

                    add_history(
                        "Exam Hacker MCQ",
                        subject,
                        result
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
                    if total
                    else 0
                )

                if percentage >= 80:

                    performance = (
                        "🏆 Excellent!"
                    )

                elif percentage >= 60:

                    performance = (
                        "👏 Good!"
                    )

                elif percentage >= 40:

                    performance = (
                        "📖 Need More Practice"
                    )

                else:

                    performance = (
                        "💪 Keep Practicing!"
                    )

                st.divider()

                st.subheader(
                    "🏆 QUIZ RESULT"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Score",
                        f"{score}/{total}"
                    )

                with col2:

                    st.metric(
                        "Percentage",
                        f"{percentage:.1f}%"
                    )

                with col3:

                    st.metric(
                        "Performance",
                        performance
                    )

                st.divider()

                st.subheader(
                    "📋 Correct Answers & Explanations"
                )

                # -------------------------------------------------
                # ANSWERS
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
                        mcq.get(
                            "answer",
                            ""
                        )
                    ).upper()

                    user_answer = (
                        st.session_state.mcq_answers
                        .get(
                            index,
                            "Not Answered"
                        )
                    )

                    explanation = mcq.get(
                        "explanation",
                        "Explanation not available."
                    )

                    st.markdown(
                        f"""
### Q{index + 1}. {question}
"""
                    )

                    st.write(
                        f"**Your Answer:** "
                        f"{user_answer}"
                    )

                    st.write(
                        f"**Correct Answer:** "
                        f"{correct}. "
                        f"{options.get(correct, '')}"
                    )

                    if (
                        user_answer
                        == correct
                    ):

                        st.success(
                            "✅ Correct Answer"
                        )

                    else:

                        st.error(
                            "❌ Wrong Answer"
                        )

                    st.info(
                        f"💡 Explanation: "
                        f"{explanation}"
                    )

                    st.divider()

                # -------------------------------------------------
                # NEW QUIZ
                # -------------------------------------------------

                if st.button(
                    "🔄 START NEW QUIZ",
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
        "🎯 Target Role",
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
        "📚 Preparation Type",
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
- Best Answer
- Explanation
- Interview Tips
- Common Mistakes
"""

        answer = ask_ai(
            prompt
        )

        st.markdown(
            answer
        )

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
            f"Total Records: "
            f"{len(st.session_state.history)}"
        )

        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            st.session_state.history = []

            st.success(
                "History cleared successfully."
            )

            st.rerun()

        for item in st.session_state.history:

            with st.expander(
                f"{item['mode']} • "
                f"{item['time']}"
            ):

                st.markdown(
                    f"**Question:**\n"
                    f"{item['question']}"
                )

                st.markdown(
                    f"**Answer:**\n"
                    f"{item['answer']}"
                )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "🚀 Tech Mithra AI Pro"
)
