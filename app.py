
import streamlit as st
import json
import os
from datetime import date, datetime

st.set_page_config(
    page_title="Smart Deadline Reminder",
    page_icon="⏰",
    layout="wide"
)

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)

            for task in tasks:
                task["deadline"] = date.fromisoformat(
                    task["deadline"]
                )

            return tasks
        except (json.JSONDecodeError, ValueError, KeyError):
            return []
    return []


def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(
            st.session_state.tasks,
            file,
            default=str,
            indent=4
        )


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()


st.title("⏰ Smart Deadline Reminder")
st.write("Plan your work. Track your deadlines. Stay organized!")

st.divider()

# Dashboard
st.header("📊 Dashboard")

total = len(st.session_state.tasks)
completed = sum(
    1 for task in st.session_state.tasks
    if task["completed"]
)
pending = total - completed

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total)
col2.metric("Completed Tasks", completed)
col3.metric("Pending Tasks", pending)

st.divider()

# Add new task
st.header("➕ Add New Task")

with st.form("task_form"):
    task_name = st.text_input("Enter task name")

    deadline = st.date_input(
        "Select deadline",
        min_value=date.today()
    )

    priority = st.selectbox(
        "Select priority",
        ["High", "Medium", "Low"]
    )

    add_task = st.form_submit_button("Add Task")

if add_task:
    if task_name.strip():
        st.session_state.tasks.append({
            "name": task_name.strip(),
            "deadline": deadline,
            "priority": priority,
            "completed": False
        })

        save_tasks()
        st.success("Task added successfully!")
        st.rerun()
    else:
        st.warning("Please enter a task name.")

st.divider()

# Display tasks
st.header("📋 My Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add your first task above!")
else:
    for i, task in enumerate(st.session_state.tasks):
        with st.container(border=True):
            left, right = st.columns([3, 1])

            with left:
                st.subheader(task["name"])
                st.write("📅 Deadline:", task["deadline"])
                st.write("🎯 Priority:", task["priority"])

                if task["completed"]:
                    st.success("Completed ✅")
                else:
                    days_left = (
                        task["deadline"] - date.today()
                    ).days

                    if days_left < 0:
                        st.error("Deadline missed!")
                    elif days_left == 0:
                        st.warning("Deadline is today!")
                    else:
                        st.info(
                            f"{days_left} day(s) remaining"
                        )

            with right:
                if not task["completed"]:
                    if st.button(
                        "Mark Completed",
                        key=f"complete_{i}"
                    ):
                        st.session_state.tasks[i][
                            "completed"
                        ] = True

                        save_tasks()
                        st.rerun()

                if st.button("Delete Task", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    save_tasks()
                    st.rerun()

st.divider()
st.caption("Smart Deadline Reminder | Stay productive!")
python -m streamlit run app.py
