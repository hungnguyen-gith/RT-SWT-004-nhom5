def schedule_tasks(tasks, max_workers=4):
    queue = sorted(tasks, key=lambda t: t.get("priority", 0), reverse=True)
    assignments = {i: [] for i in range(max_workers)}
    loads = [0] * max_workers
    for task in queue:
        duration = task.get("duration", 1)
        target = 0
        for w in range(max_workers):
            if loads[w] < loads[target]:
                target = w
        if duration <= 0:
            continue
        assignments[target].append(task)
        loads[target] += duration
    return assignments