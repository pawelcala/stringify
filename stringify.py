#!/usr/bin/env python3
from executable.android2docs import AndroidToDocs
from executable.docs2android import DocsToAndroid
from executable.docs2swift import DocsToSwift
from executable.swift2docs import SwiftToDocs
from utils.args_utils import Settings, Mode
from utils.executiontimer import ExecutionTimer
from utils.log_utils import log_step

MODE_EXECS = {
    Mode.EXPORT_ANDROID: AndroidToDocs,
    Mode.IMPORT_ANDROID: DocsToAndroid,
    Mode.EXPORT_IOS: SwiftToDocs,
    Mode.IMPORT_IOS: DocsToSwift,
}


def main():
    execution_timer = ExecutionTimer(log_tag="stringify", logger=log_step)
    execution_timer.start()

    settings = Settings()
    settings.parse()
    settings.debug()

    mode = settings.app_mode()
    executable = MODE_EXECS[mode](settings)
    executable.execute()
    execution_timer.stop()


if __name__ == '__main__':
    main()
