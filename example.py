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
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
