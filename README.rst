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
        sleep(1)
        print(
            "Proceess #{id} nas PID: {pid}".format(
                id=forkme.get_id(),
                pid=os.getpid()
            )
        )


    if __name__ == '__main__':
        main()


This code makes 4 forks. When you try to run it you will see something like this ::

    Master proccess has PID: 7437
    INFO:forkme:Starting 4 processes
    Proceess #2 nas PID: 7440
    Proceess #1 nas PID: 7439
    Proceess #3 nas PID: 7441
    Proceess #0 nas PID: 7438
    INFO:forkme:Child with PID: 7439 Number: 1 exited normally
    INFO:forkme:Child with PID: 7441 Number: 3 exited normally
    INFO:forkme:Child with PID: 7440 Number: 2 exited normally
    INFO:forkme:Child with PID: 7438 Number: 0 exited normally


Forkme will be control forks. When subprocess will be killed or will exit with 
non-zero code it will be restarted immediately.
