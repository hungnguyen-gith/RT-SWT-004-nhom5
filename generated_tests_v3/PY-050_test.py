from functions.PY_050 import schedule_tasks

def test_schedule_tasks_normal_case():
    tasks = [
        {"id": 1, "duration": 2, "priority": 1},
        {"id": 2, "duration": 1, "priority": 2},
        {"id": 3, "duration": 3, "priority": 3},
        {"id": 4, "duration": 2, "priority": 1}
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result) == 2
    assert len(result[0]) + len(result[1]) == len(tasks)

def test_schedule_tasks_edge_case_empty():
    tasks = []
    result = schedule_tasks(tasks, max_workers=4)
    assert result == {0: [], 1: [], 2: [], 3: []}

def test_schedule_tasks_edge_case_single_task():
    tasks = [{"id": 1, "duration": 5, "priority": 1}]
    result = schedule_tasks(tasks, max_workers=4)
    assert len(result[0]) == 1
    assert result[0][0]["id"] == 1
    assert all(len(result[i]) == 0 for i in range(1, 4))

def test_schedule_tasks_edge_case_zero_duration():
    tasks = [{"id": 1, "duration": 0, "priority": 1}]
    result = schedule_tasks(tasks, max_workers=4)
    assert all(len(result[i]) == 0 for i in range(4))

def test_schedule_tasks_invalid_duration():
    tasks = [
        {"id": 1, "duration": -1, "priority": 1},
        {"id": 2, "duration": 2, "priority": 2}
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result[0]) == 0
    assert len(result[1]) == 1
    assert result[1][0]["id"] == 2

def test_schedule_tasks_max_workers():
    tasks = [
        {"id": 1, "duration": 1, "priority": 1},
        {"id": 2, "duration": 1, "priority": 2},
        {"id": 3, "duration": 1, "priority": 3},
        {"id": 4, "duration": 1, "priority": 4},
        {"id": 5, "duration": 1, "priority": 5}
    ]
    result = schedule_tasks(tasks, max_workers=3)
    assert len(result[0]) + len(result[1]) + len(result[2]) == len(tasks)

def test_schedule_tasks_high_priority():
    tasks = [
        {"id": 1, "duration": 2, "priority": 1},
        {"id": 2, "duration": 1, "priority": 3},
        {"id": 3, "duration": 3, "priority": 2}
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert result[0][0]["id"] == 2  # Highest priority task
    assert result[1][0]["id"] == 3  # Second highest priority task
    assert len(result[1]) == 1 and result[1][0]["id"] == 1  # Remaining task

def test_schedule_tasks_large_number_of_tasks():
    tasks = [{"id": i, "duration": 1, "priority": i} for i in range(1, 101)]
    result = schedule_tasks(tasks, max_workers=10)
    assert len(result) == 10
    assert sum(len(v) for v in result.values()) == len(tasks)