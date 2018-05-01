import signal
from subprocess import call
from typing import List
from psutil import Process, wait_procs, NoSuchProcess
from server.database.models.execution_process import ExecutionProcess


def kill_all_execution_processes(execution_processes: List[ExecutionProcess]):
    actual_execution_processes = [
        e for e in execution_processes if e.is_execution
    ]
    execution_parent_processes = [
        e for e in execution_processes if not e.is_execution
    ]

    kill_execution_processes(execution_parent_processes)
    kill_execution_processes(actual_execution_processes)


def kill_execution_processes(processes: List[ExecutionProcess]):
    for process_entry in processes:
        try:
            process = Process(process_entry.pid)
            children = process.children(recursive=True)
            children.append(process)
            for p in children:
                call(['kill', '-s', 'TERM', str(p.pid)])
            _, alive = wait_procs(children, timeout=2)
            for p in alive:
                call(['kill', '-s', 'QUIT', str(p.pid)])
        except NoSuchProcess:
            # The process was already killed. Let's continue
            pass


def get_process_alive_count(processes: List[ExecutionProcess],
                            count_children: bool = False):
    count = 0
    for process_entry in processes:
        try:
            process = Process(process_entry.pid)
            count += 1
            if count_children:
                children = process.children(recursive=True)
                count += len(children)
        except NoSuchProcess:
            # The process was already killed. Let's continue
            pass

    return count
