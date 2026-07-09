import pytest

def test_schedule_tasks():
    # Test with normal tasks
    tasks = [
        {"name": "task1", "duration": 2, "priority": 1},
        {"name": "task2", "duration": 1, "priority": 2},
        {"name": "task3", "duration": 3, "priority": 3},
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result[0]) + len(result[1]) == len(tasks)
    
    # Test with varying durations and priorities
    tasks = [
        {"name": "task1", "duration": 5, "priority": 1},
        {"name": "task2", "duration": 3, "priority": 2},
        {"name": "task3", "duration": 2, "priority": 3},
        {"name": "task4", "duration": 1, "priority": 4},
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result[0]) + len(result[1]) == len(tasks)
    
    # Test with zero duration tasks
    tasks = [
        {"name": "task1", "duration": 0, "priority": 1},
        {"name": "task2", "duration": 2, "priority": 2},
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result[0]) == 0
    assert len(result[1]) == 1
    
    # Test with negative duration tasks
    tasks = [
        {"name": "task1", "duration": -1, "priority": 1},
        {"name": "task2", "duration": 2, "priority": 2},
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result[0]) == 0
    assert len(result[1]) == 1
    
    # Test with no tasks
    tasks = []
    result = schedule_tasks(tasks, max_workers=2)
    assert result == {0: [], 1: []}
    
    # Test with more workers than tasks
    tasks = [
        {"name": "task1", "duration": 1, "priority": 1},
        {"name": "task2", "duration": 2, "priority": 2},
    ]
    result = schedule_tasks(tasks, max_workers=5)
    assert len(result) == 5
    assert len(result[0]) + len(result[1]) == len(tasks)
    
    # Test with all tasks having the same priority
    tasks = [
        {"name": "task1", "duration": 1, "priority": 1},
        {"name": "task2", "duration": 1, "priority": 1},
        {"name": "task3", "duration": 1, "priority": 1},
    ]
    result = schedule_tasks(tasks, max_workers=2)
    assert len(result[0]) + len(result[1]) == len(tasks)