import streamlit as st
import json
from datetime import datetime
from PIL import Image
from google import genai

# ============================================================
# TECH MITHRA AI PRO
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro 🎓",
    page_icon="🚀",
    layout="wide"
)

APP_NAME = "Tech Mithra AI Pro"

# Current Gemini models
TEXT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]

# ============================================================
# SESSION STATE
# ============================================================

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


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)


# ============================================================
# HISTORY
# ============================================================

def add_history(mode, question, answer):
    st.session_state.history.insert(
        0,
        {
            "time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "mode": mode,
            "question": question,
            "answer": answer
        }
    )


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(prompt, extra_content=None):

    try:
        client = get_client()

        contents = [prompt]

        if extra_content:
            contents.extend(extra_content)

        last_error = None

        for model in TEXT_MODELS:

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=contents
                )

                if response and response.text:
                    return response.text

            except Exception as e:
                last_error = e

        return f"❌ AI Error: {last_error}"

    except Exception as e:
        return f"❌ AI Error: {e}"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI Pro")

    st.caption("AI Study & Career Assistant")

    st.divider()

    menu_items = [
        "💬 AI Chat",
        "🔬 Project & Lab Guide",
        "🎉 Event Planner",
        "📚 Exam Hacker",
        "💼 Placement Prep",
        "📜 History"
    ]

    selected = st.radio(
        "Choose Feature",
        menu_items
    )

    st.divider()

    st.info(
        "🎓 Tech Mithra AI Pro\n\n"
        "AI-powered learning assistant for students."
    )


# ============================================================
# COMMON HEADER
# ============================================================

st.title("🚀 Tech Mithra AI Pro")


# ============================================================
# AI CHAT
# ============================================================

if selected == "💬 AI Chat":

    st.subheader("💬 AI Chat")

    st.caption(
        "Ask questions, upload photos/files, or use your camera."
    )

    # Display previous chat
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Attachment button
    col1, col2 = st.columns([1, 8])

    with col1:

        if st.button(
            "➕",
            help="Attachments"
        ):
            st.session_state.show_attachments = (
                not st.session_state.show_attachments
            )

    # Attachment area
    uploaded_files = []
    camera_image = None

    if st.session_state.show_attachments:

        st.markdown("### 📎 Attachments")

        uploaded_files = st.file_uploader(
            "Upload Photo / File",
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
            "📸 Take Photo"
        )

    # Chat input
    user_prompt = st.chat_input(
        "Message Tech Mithra..."
    )

    if user_prompt:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(user_prompt)

        extra_content = []

        # Uploaded files
        if uploaded_files:

            for uploaded_file in uploaded_files:

                file_type = uploaded_file.type or ""

                try:

                    if file_type.startswith("image/"):

                        image = Image.open(uploaded_file)

                        extra_content.append(image)

                    elif uploaded_file.name.lower().endswith(
                        (
                            ".txt",
                            ".py",
                            ".java",
                            ".c",
                            ".cpp",
                            ".html",
                            ".css",
                            ".js",
                            ".json",
                            ".csv",
                            ".md"
                        )
                    ):

                        text_data = uploaded_file.read().decode(
                            "utf-8",
                            errors="ignore"
                        )

                        extra_content.append(
                            f"\n\nFILE: {uploaded_file.name}\n{text_data}"
                        )

                    else:

                        extra_content.append(
                            f"\nUploaded file: {uploaded_file.name}"
                        )

                except Exception as e:

                    extra_content.append(
                        f"\nCould not read {uploaded_file.name}: {e}"
                    )

        # Camera
        if camera_image:

            try:

                image = Image.open(camera_image)

                extra_content.append(image)

            except Exception as e:

                extra_content.append(
                    f"Camera image error: {e}"
                )

        # AI response
        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                answer = ask_ai(
                    f"""
You are Tech Mithra AI Pro, a helpful AI assistant for students.

Answer the user's question clearly and accurately.

User question:
{user_prompt}

Give a student-friendly answer.
Use headings, bullets and examples when useful.
""",
                    extra_content
                )

            st.markdown(answer)

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


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif selected == "🔬 Project & Lab Guide":

    st.subheader("🔬 Project & Lab Guide")

    st.write(
        "Enter your project/lab topic and optionally upload a photo."
    )

    topic = st.text_input(
        "Project / Lab Topic",
        placeholder="Example: Automatic Solar Street Light"
    )

    project_image = st.file_uploader(
        "📷 Upload Project Photo (Optional)",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if st.button(
        "🚀 Generate Project Guide",
        use_container_width=True
    ):

        if not topic:

            st.warning(
                "⚠️ Please enter a project or lab topic."
            )

        else:

            extra = []

            if project_image:

                try:

                    image = Image.open(project_image)

                    extra.append(image)

                except Exception:
                    pass

            prompt = f"""
You are an expert engineering project and laboratory guide.

Create a complete student-friendly guide for:

PROJECT / LAB:
{topic}

Include:

1. Title
2. Aim
3. Introduction
4. Objectives
5. Components / Requirements
6. Block diagram description
7. Circuit / System explanation
8. Working principle
9. Step-by-step procedure
10. Algorithm
11. Advantages
12. Disadvantages
13. Applications
14. Safety precautions
15. Expected result
16. Viva questions with answers
17. Future scope

Keep the explanation simple and suitable for college students.
"""

            with st.spinner("🔬 Preparing project guide..."):

                answer = ask_ai(
                    prompt,
                    extra
                )

            st.markdown(answer)

            add_history(
                "Project & Lab Guide",
                topic,
                answer
            )


# ============================================================
# EVENT PLANNER
# ============================================================

elif selected == "🎉 Event Planner":

    st.subheader("🎉 Event Planner")

    event_name = st.text_input(
        "Event Name",
        placeholder="Example: Technical Fest 2026"
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Technical Event",
            "College Fest",
            "Workshop",
            "Seminar",
            "Cultural Event",
            "Sports Event",
            "Farewell",
            "Freshers Event",
            "Hackathon",
            "Other"
        ]
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="Example: EEE Students"
    )

    if st.button(
        "🎯 Generate Event Plan",
        use_container_width=True
    ):

        if not event_name:

            st.warning(
                "⚠️ Please enter event name."
            )

        else:

            prompt = f"""
You are a professional college event planner.

Create a detailed event plan.

Event Name:
{event_name}

Event Type:
{event_type}

Target Audience:
{audience}

Include:

1. Event objective
2. Theme ideas
3. Complete schedule
4. Registration plan
5. Volunteer responsibilities
6. Stage arrangement
7. Required materials
8. Technical requirements
9. Budget categories
10. Promotion ideas
11. Social media promotion
12. Prize ideas
13. Guest coordination
14. Food and refreshments
15. Safety arrangements
16. Certificate plan
17. Closing ceremony
18. Final checklist

Make it practical for a college.
"""

            with st.spinner("🎉 Creating event plan..."):

                answer = ask_ai(prompt)

            st.markdown(answer)

            add_history(
                "Event Planner",
                event_name,
                answer
            )


# ============================================================
# EXAM HACKER
# ============================================================

elif selected == "📚 Exam Hacker":

    st.subheader("📚 Exam Hacker")

    tab1, tab2 = st.tabs(
        [
            "✍️ Answer Generator",
            "🧠 MCQ Quiz"
        ]
    )

    # ========================================================
    # ANSWER GENERATOR
    # ========================================================

    with tab1:

        st.markdown("### ✍️ Exam Answer Generator")

        question = st.text_area(
            "Enter your question",
            height=150,
            placeholder="Example: Explain evolution of management."
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
            "📝 Generate Answer",
            use_container_width=True
        ):

            if not question:

                st.warning(
                    "⚠️ Please enter a question."
                )

            else:

                prompt = f"""
You are an expert college exam answer writer.

Question:
{question}

Marks:
{marks}

Generate an exam-ready answer.

Requirements:

- Simple language
- Clear headings
- Important points
- Definitions where required
- Examples where useful
- Suitable length for {marks}
- Easy to memorize
- Use bullet points or numbering where appropriate
"""

                with st.spinner("✍️ Writing exam answer..."):

                    answer = ask_ai(prompt)

                st.markdown(answer)

                add_history(
                    "Exam Answer",
                    question,
                    answer
                )

    # ========================================================
    # MCQ QUIZ
    # ========================================================

    with tab2:

        st.markdown("### 🧠 MCQ Quiz")

        mcq_topic = st.text_input(
            "MCQ Topic",
            placeholder="Example: Management Principles"
        )

        mcq_count = st.selectbox(
            "Number of Questions",
            [5, 10, 15, 20]
        )

        if st.button(
            "🎯 Generate MCQs",
            use_container_width=True
        ):

            if not mcq_topic:

                st.warning(
                    "⚠️ Please enter a topic."
                )

            else:

                prompt = f"""
Create {mcq_count} multiple choice questions for college students.

Topic:
{mcq_topic}

Return ONLY valid JSON.

Format:

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

- Exactly {mcq_count} questions
- Four options per question
- Only one correct answer
- Answer must be A, B, C or D
- No markdown
- No ```json
"""

                with st.spinner(
                    "🧠 Generating MCQs..."
                ):

                    raw = ask_ai(prompt)

                try:

                    clean = raw.strip()

                    if clean.startswith("```"):

                        clean = clean.replace(
                            "```json",
                            ""
                        )

                        clean = clean.replace(
                            "```",
                            ""
                        )

                    start = clean.find("[")

                    end = clean.rfind("]")

                    if start != -1 and end != -1:

                        clean = clean[start:end + 1]

                    data = json.loads(clean)

                    st.session_state.mcq_data = data

                    st.session_state.mcq_answers = {}

                    st.session_state.mcq_submitted = False

                    st.session_state.mcq_score = 0

                    st.success(
                        f"✅ {len(data)} MCQs generated!"
                    )

                except Exception as e:

                    st.error(
                        f"❌ MCQ generation error: {e}"
                    )

                    st.code(raw)

        # ====================================================
        # DISPLAY QUESTIONS
        # ====================================================

        if st.session_state.mcq_data:

            st.divider()

            st.markdown(
                "## 📝 Answer the Questions"
            )

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

                option_keys = [
                    "A",
                    "B",
                    "C",
                    "D"
                ]

                available_options = []

                for key in option_keys:

                    if key in options:

                        available_options.append(
                            key
                        )

                selected_answer = st.radio(
                    "Select answer:",
                    available_options,
                    format_func=lambda x:
                        f"{x}. {options.get(x, '')}",
                    key=f"mcq_{index}"
                )

                st.session_state.mcq_answers[
                    index
                ] = selected_answer

            st.divider()

            if st.button(
                "✅ Submit Quiz",
                use_container_width=True
            ):

                score = 0

                for index, mcq in enumerate(
                    st.session_state.mcq_data
                ):

                    correct = str(
                        mcq.get(
                            "answer",
                            ""
                        )
                    ).upper().strip()

                    selected_answer = str(
                        st.session_state.mcq_answers.get(
                            index,
                            ""
                        )
                    ).upper().strip()

                    if selected_answer == correct:

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

                result_text = (
                    f"Score: {score}/{total}\n"
                    f"Percentage: {percentage:.1f}%"
                )

                add_history(
                    "MCQ Quiz",
                    mcq_topic,
                    result_text
                )

            # =================================================
            # RESULT
            # =================================================

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

                st.divider()

                st.markdown(
                    "## 🏆 Quiz Result"
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

                    if percentage >= 80:

                        performance = "🔥 Excellent"

                    elif percentage >= 60:

                        performance = "👍 Good"

                    elif percentage >= 40:

                        performance = "📈 Average"

                    else:

                        performance = "💪 Need Practice"

                    st.metric(
                        "Performance",
                        performance
                    )

                st.divider()

                st.markdown(
                    "## 📖 Correct Answers & Explanations"
                )

                for index, mcq in enumerate(
                    st.session_state.mcq_data
                ):

                    correct = str(
                        mcq.get(
                            "answer",
                            ""
                        )
                    ).upper()

                    selected_answer = str(
                        st.session_state.mcq_answers.get(
                            index,
                            "Not answered"
                        )
                    ).upper()

                    st.markdown(
                        f"### Q{index + 1}"
                    )

                    if selected_answer == correct:

                        st.success(
                            f"✅ Your Answer: {selected_answer}"
                        )

                    else:

                        st.error(
                            f"❌ Your Answer: {selected_answer}"
                        )

                    st.info(
                        f"✅ Correct Answer: {correct}"
                    )

                    explanation = mcq.get(
                        "explanation",
                        "No explanation available."
                    )

                    st.write(
                        f"💡 Explanation: {explanation}"
                    )

                st.divider()

                if st.button(
                    "🔄 New Quiz",
                    use_container_width=True
                ):

                    st.session_state.mcq_data = []

                    st.session_state.mcq_answers = {}

                    st.session_state.mcq_submitted = False

                    st.session_state.mcq_score = 0

                    st.rerun()


# ============================================================
# PLACEMENT PREP
# ============================================================

elif selected == "💼 Placement Prep":

    st.subheader("💼 Placement Prep")

    role = st.selectbox(
        "Target Role",
        [
            "Software Engineer",
            "Electrical Engineer",
            "Electronics Engineer",
            "Data Analyst",
            "Cloud Engineer",
            "AI / ML Engineer",
            "Embedded Engineer",
            "PLC / Automation Engineer",
            "Other"
        ]
    )

    prep_type = st.selectbox(
        "Preparation Type",
        [
            "Interview Questions",
            "Technical Questions",
            "HR Questions",
            "Aptitude",
            "Resume Preparation",
            "Group Discussion",
            "Mock Interview"
        ]
    )

    placement_topic = st.text_input(
        "Topic / Question",
        placeholder="Example: Transformer interview questions"
    )

    if st.button(
        "🚀 Start Placement Prep",
        use_container_width=True
    ):

        prompt = f"""
You are an expert placement trainer.

Target Role:
{role}

Preparation Type:
{prep_type}

Topic:
{placement_topic}

Create useful placement preparation material.

Include:

1. Important concepts
2. Frequently asked questions
3. Answers
4. Technical points
5. Interview tips
6. Common mistakes
7. Practice questions
8. HR tips if relevant
9. Final preparation checklist

Use simple language suitable for college students.
"""

        with st.spinner(
            "💼 Preparing placement material..."
        ):

            answer = ask_ai(prompt)

        st.markdown(answer)

        add_history(
            "Placement Prep",
            placement_topic or prep_type,
            answer
        )


# ============================================================
# HISTORY
# ============================================================

elif selected == "📜 History":

    st.subheader("📜 History")

    if not st.session_state.history:

        st.info(
            "📭 No history available yet."
        )

    else:

        st.write(
            f"Total activities: {len(st.session_state.history)}"
        )

        for i, item in enumerate(
            st.session_state.history
        ):

            with st.expander(
                f"{i + 1}. {item['mode']} — {item['time']}"
            ):

                st.markdown(
                    "**Question / Topic:**"
                )

                st.write(
                    item["question"]
                )

                st.markdown(
                    "**Answer / Result:**"
                )

                st.markdown(
                    item["answer"]
                )

        st.divider()

        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            st.session_state.history = []

            st.success(
                "✅ History cleared."
            )

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚀 Tech Mithra AI Pro • AI-powered student assistant"
)
