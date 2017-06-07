import argparse

from utils.log_utils import log_exception


class Mode:
    EXPORT_ALL = "export_all"
    EXPORT_ANDROID = "export_android"
    EXPORT_IOS = "export_ios"
    IMPORT_ANDROID = "import_android"
    IMPORT_IOS = "import_ios"


SETTINGS_KEY_GDOC_NAME = "spreadsheet_name"
SETTINGS_KEY_DEFAULT_LANG = "default_language"
SETTINGS_KEY_EXPORT_PATH = "locale"
SETTINGS_KEY_XML_NAME = "xml_name"
SETTINGS_KEY_MODE = "mode"
SETTINGS_KEY_LOGS_ON = "logs_on"
SETTINGS_KEY_CREDENTIALS_LOCATION = "credentials_location"

SETTINGS_DEFAULT_LANG = "en"
SETTINGS_DEFAULT_MODE = Mode.EXPORT_ALL
SETTINGS_DEFAULT_XML_NAME = "strings.xml"
SETTINGS_DEFAULT_LOCALIZABLE_NAME = "Localizable.strings"
SETTINGS_DEFAULT_LOGS_ON = True

G_FILE = "stringify_1.json"


class Settings:
    def __init__(self):
        self.settings = dict()

    def debug(self):
        print(self.settings)

    def parse(self):
        self.settings.update({SETTINGS_KEY_DEFAULT_LANG: SETTINGS_DEFAULT_LANG})
        self.settings.update({SETTINGS_KEY_MODE: SETTINGS_DEFAULT_MODE})
        self.settings.update({SETTINGS_KEY_LOGS_ON: SETTINGS_DEFAULT_LOGS_ON})
        self.settings.update({SETTINGS_KEY_EXPORT_PATH: '.'})
        self.settings.update({SETTINGS_KEY_CREDENTIALS_LOCATION: G_FILE})

        parser = argparse.ArgumentParser(description='Stringify parser')
        parser.add_argument("-d", "--default-lang",
                            help="Android default language. Default language sets values folder "
                                 "without language postfix. If left 'en' is set.")

        parser.add_argument("-n", "--spreadsheet-name", help="Google Spreadsheet name.")

        parser.add_argument("-p", "--dest-path",
                            help="Localized strings destination path. Should point on project/module directory "
                                 "(Used in both modes - IMPORT and EXPORT).")

        parser.add_argument("-x", "--xml-filename", help="Android xml or swift strings filename. "
                                                         "Default: strings.xml (Android), Localizable.strings (iOS)")

        parser.add_argument("-m", "--mode",
                            help="Available modes: "
                                 "export_ios - exports/uploads ios strings,\n"
                                 "export_android - exports/uploads android strings,\n"
                                 "import_android - import/download Android strings and create Google Spreadsheet,\n"
                                 "import_ios - import/download iOS strings and create Google Spreadsheet\n")

        parser.add_argument("-o", "--logs-off", help="Turns progress debug logs off")

        parser.add_argument("-u", "--oauth-credentials-location",
                            help="oauth credentials location. Default: .credentials")

        args = parser.parse_args()

        if args.mode:
            self.settings.update({SETTINGS_KEY_MODE: args.mode.lower()})

        if args.spreadsheet_name:
            self.settings.update({SETTINGS_KEY_GDOC_NAME: args.spreadsheet_name})
        else:
            log_exception("'Spreadsheet name' shouldn't be empty", force_quit=True)

        if args.default_lang:
            self.settings.update({SETTINGS_KEY_DEFAULT_LANG: args.default_lang})

        if args.dest_path:
            self.settings.update({SETTINGS_KEY_EXPORT_PATH: args.dest_path})

        if args.xml_filename:
            self.settings.update({SETTINGS_KEY_XML_NAME: args.xml_filename})

        if args.logs_off:
            self.settings.update({SETTINGS_KEY_LOGS_ON: False})

        if args.oauth_credentials_location:
            self.settings.update({SETTINGS_KEY_CREDENTIALS_LOCATION: args.oauth_credentials_location})

    def credentials_location(self):
        return self.settings.get(SETTINGS_KEY_CREDENTIALS_LOCATION)

    def app_mode(self):
        return self.settings.get(SETTINGS_KEY_MODE)

    def google_doc_name(self):
        return self.settings.get(SETTINGS_KEY_GDOC_NAME)

    def export_path(self):
        return self.settings.get(SETTINGS_KEY_EXPORT_PATH)

    def default_language(self):
        return self.settings.get(SETTINGS_KEY_DEFAULT_LANG)

    def android_destination_filename(self):
        return self.settings[
            SETTINGS_KEY_XML_NAME] if SETTINGS_KEY_XML_NAME in self.settings.keys() else SETTINGS_DEFAULT_XML_NAME

    def export_filename(self):
        return self.settings[SETTINGS_KEY_XML_NAME] if SETTINGS_KEY_XML_NAME in self.settings.keys() \
            else SETTINGS_DEFAULT_XML_NAME

    def export_ios_filename(self):
        return self.settings[SETTINGS_KEY_XML_NAME] if SETTINGS_KEY_XML_NAME in self.settings.keys() \
            else SETTINGS_DEFAULT_LOCALIZABLE_NAME
