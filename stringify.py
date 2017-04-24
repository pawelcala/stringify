#!/usr/bin/env python3

import time

from googledocs.GoogleDocsHandler import GoogleDocsHandler
from loaders.AndroidStringsLoader import AndroidStringsLoader
from loaders.IosStringsLoader import IOSStringsLoader
from producers.AndroidProducer import AndroidProducer
from utils.ArgsUtils import Settings, Mode
from utils.LogUtils import log_step


def main():
    start_seconds = time.time()

    settings = Settings()
    settings.parse()

    google_doc_name = settings.google_doc_name()
    google_docs_handler = GoogleDocsHandler(settings.credentials_location())
    mode = settings.app_mode()

    if mode == Mode.IMPORT_ANDROID:
        export_path = settings.export_path()
        default_language = settings.default_language()

        filename = settings.android_destination_filename()

        AndroidProducer(google_docs_handler, google_doc_name,
                        export_path=export_path,
                        xml_name=filename,
                        default_language=default_language).execute()

    # if mode == Mode.IMPORT_IOS:
    #     export_path = settings[SETTINGS_KEY_EXPORT_PATH]
    #     filename = settings[
    #         SETTINGS_KEY_XML_NAME] if SETTINGS_DEFAULT_XML_NAME in settings.keys() else SETTINGS_DEFAULT_LOCALIZABLE_NAME
    #
    #     SwiftProducer(google_docs_handler, google_doc_name,
    #                   export_path=export_path,
    #                   filename=filename).execute()
    #
    if mode in (Mode.EXPORT_IOS, Mode.EXPORT_ANDROID):
        path = settings.export_path()
        default_language = settings.default_language()

        if mode == Mode.EXPORT_ANDROID:
            xml_name = settings.export_filename()
            loader = AndroidStringsLoader(path=path, xml_name=xml_name, default_language=default_language)

        if mode == Mode.EXPORT_IOS:
            filename = settings.export_ios_filename()
            loader = IOSStringsLoader(path=path, filename=filename)

        dictionary = loader.load()
        google_docs_handler.write(google_doc_name, dictionary)

    log_step("Done (took: {} seconds)".format(int(time.time() - start_seconds)))


if __name__ == '__main__':
    main()
