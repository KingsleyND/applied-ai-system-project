from dataclasses import dataclass, field
from typing import List, Literal


@dataclass
class Pet:
    name: str
    animal: str  # e.g. "dog", "cat", "other"
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task"):
        """Add a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Task:
    title: str
    time_to_complete: int                        # minutes
    priority: Literal["low", "medium", "high"]
    pet_name: str = ""                           # which pet this task belongs to
    completed: bool = False
    time: str = "08:00"                          # scheduled start time in "HH:MM" format

    def set_time(self, minutes: int):
        """Update the estimated time to complete this task in minutes."""
        self.time_to_complete = minutes

    def set_priority(self, priority: Literal["low", "medium", "high"]):
        """Set the priority level for this task."""
        self.priority = priority

    def mark_complete(self) -> bool:
        """Mark this task as completed and return True."""
        self.completed = True
        return True


@dataclass
class Owner:
    name: str
    preferences: str = ""
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Build name-keyed dicts for O(1) pet and task lookups.

        Called automatically after __init__. Mirrors the pets and tasks
        lists into dicts so that delete operations skip linear scans.
        """
        self._pets_dict: dict = {p.name: p for p in self.pets}
        self._tasks_dict: dict = {t.title: t for t in self.tasks}

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)
        self._pets_dict[pet.name] = pet

    def delete_pet(self, pet_name: str):
        """Remove a pet by name, raising ValueError if not found."""
        if pet_name not in self._pets_dict:
            raise ValueError(f"Pet '{pet_name}' not found.")
        self._pets_dict.pop(pet_name)
        self.pets = list(self._pets_dict.values())

    def add_task(self, task: Task):
        """Add a task to this owner's task list."""
        self.tasks.append(task)
        self._tasks_dict[task.title] = task

    def delete_task(self, title: str):
        """Remove a task by title, raising ValueError if not found."""
        if title not in self._tasks_dict:
            raise ValueError(f"Task '{title}' not found.")
        self._tasks_dict.pop(title)
        self.tasks = list(self._tasks_dict.values())

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status.

        Pass pet_name to get only that pet's tasks.
        Pass completed=True/False to filter by completion status.
        Both filters can be combined.
        """
        result = self.tasks
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Schedule:
    owner: Owner
    available_minutes: int = 480  # default: 8-hour day
    _sorted_cache: List[Task] = field(default_factory=list, init=False, repr=False)
    _tasks_snapshot: int = field(default=0, init=False, repr=False)

    def _invalidate_cache(self):
        self._tasks_snapshot = -1

    def generate_schedule(self) -> List[Task]:
        """Return a prioritized list of tasks that fit within the available time.

        Sorts tasks by priority (high → low) then by duration (shortest first)
        as a tiebreaker. Uses a snapshot-based cache so the sort only reruns
        when the task list changes. Greedily packs tasks until available_minutes
        is exhausted; tasks that don't fit are skipped.
        """
        current_snapshot = id(self.owner.tasks) + len(self.owner.tasks)
        if not self._sorted_cache or current_snapshot != self._tasks_snapshot:
            self._sorted_cache = sorted(
                self.owner.tasks,
                key=lambda t: (PRIORITY_ORDER[t.priority], t.time_to_complete),
            )
            self._tasks_snapshot = current_snapshot

        scheduled = []
        time_remaining = self.available_minutes
        for task in self._sorted_cache:
            if task.time_to_complete <= time_remaining:
                scheduled.append(task)
                time_remaining -= task.time_to_complete

        return scheduled

    def sort_by_time(self) -> List[Task]:
        """Return owner tasks sorted by scheduled start time (HH:MM) ascending.

        Converts each task's time string to an (hour, minute) integer tuple
        before comparing, so the sort is numerically correct regardless of
        zero-padding. Does not mutate the original task list.
        """
        return sorted(
            self.owner.tasks,
            key=lambda t: tuple(int(x) for x in t.time.split(":")),
        )

    def detect_conflicts(self) -> List[str]:
        """Check all tasks for overlapping time windows and return warnings.

        Compares every unique pair of tasks using the interval overlap formula:
            A overlaps B  if  A.start < B.end  AND  B.start < A.end
        Start and end times are converted from "HH:MM" strings to
        minutes-since-midnight for integer arithmetic. Applies to tasks
        across all pets — same-pet and cross-pet overlaps are both reported.
        Returns a list of human-readable warning strings; never raises.
        """
        to_min = lambda s: int(s.split(":")[0]) * 60 + int(s.split(":")[1])

        warnings = []
        tasks = self.owner.tasks

        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                a, b = tasks[i], tasks[j]
                a_start, a_end = to_min(a.time), to_min(a.time) + a.time_to_complete
                b_start, b_end = to_min(b.time), to_min(b.time) + b.time_to_complete

                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"WARNING: '{a.title}' ({a.pet_name}, {a.time}–{a_end // 60:02d}:{a_end % 60:02d}) "
                        f"overlaps with '{b.title}' ({b.pet_name}, {b.time}–{b_end // 60:02d}:{b_end % 60:02d})"
                    )

        return warnings

    def delete_schedule(self):
        """Clear all tasks from the owner's task list."""
        self.owner.tasks = []
