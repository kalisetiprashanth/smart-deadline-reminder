
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Smart Deadline Reminder",
    page_icon="⏰"
)

st.title("⏰ Smart Deadline Reminder")
st.write("Manage your tasks and never miss a deadline!")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.subheader("Add a New Task")

task_name = st.text_input("Enter task name")
deadline = st.date_input(
    "Select deadline",
    min_value=date.today()
)

priority = st.selectbox(
    "Select priority",
    ["High", "Medium", "Low"]
)

if st.button("Add Task"):
    if task_name.strip():
        st.session_state.tasks.append({
            "name": task_name.strip(),
            "deadline": deadline,
            "priority": priority,
            "done": False
        })
        st.success("Task added successfully!")
    else:
        st.warning("Please enter a task name.")

st.subheader("My Tasks")

if not st.session_state.tasks:
    st.info("No tasks added yet. Add your first task!")

for i, task in enumerate(st.session_state.tasks):
    with st.container(border=True):
        st.write("**Task:**", task["name"])
        st.write("**Deadline:**", task["deadline"])
        st.write("**Priority:**", task["priority"])

        if task["done"]:
            st.success("Completed")
        else:
            remaining = (task["deadline"] - date.today()).days

            if remaining < 0:
                st.error("Deadline missed!")
            elif remaining == 0:
                st.warning("Deadline is today!")
            else:
                st.write(f"Days remaining: {remaining}")

            if st.button("Mark Completed", key=f"done_{i}"):
                st.session_state.tasks[i]["done"] = True
                st.rerun()
