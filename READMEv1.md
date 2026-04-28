# PawPal+ — Pet Care Planning Assistant

PawPal+ is a Streamlit app that helps a pet owner plan daily care tasks across one or more pets. It builds a smart schedule based on priority and available time, detects conflicts, and supports recurring tasks so nothing gets forgotten.

## Demo

<a href="/course_images/ai110/pawpal_ss.png" target="_blank"><img src='/course_images/ai110/pawpal_ss.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Features

### Priority-Based Scheduling
The scheduler sorts all tasks by priority (high before medium before low) and uses duration as a tiebreaker when priorities are equal. It then greedily fits tasks into the owner's available time budget for the day, skipping any that would exceed the remaining minutes. Tasks that do not fit are surfaced in the UI as skipped rather than silently dropped.

### Sorting by Time
`Schedule.sort_by_time()` returns tasks ordered chronologically by their `HH:MM` start time. Start times are converted to integer `(hour, minute)` tuples before comparison so the sort is numerically correct regardless of zero-padding.

### Conflict Warnings
`Schedule.detect_conflicts()` scans every pair of tasks using the standard interval overlap formula — task A conflicts with task B if A starts before B ends and B starts before A ends. Conflicts between tasks for the same pet and across different pets are both detected. The method always returns a list of plain-English warning strings and never raises an exception, so the app stays running even when overlaps exist.

### Daily Recurrence
Tasks can be marked as recurring by setting a `recur_days` interval (e.g. `1` for daily, `7` for weekly). Calling `task.complete_and_recur(owner)` marks the original task complete and automatically adds a fresh, identical copy back to the owner's task list so the task reappears the next time a schedule is generated.

### Filter by Pet or Status
`Owner.filter_tasks(pet_name, completed)` returns a filtered subset of tasks. Filters can be applied individually or combined — for example, "show only Max's pending tasks." The original task list is never modified.

### Fast Lookups
`Owner` maintains internal dictionaries keyed by pet name and task title. Delete operations (`delete_pet`, `delete_task`) use a single dictionary lookup instead of scanning the full list, keeping performance consistent as the task list grows.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

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

## Testing PawPal+

### Run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

The suite contains 27 tests across four areas:

**Sorting correctness** — verifies that `sort_by_time()` returns tasks in chronological order, handles a single task, an empty list, an already-sorted list, and tasks that share the same hour but differ by minutes. Also confirms the original task list is never mutated.

**Recurrence logic** — verifies that calling `complete_and_recur()` on a recurring task marks the original complete, adds a fresh copy to the owner with `completed=False`, and preserves all original properties (title, duration, priority, time, recur interval). Also confirms that non-recurring tasks return `None` and no extra task is added.

**Conflict detection** — verifies that overlapping tasks are flagged with a `WARNING` string, that exact same start times are caught, that cross-pet overlaps are detected, and that the method never raises an exception. Edge cases include back-to-back tasks (touching but not overlapping), a single task, and an empty task list — all of which should return no warnings.

**Filter tasks** — verifies filtering by pet name, by completion status, and by both combined. Confirms that filtering for a pet with no tasks returns an empty list rather than an error.

### Confidence Level

*****/5

All 27 tests pass in 0.09 seconds. Core behaviors — sorting, recurrence, conflict detection, and filtering — are covered for both happy paths and edge cases. The rating is held back from a perfect score because the scheduler has no tests for the greedy packing algorithm itself, the Streamlit UI layer is untested, and task deduplication (two tasks with the same title) has no guard or test.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
