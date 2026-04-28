import streamlit as st
from pawpal_system import Pet, Task, Owner, Schedule
from rag import get_ai_suggestions


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart pet care planning assistant.")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None

st.divider()

# -------------------------------------------------------------------------
# Owner & Pet Setup
# -------------------------------------------------------------------------
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
    st.session_state.schedule = None
    st.success(f"Owner '{owner_name}' created with pet '{pet_name}'.")

if st.session_state.owner:
    owner = st.session_state.owner
    pet_list = ", ".join(f"**{p.name}** ({p.animal})" for p in owner.pets)
    st.info(f"Owner: **{owner.name}** | Pets: {pet_list}")

    with st.expander("Add another pet"):
        col1, col2 = st.columns(2)
        with col1:
            new_pet_name = st.text_input("New pet name")
        with col2:
            new_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_species")
        if st.button("Add pet"):
            if new_pet_name.strip():
                owner.add_pet(Pet(new_pet_name.strip(), new_species))
                st.success(f"Pet '{new_pet_name}' added.")
            else:
                st.error("Enter a pet name before adding.")

st.divider()

# -------------------------------------------------------------------------
# AI Care Suggestions (RAG)
# -------------------------------------------------------------------------
st.subheader("AI Care Suggestions")

if st.session_state.owner:
    owner = st.session_state.owner
    col1, col2, col3 = st.columns(3)
    with col1:
        suggest_pet = st.selectbox("Select pet", [p.name for p in owner.pets], key="suggest_pet")
    with col2:
        suggest_breed = st.text_input("Breed (e.g. Golden Retriever)", key="suggest_breed")
    with col3:
        suggest_age = st.number_input("Age (years)", min_value=0, max_value=20, value=3, key="suggest_age")

    if st.button("Get AI Suggestions"):
        if not suggest_breed.strip():
            st.error("Enter a breed to get suggestions.")
        else:
            with st.spinner("Looking up breed facts and generating suggestions..."):
                suggestions = get_ai_suggestions(suggest_breed.strip(), int(suggest_age))
            st.success("Here's what the AI found:")
            st.markdown(suggestions)
else:
    st.info("Create an owner first to get AI suggestions.")

st.divider()

# -------------------------------------------------------------------------
# Task Entry
# -------------------------------------------------------------------------
st.subheader("Add a Task")

owner = st.session_state.owner
pet_names = [p.name for p in owner.pets] if owner else []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=480, value=30)
with col3:
    task_time = st.text_input("Start time (HH:MM)", value="08:00")

col4, col5, col6 = st.columns(3)
with col4:
    priority = st.selectbox("Priority", ["high", "medium", "low"])
with col5:
    task_pet = st.selectbox("For pet", pet_names if pet_names else ["(create owner first)"])
with col6:
    recur_days = st.number_input("Repeats every N days (0 = never)", min_value=0, max_value=30, value=0)

if st.button("Add task"):
    if owner is None:
        st.error("Create an owner first.")
    elif not task_title.strip():
        st.error("Task title cannot be empty.")
    else:
        task = Task(
            title=task_title.strip(),
            time_to_complete=int(duration),
            priority=priority,
            pet_name=task_pet,
            time=task_time,
            recur_days=int(recur_days),
        )
        owner.add_task(task)
        st.success(f"Task '{task_title}' added for {task_pet} at {task_time}.")

st.divider()

# -------------------------------------------------------------------------
# Current Tasks: filter + sorted view
# -------------------------------------------------------------------------
st.subheader("Current Tasks")

if owner and owner.tasks:
    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox(
            "Filter by pet",
            ["All pets"] + [p.name for p in owner.pets],
            key="filter_pet",
        )
    with col2:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed"],
            key="filter_status",
        )

    pet_arg = None if filter_pet == "All pets" else filter_pet
    status_arg = None if filter_status == "All" else (filter_status == "Completed")
    filtered = owner.filter_tasks(pet_name=pet_arg, completed=status_arg)

    if filtered:
        sched = Schedule(owner)
        sorted_tasks = sorted(
            filtered,
            key=lambda t: tuple(int(x) for x in t.time.split(":")),
        )
        st.table([
            {
                "time": t.time,
                "title": t.title,
                "pet": t.pet_name,
                "duration (min)": t.time_to_complete,
                "priority": t.priority.upper(),
                "recurring": f"every {t.recur_days}d" if t.recur_days else "no",
                "done": "yes" if t.completed else "no",
            }
            for t in sorted_tasks
        ])
    else:
        st.info("No tasks match that filter.")
else:
    st.info("No tasks yet. Add tasks above.")

st.divider()

# -------------------------------------------------------------------------
# Schedule Builder
# -------------------------------------------------------------------------
st.subheader("Build Schedule")

available_minutes = st.number_input(
    "Available time today (minutes)", min_value=1, max_value=1440, value=480
)

if st.button("Generate schedule"):
    if owner is None:
        st.error("Create an owner first.")
    elif not owner.tasks:
        st.error("Add at least one task first.")
    else:
        sched = Schedule(owner, int(available_minutes))
        st.session_state.schedule = sched

        # --- Conflict warnings first ---
        conflicts = sched.detect_conflicts()
        if conflicts:
            st.warning(
                f"**{len(conflicts)} scheduling conflict(s) detected** — "
                "review before confirming this plan:"
            )
            for msg in conflicts:
                # Strip the leading "WARNING: " prefix for a cleaner UI label
                detail = msg.replace("WARNING: ", "")
                st.error(f"Conflict: {detail}")

        # --- Scheduled tasks sorted by start time ---
        result = sched.generate_schedule()
        if result:
            st.success(
                f"Schedule generated — {len(result)} task(s) fit within "
                f"{available_minutes} minutes."
            )
            time_sorted = sched.sort_by_time()
            scheduled_titles = {t.title for t in result}
            display = [t for t in time_sorted if t.title in scheduled_titles]

            st.table([
                {
                    "start": t.time,
                    "title": t.title,
                    "pet": t.pet_name,
                    "duration (min)": t.time_to_complete,
                    "priority": t.priority.upper(),
                }
                for t in display
            ])

            # --- Skipped tasks ---
            skipped = [t for t in owner.tasks if t.title not in scheduled_titles and not t.completed]
            if skipped:
                st.warning(
                    f"{len(skipped)} task(s) could not fit in today's schedule:"
                )
                for t in skipped:
                    st.caption(f"- {t.title} ({t.time_to_complete} min, {t.priority} priority) for {t.pet_name}")
        else:
            st.error("No tasks fit within the available time.")
