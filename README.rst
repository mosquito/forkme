ForkMe
======

Fork your proccess like a boss::

    import forkme
    import logging
    from time import sleep


    logging.basicConfig(level=logging.DEBUG)


    def main():
        forkme.fork(4)
        sleep(1)
        print(forkme.get_id())


    if __name__ == '__main__':
        main()


Forkme will control forks. When subprocess will be killed or will exit with non-zero code it
will be restarted immediately.