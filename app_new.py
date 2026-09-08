import streamlit as st
from datetime import date

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="My To-Do List",
    page_icon="✅",
    layout="centered"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #dff3ff, #f7fbff);
}

/* Main content */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #123b5d !important;
}

/* Normal text */
[data-testid="stMarkdownContainer"] p {
    color: #183b56 !important;
}

/* Labels */
[data-testid="stWidgetLabel"] p {
    color: #183b56 !important;
    font-weight: 600;
}

/* Text input */
input {
    color: #ffffff !important;
    background-color: #3b6ea5 !important;
}

input::placeholder {
    color: #e8f3ff !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background-color: #3b6ea5 !important;
    color: #ffffff !important;
}

[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* Date input */
[data-baseweb="input"] {
    background-color: #3b6ea5 !important;
}

[data-baseweb="input"] input {
    color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    background-color: #3b82d0 !important;
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

/* Task cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 14px;
    padding: 8px;
}

/* Metrics */
div[data-testid="stMetricValue"] {
    color: #123b5d !important;
}

div[data-testid="stMetricLabel"] {
    color: #36566d !important;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #36566d !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align: center;'>✨ My To-Do List ✨</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>"
    "Stay organized • Get things done 💙"
    "</p>",
    unsafe_allow_html=True
)


# ---------------- STORE TASKS ----------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []


# ---------------- ADD TASK ----------------
st.subheader("📝 Add a New Task")

task = st.text_input(
    "What do you need to do?",
    placeholder="Enter your task here..."
)

col1, col2 = st.columns(2)

with col1:
    priority = st.selectbox(
        "⭐ Priority",
        ["High", "Medium", "Low"]
    )

with col2:
    deadline = st.date_input(
        "📅 Deadline",
        value=date.today()
    )


if st.button("➕ Add Task", use_container_width=True):

    if task.strip():

        new_task = {
            "task": task.strip(),
            "priority": priority,
            "deadline": deadline,
            "completed": False
        }

        st.session_state.tasks.append(new_task)

        st.success("Task added successfully! 🎉")

    else:
        st.warning("Please enter a task.")


# ==================================================
# SELECT DATE
# ==================================================

st.subheader("📅 View Tasks by Date")

selected_date = st.date_input(
    "Select a date to see your tasks",
    value=date.today()
)


# ==================================================
# FILTER TASKS BY SELECTED DATE
# ==================================================

date_tasks = [
    task for task in st.session_state.tasks
    if task["deadline"] == selected_date
]


# ==================================================
# PROGRESS FOR SELECTED DATE
# ==================================================

total_tasks = len(date_tasks)

completed_tasks = sum(
    1 for task in date_tasks
    if task["completed"]
)

pending_tasks = total_tasks - completed_tasks


st.subheader(
    f"📊 Progress for {selected_date.strftime('%d %b %Y')}"
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📋 Total",
        total_tasks
    )

with col2:
    st.metric(
        "✅ Completed",
        completed_tasks
    )

with col3:
    st.metric(
        "⏳ Pending",
        pending_tasks
    )


if total_tasks > 0:

    progress = completed_tasks / total_tasks

    st.progress(progress)

    st.caption(
        f"{completed_tasks} of {total_tasks} tasks completed"
    )


# ==================================================
# SEARCH TASKS
# ==================================================

st.subheader("🔍 Search Tasks")

search = st.text_input(
    "Search",
    placeholder="Search tasks for this date..."
)


# ==================================================
# SORT TASKS
# ==================================================

sort_option = st.selectbox(
    "🔃 Sort tasks by",
    ["Default", "Priority", "Deadline"]
)


priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}


display_tasks = date_tasks.copy()


# ---------------- SORTING ----------------

if sort_option == "Priority":

    display_tasks.sort(
        key=lambda x: priority_order[x["priority"]]
    )

elif sort_option == "Deadline":

    display_tasks.sort(
        key=lambda x: x["deadline"]
    )


# ==================================================
# MY TASKS
# ==================================================

st.subheader(
    f"📋 Tasks for {selected_date.strftime('%d %b %Y')}"
)


if display_tasks:

    found_task = False

    for current_task in display_tasks:

        # ---------------- LINEAR SEARCH ----------------
        if search.lower() not in current_task["task"].lower():
            continue

        found_task = True

        original_index = st.session_state.tasks.index(
            current_task
        )


        # ---------------- TASK CARD ----------------
        with st.container(border=True):

            col1, col2, col3 = st.columns([5, 1, 1])


            # ---------------- TASK DETAILS ----------------
            with col1:

                if current_task["completed"]:

                    st.markdown(
                        f"~~**{current_task['task']}**~~"
                    )

                    st.caption(
                        f"✅ Completed  •  "
                        f"⭐ {current_task['priority']}  •  "
                        f"📅 {current_task['deadline']}"
                    )

                else:

                    st.markdown(
                        f"**{current_task['task']}**"
                    )

                    st.caption(
                        f"⭐ {current_task['priority']}  •  "
                        f"📅 {current_task['deadline']}"
                    )


            # ---------------- COMPLETE ----------------
            with col2:

                if not current_task["completed"]:

                    if st.button(
                        "☑️",
                        key=f"complete_{original_index}"
                    ):

                        st.session_state.tasks[
                            original_index
                        ]["completed"] = True

                        st.rerun()

                else:

                    st.write("✅")


            # ---------------- DELETE ----------------
            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_{original_index}"
                ):

                    st.session_state.tasks.pop(
                        original_index
                    )

                    st.rerun()


    if not found_task:

        st.info(
            "🔍 No matching tasks found for this date."
        )


else:

    st.info(
        f"📅 No tasks planned for "
        f"{selected_date.strftime('%d %b %Y')}."
    )