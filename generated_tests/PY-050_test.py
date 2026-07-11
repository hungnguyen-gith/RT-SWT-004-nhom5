import pytest

def test_schedule_tasks_normal_cases():
    tasks = [
        {"name": "task1", "duration": 2, "priority": 1},
        {"name": "task2", "duration": 3, "priority": 2},
        {"name": "task3", "duration": 1, "priority": 3},
    ]
    expected = {
        0: [{"name": "task2", "duration": 3, "priority": 2}],
        1: [{"name": "task1", "duration": 2, "priority": 1}],
        2: [{"name": "task3", "duration": 1, "priority": 3}],
        3: [],
    }
    assert schedule_tasks(tasks) == expected

def test_schedule_tasks_boundary_cases():
    tasks = [
        {"name": "task1", "duration": 0, "priority": 1},
        {"name": "task2", "duration": 1, "priority": 2},
        {"name": "task3", "duration": 1, "priority": 3},
    ]
    expected = {
        0: [{"name": "task2", "duration": 1, "priority": 2}],
        1: [{"name": "task3", "duration": 1, "priority": 3}],
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

    tasks = [{"name": "task1", "duration": 1, "priority": 1}] * 5
    expected = {
        0: [{"name": "task1", "duration": 1, "priority": 1}],
        1: [{"name": "task1", "duration": 1, "priority": 1}],
        2: [{"name": "task1", "duration": 1, "priority": 1}],
        3: [{"name": "task1", "duration": 1, "priority": 1}],
    }
    assert schedule_tasks(tasks, max_workers=4) == expected

def test_schedule_tasks_with_max_workers():
    tasks = [
        {"name": "task1", "duration": 2, "priority": 1},
        {"name": "task2", "duration": 3, "priority": 2},
        {"name": "task3", "duration": 1, "priority": 3},
        {"name": "task4", "duration": 4, "priority": 4},
    ]
    expected = {
        0: [{"name": "task4", "duration": 4, "priority": 4}],
        1: [{"name": "task2", "duration": 3, "priority": 2}],
        2: [{"name": "task1", "duration": 2, "priority": 1}],
        3: [{"name": "task3", "duration": 1, "priority": 3}],
    }
    assert schedule_tasks(tasks, max_workers=4) == expected