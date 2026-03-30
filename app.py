import streamlit as st
from pawpal_system import Pet, Task, Owner, Schedule


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None

st.divider()

# --- Owner & Pet Setup ---
st.subheader("Owner & Pets")

col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Create Owner"):
    pet = Pet(pet_name, species)
    st.session_state.owner = Owner(owner_name, "", [pet], [])
    st.success(f"Owner '{owner_name}' created with pet '{pet_name}'.")

if st.session_state.owner:
    st.info(f"Owner: **{st.session_state.owner.name}** | Pets: {[p.name for p in st.session_state.owner.pets]}")

    st.markdown("#### Add another pet")
    col1, col2 = st.columns(2)
    with col1:
        new_pet_name = st.text_input("New pet name", value="")
    with col2:
        new_species = st.selectbox("New pet species", ["dog", "cat", "other"], key="new_species")

    if st.button("Add pet"):
        st.session_state.owner.add_pet(Pet(new_pet_name, new_species))
        st.success(f"Pet '{new_pet_name}' added.")

st.divider()

# --- Tasks ---
st.subheader("Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    pet_names = [p.name for p in st.session_state.owner.pets] if st.session_state.owner else []
    task_pet = st.selectbox("For pet", pet_names if pet_names else ["(create owner first)"])

if st.button("Add task"):
    if st.session_state.owner is None:
        st.error("Create an owner first.")
    else:
        task = Task(task_title, int(duration), priority, task_pet)
        st.session_state.owner.add_task(task)
        st.success(f"Task '{task_title}' added for {task_pet}.")

if st.session_state.owner and st.session_state.owner.tasks:
    st.write("Current tasks:")
    st.table([
        {"title": t.title, "pet": t.pet_name, "duration (min)": t.time_to_complete, "priority": t.priority}
        for t in st.session_state.owner.tasks
    ])
else:
    st.info("No tasks yet. Create an owner and add tasks above.")

st.divider()

# --- Schedule ---
st.subheader("Build Schedule")
available_minutes = st.number_input("Available time (minutes)", min_value=1, max_value=1440, value=480)

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.error("Create an owner first.")
    elif not st.session_state.owner.tasks:
        st.error("Add at least one task first.")
    else:
        st.session_state.schedule = Schedule(st.session_state.owner, int(available_minutes))
        result = st.session_state.schedule.generate_schedule()
        st.success("Schedule generated!")
        st.table([
            {"priority": t.priority.upper(), "title": t.title, "duration (min)": t.time_to_complete, "pet": t.pet_name}
            for t in result
        ])
