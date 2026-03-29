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

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def delete_pet(self, pet_name: str):
        """Remove a pet by name, raising ValueError if not found."""
        match = [p for p in self.pets if p.name == pet_name]
        if not match:
            raise ValueError(f"Pet '{pet_name}' not found.")
        self.pets = [p for p in self.pets if p.name != pet_name]

    def add_task(self, task: Task):
        """Add a task to this owner's task list."""
        self.tasks.append(task)

    def delete_task(self, title: str):
        """Remove a task by title, raising ValueError if not found."""
        match = [t for t in self.tasks if t.title == title]
        if not match:
            raise ValueError(f"Task '{title}' not found.")
        self.tasks = [t for t in self.tasks if t.title != title]


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Schedule:
    owner: Owner
    available_minutes: int = 480  # default: 8-hour day

    def generate_schedule(self) -> List[Task]:
        """Return a prioritized list of tasks that fit within the available time."""
        sorted_tasks = sorted(
            self.owner.tasks,
            key=lambda t: (PRIORITY_ORDER[t.priority], t.time_to_complete),
        )

        scheduled = []
        time_remaining = self.available_minutes
        for task in sorted_tasks:
            if task.time_to_complete <= time_remaining:
                scheduled.append(task)
                time_remaining -= task.time_to_complete

        return scheduled

    def delete_schedule(self):
        """Clear all tasks from the owner's task list."""
        self.owner.tasks = []
