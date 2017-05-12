import time


class ExecutionTimer:
    def __init__(self, log_tag="ExecutionTimer", print_log=True):
        self.print_log = print_log
        self.log_tag = log_tag
        self.starttime = -1
        self.endtime = -1
        self.running = True

    def start(self):
        self.running = True
        self.starttime = time.time()
        self.log("start timer")

    def split(self, message="split"):
        if not self.running:
            self.log("stopwatch not started!")
            return
        splittime = time.time() - self.starttime
        self.log("%d (%s)" % (splittime, message))

    def stop(self):
        self.running = False
        self.endtime = time.time()
        self.log("stop timer")
        self.log("----------")
        self.log(self.endtime - self.starttime)

    def log(self, message):
        print("[%s] %s" % (self.log_tag, message))
