from pawpal_system import Pet, Task, Owner, Schedule

p1 = Pet("max", "dog")
p2 = Pet("Hunna", "Spider")

# Tasks added out of order (late times first, then early)
# t3 "walk" starts at 07:00 and takes 30 min  → ends 07:30
# t5 "feed" starts at 07:15 and takes 15 min  → ends 07:30  ← overlaps with walk
# t4 "tv"   starts at 11:00 and takes 100 min → ends 12:40
# t1 "wash" starts at 11:30 and takes 200 min → ends 14:50  ← overlaps with tv
t1 = Task("wash",   200, "high",   "Hunna", time="11:30")
t2 = Task("kisses",  20, "low",    "max",   time="09:30")
t3 = Task("walk",    30, "medium", "max",   time="07:00")
t4 = Task("tv",     100, "medium", "Hunna", time="11:00")
t5 = Task("feed",    15, "high",   "max",   time="07:15")

bobby = Owner("Bobby", "", [p1, p2], [t1, t2, t3])
bobby.add_task(t4)
bobby.add_task(t5)

# Mark one task complete so filtering by status is meaningful
t2.mark_complete()

SunnyDaySched = Schedule(bobby, 500)

# --- Generated schedule (priority-sorted) ---
schedule = SunnyDaySched.generate_schedule()
print(f"\n{'='*40}")
print(f"  PawPal Schedule for {bobby.name}")
print(f"{'='*40}")
for task in schedule:
    print(f"  [{task.priority.upper():6}] {task.title:<10} ({task.time_to_complete} min) — {task.pet_name}")

# --- Sorted by time (HH:MM) ---
print(f"\n{'='*40}")
print("  Tasks sorted by scheduled time")
print(f"{'='*40}")
for task in SunnyDaySched.sort_by_time():
    status = "done" if task.completed else "    "
    print(f"  {task.time}  [{status}]  {task.title:<10} — {task.pet_name}")

# --- Filter: max's tasks only ---
print(f"\n{'='*40}")
print("  Max's tasks only")
print(f"{'='*40}")
for task in bobby.filter_tasks(pet_name="max"):
    print(f"  {task.title:<10} ({task.priority}) — completed: {task.completed}")

# --- Filter: incomplete tasks only ---
print(f"\n{'='*40}")
print("  Incomplete tasks only")
print(f"{'='*40}")
for task in bobby.filter_tasks(completed=False):
    print(f"  {task.title:<10} — {task.pet_name}")

# --- Conflict detection ---
print(f"\n{'='*40}")
print("  Conflict Detection")
print(f"{'='*40}")
conflicts = SunnyDaySched.detect_conflicts()
if conflicts:
    for msg in conflicts:
        print(f"  {msg}")
else:
    print("  No conflicts found.")
print(f"{'='*40}\n")
