import sys

from constants import APP_VERSION


def log_exception(message, force_quit=False):
    print("EXCEPTION: {}".format(message))
    if force_quit:
        sys.exit()


def log_step(message):
    print("[stringify]:\t{}".format(message.encode('utf-8')))


def log_version():
    log_step("version: " + APP_VERSION)
    log_step("-----------------")
    log_step("")
