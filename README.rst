ForkMe
======

Fork your proccess like a boss

.. code-block:: python

    import forkme
    import logging
    import os
    from time import sleep


    logging.basicConfig(level=logging.DEBUG)


    def main():
        print("Master proccess has PID: {0}".format(os.getpid()))
        forkme.fork(4)
        print(
            "Proceess #{id} has PID: {pid}".format(
                id=forkme.get_id(),
                pid=os.getpid()
            )
        )
        sleep(1)


    if __name__ == '__main__':
        main()


This code makes 4 forks. When you try to run it you will see something like this ::

    Master proccess has PID: 7437
    INFO:forkme:Starting 4 processes
    Proceess #2 has PID: 7440
    Proceess #1 has PID: 7439
    Proceess #3 has PID: 7441
    Proceess #0 has PID: 7438
    INFO:forkme:Child with PID: 7439 Number: 1 exited normally
    INFO:forkme:Child with PID: 7441 Number: 3 exited normally
    INFO:forkme:Child with PID: 7440 Number: 2 exited normally
    INFO:forkme:Child with PID: 7438 Number: 0 exited normally


Forkme will be control forks. When subprocess will be killed or will exit with 
non-zero code it will be restarted immediately. e.g.::

    Master proccess has PID: 7579
    INFO:forkme:Starting 4 processes
    Proceess #0 has PID: 7580
    Proceess #1 has PID: 7581
    Proceess #2 has PID: 7582
    Proceess #3 has PID: 7583
    WARNING:forkme:Child with PID: 7580 Number: 0 killed by signal 9, restarting
    Proceess #0 has PID: 7584
    INFO:forkme:Child with PID: 7581 Number: 1 exited normally
    INFO:forkme:Child with PID: 7582 Number: 2 exited normally
    INFO:forkme:Child with PID: 7583 Number: 3 exited normally
    INFO:forkme:Child with PID: 7584 Number: 0 exited normally

