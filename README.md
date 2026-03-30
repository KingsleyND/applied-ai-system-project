# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

The scheduling engine in `pawpal_system.py` goes beyond a basic priority sort. Here is what was added:

**Sort by time** — `Schedule.sort_by_time()` orders tasks chronologically by their `"HH:MM"` start time using a lambda that converts to `(hour, minute)` integer tuples, so the sort is numerically correct regardless of zero-padding.

**Filter tasks** — `Owner.filter_tasks(pet_name, completed)` returns a subset of tasks matching an optional pet name, completion status, or both combined. Useful for displaying only a single pet's pending tasks.

**Conflict detection** — `Schedule.detect_conflicts()` compares every pair of tasks using the interval overlap formula (`A.start < B.end and B.start < A.end`). Conflicts across any pets are caught. Returns a list of plain-English warning strings and never raises an exception, so the app keeps running even when overlaps exist.

**O(1) lookups** — `Owner` maintains internal dicts keyed by pet name and task title so that `delete_pet()` and `delete_task()` skip linear scans entirely.

**Sort cache** — `generate_schedule()` caches the sorted task order and only re-sorts when the task list actually changes, avoiding redundant work on repeated calls.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
