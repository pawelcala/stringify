#!/usr/bin/env python3
from executable.AndroidToDocs import AndroidToDocs
from executable.DocsToAndroid import DocsToAndroid
from executable.DocsToSwift import DocsToSwift
from executable.SwiftToDocs import SwiftToDocs
from utils.ArgsUtils import Settings, Mode
from utils.executiontimer import ExecutionTimer

MODE_EXECS = {
    Mode.EXPORT_ANDROID: AndroidToDocs,
    Mode.IMPORT_ANDROID: DocsToAndroid,
    Mode.EXPORT_IOS: SwiftToDocs,
    Mode.IMPORT_IOS: DocsToSwift,
}


def main():
    execution_timer = ExecutionTimer(log_tag="ScriptTimer")
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
