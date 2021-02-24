def debug_init():
    global DEBUG
    DEBUG = False


def log(*args):
    if DEBUG:
        print(*args)