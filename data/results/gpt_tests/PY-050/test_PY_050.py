import pytest

def test_schedule_tasks_normal_cases():
    tasks = [
        {"name": "task1", "duration": 2, "priority": 1},
        {"name": "task2", "duration": 1, "priority": 2},
        {"name": "task3", "duration": 3, "priority": 3},
        {"name": "task4", "duration": 2, "priority": 1},
    ]
    expected = {
        0: [{"name": "task3", "duration": 3, "priority": 3}],
        1: [{"name": "task1", "duration": 2, "priority": 1}],
        2: [{"name": "task2", "duration": 1, "priority": 2}],
        3: [{"name": "task4", "duration": 2, "priority": 1}],
    }
    assert schedule_tasks(tasks) == expected

def test_schedule_tasks_boundary_cases():
    tasks = [
        {"name": "task1", "duration": 0, "priority": 1},
        {"name": "task2", "duration": 1, "priority": 2},
        {"name": "task3", "duration": 1, "priority": 3},
    ]
    expected = {
        0: [{"name": "task3", "duration": 1, "priority": 3}],
        1: [{"name": "task2", "duration": 1, "priority": 2}],
        2: [],
        3: [],
    }
    assert schedule_tasks(tasks) == expected

def test_schedule_tasks_edge_cases():
    tasks = []
    expected = {0: [], 1: [], 2: [], 3: []}
    assert schedule_tasks(tasks) == expected

    tasks = [{"name": "task1", "duration": -1, "priority": 1}]
    expected = {0: [], 1: [], 2: [], 3: []}
    assert schedule_tasks(tasks) == expected

    tasks = [{"name": "task1", "duration": 1, "priority": 1}]
    expected = {0: [{"name": "task1", "duration": 1, "priority": 1}], 1: [], 2: [], 3: []}
    assert schedule_tasks(tasks) == expected

def test_schedule_tasks_with_max_workers():
    tasks = [
        {"name": "task1", "duration": 2, "priority": 1},
        {"name": "task2", "duration": 2, "priority": 2},
        {"name": "task3", "duration": 2, "priority": 3},
        {"name": "task4", "duration": 2, "priority": 4},
        {"name": "task5", "duration": 2, "priority": 5},
    ]
    expected = {
        0: [{"name": "task5", "duration": 2, "priority": 5}],
        1: [{"name": "task4", "duration": 2, "priority": 4}],
        2: [{"name": "task3", "duration": 2, "priority": 3}],
        3: [{"name": "task2", "duration": 2, "priority": 2}],
    }
    assert schedule_tasks(tasks, max_workers=4) == expected