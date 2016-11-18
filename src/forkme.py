import errno
import os
import signal
import sys
import fcntl
import logging
import multiprocessing
import random

from binascii import hexlify


log = logging.getLogger(__name__)


def _cloexec(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)


def _pipe_cloexec():
    r, w = os.pipe()
    _cloexec(r)
    _cloexec(w)
    return r, w


_TASK_ID = None


default_signals = frozenset({
    signal.SIGTERM,
    signal.SIGINT,
    signal.SIGQUIT,
    signal.SIGALRM,
    signal.SIGUSR1,
    signal.SIGUSR2,
})


def fork(num_processes, max_restarts=100, pass_signals=default_signals):
    global _TASK_ID
    assert _TASK_ID is None, "Process already forked"

    if num_processes is None or num_processes <= 0:
        num_processes = multiprocessing.cpu_count()

    log.info("Starting %d processes", num_processes)

    interrupt = False
    children = {}

    def signal_to_children(sig, frame):
        nonlocal children, interrupt

        if sig in {signal.SIGTERM, signal.SIGINT, signal.SIGQUIT}:
            interrupt = True

        for pid in children:
            os.kill(pid, sig)

    for sig in pass_signals:
        signal.signal(sig, signal_to_children)

    def start(number):
        pid = os.fork()

        if pid:
            children[pid] = number
            return None

        else:
            # child process
            seed = int(hexlify(os.urandom(16)), 16)
            random.seed(seed)

            global _TASK_ID
            _TASK_ID = number

            return number

    for i in range(num_processes):
        process_id = start(i)

        if process_id is not None:
            return process_id

    num_restarts = 0

    while children:
        try:
            pid, status = os.wait()
        except OSError as e:
            err_no = None

            if hasattr(e, 'errno'):
                err_no = e.errno
            elif e.args:
                err_no = e.args[0]

            if err_no == errno.EINTR:
                continue

            raise

        if pid not in children:
            continue

        process_id = children.pop(pid)

        if interrupt:
            continue

        if os.WIFSIGNALED(status):
            log.warning(
                "Child with PID: %d Number: %d killed by signal %d, restarting",
                pid,
                process_id,
                os.WTERMSIG(status)
            )

        elif os.WEXITSTATUS(status) != 0:
            log.warning(
                "Child with PID: %d Number: %d exited with status %d, restarting",
                pid,
                process_id,
                os.WEXITSTATUS(status)
            )
        else:
            log.info("Child with PID: %d Number: %d exited normally", pid, process_id)
            continue

        num_restarts += 1

        if num_restarts > max_restarts:
            raise RuntimeError("Too many child restarts, giving up")

        new_id = start(process_id)

        if new_id is not None:
            return new_id

    sys.exit(0)


def get_id():
    """Returns the current task id"""
    global _TASK_ID
    return _TASK_ID
