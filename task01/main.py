from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = [PrintJob(**job) for job in print_jobs]
    constraints = PrinterConstraints(**constraints)

    jobs.sort(key=lambda job: (job.priority, job.print_time))

    print_order = []
    total_time = 0

    i = 0
    n = len(jobs)

    while i < n:
        group = []
        total_volume = 0

        while i < n and len(group) < constraints.max_items and total_volume + jobs[i].volume <= constraints.max_volume:
            group.append(jobs[i])
            total_volume += jobs[i].volume
            i += 1

        if not group:
            group.append(jobs[i])
            i += 1

        print_order.extend([job.id for job in group])
        max_time = max(job.print_time for job in group)
        total_time += max_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }

def test_printing_optimization():

    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    result1 = optimize_printing(test1_jobs, constraints)
    result2 = optimize_printing(test2_jobs, constraints)
    result3 = optimize_printing(test3_jobs, constraints)

    return result1, result2, result3

test_printing_optimization()
