#!/usr/bin/env python3

# system imports
import time
import argparse
import os
import io
import re
import sys
import xml.etree.ElementTree as ET

# Dependency imports
from xml.dom import minidom

import gspread
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


class NotFoundException(Exception):
    pass


class Mode:
    EXPORT_ALL = "export_all"
    EXPORT_ANDROID = "export_android"
    EXPORT_IOS = "export_ios"
    IMPORT_ANDROID = "import_android"
    IMPORT_IOS = "import_ios"


class TranslationRow:
    def __init__(self, key):
        self.key = key
        self.translations = dict()

    def add_translation(self, lang, value):
        self.translations.update({lang: value})

    def get_translation(self, lang):
        return self.translations.get(lang)


class Dictionary:
    def __init__(self):
        self.dictionary = dict()
        self.languages = set()

    def add_translation(self, key, lang, word, comment=None):
        self.languages.add(lang)
        translation_row = self.dictionary.get(key)
        if translation_row is None:
            translation_row = TranslationRow(key)
            self.dictionary.update({translation_row.key: translation_row})

        translation_row.add_translation(lang, word)

    def get_translation(self, key, lang):
        return self.dictionary.get(key).get_translation(lang)

    def keys_iterator(self):
        return self.dictionary

    def keys(self):
        return self.dictionary.keys()


# CONTENT PARSERS

class Command:
    def execute(self):
        pass


class GoogleDocsHandler(Command):
    def __init__(self, credentials_path):
        self.client = None
        self.credentials_path = credentials_path

    def _oauth_load_credentials(self):
        log_step("Loading saved credentials")
        if os.path.isfile(settings[SETTINGS_KEY_CREDENTIALS_LOCATION]):
            try:
                storage = Storage(settings[SETTINGS_KEY_CREDENTIALS_LOCATION])
                return storage.locked_get()
            except:
                return None
        return None

    def _oauth_save_credentials(self, credentials):
        log_step("Saving credentials")
        storage = Storage(G_FILE)
        storage.locked_put(credentials)

    def _oauth(self):
        log_step("Authorizing user")
        credentials = self._oauth_load_credentials()
        if credentials:
            return credentials
        else:
            flow = OAuth2WebServerFlow(client_id=G_CLIENT_ID,
                                       client_secret=G_CLIENT_SECRET,
                                       scope=G_SCOPE,
                                       redirect_uri=G_REDIRECT)
            auth_uri = flow.step1_get_authorize_url()
            print(auth_uri)
            code = input("Enter code:")
            credentials = flow.step2_exchange(code)
            self._oauth_save_credentials(credentials)
            return credentials

    def authorize(self):
        if not self.client:
            credentials = self._oauth()
            self.client = gspread.authorize(credentials)
        return self.client

    def write(self, google_doc_name, dictionary):
        worksheet = self._get_worksheet(google_doc_name)

        log_step("Clear spreadsheet...")
        self._clear_worksheet(worksheet)
        log_step("Writing cells...")

        row = 1
        languages = dictionary.languages
        languages = sorted(languages)
        for index, lang in enumerate(languages):
            column = index + 2
            worksheet.update_cell(row, column, lang)

        row = 2
        for key in dictionary.keys():
            worksheet.update_cell(row, 1, key)
            cells = []
            for index, lang in enumerate(languages):
                column = index + 2
                translated_value = dictionary.get_translation(key, lang)
                cell = worksheet.cell(row, column)
                cell.value = translated_value
                cells.append(cell)
            row += 1

            worksheet.update_cells(cells)

    def _get_worksheet(self, google_doc_name):
        google_doc_client = self.authorize()
        try:
            spreadsheet = google_doc_client.open(google_doc_name).sheet1
        except gspread.SpreadsheetNotFound:
            spreadsheet = google_doc_client.create(google_doc_name).sheet1
        return spreadsheet

    def read(self, google_doc_name):
        worksheet = self._get_worksheet(google_doc_name)
        languages = self._load_languages(worksheet)
        entries = self._read_strings(worksheet, len(languages))
        dictionary = Dictionary()

        for i, lang in enumerate(languages):
            for row in entries:
                if len(row) == 0:
                    continue
                dictionary.add_translation(row[0], lang, row[i + 1])
        return dictionary

    def _clear_worksheet(self, spreadsheet):
        '''This is way more efficient than worksheet.clear() method'''
        cells = spreadsheet.findall(re.compile(".+"))
        for cell in cells:
            cell.value = ""
        spreadsheet.update_cells(cells)

    def _load_languages(self, sheet):
        log_step("Reading languages")
        column = 2
        languages = []
        while True:
            lang_code = sheet.cell(1, column).value
            if len(lang_code.strip()) > 0:
                languages.append(lang_code)
                column += 1
            else:
                return languages

    def _read_row(self, sheet, row, langs_count):
        row_data = list()
        for column in range(1, langs_count + 2):
            cell_value = sheet.cell(row, column).value
            if len(cell_value.strip()) == 0 and column == 1:
                return row_data
            else:
                row_data.append(cell_value)
        return row_data

    def _read_strings(self, sheet, langs_count):
        log_step("Reading spreadsheet cells")
        row = 2
        rows = []
        empty_row = False
        while True:
            row_data = self._read_row(sheet, row, langs_count)
            if len(row_data) == 0:
                if empty_row:
                    return rows
                else:
                    empty_row = True
            else:
                empty_row = False

            rows.append(row_data)
            row += 1


class DataLoader(Command):
    def execute(self):
        raise NotImplemented

    def load(self):
        return self.execute()


class AndroidStringsLoader(DataLoader):
    def __init__(self, path, **kwargs):
        self.path = path
        self.filename = kwargs['xml_name'] if 'xml_name' in kwargs.keys() else 'strings.xml'
        self.default_language = kwargs['default_language'] if 'default_language' in kwargs.keys() else 'en'

    def execute(self):
        file_paths = find_files(path=self.path, filename_regex=self.filename)
        dictionary = Dictionary()
        for filepath in file_paths:
            language = self._decode_filepath_language(filepath)
            entries = self._decode_file_entries(filepath)

            if len(language.strip()) == 0:
                language = self.default_language

            for entry in entries:
                dictionary.add_translation(entry[0], language, entry[1])
        return dictionary

    def _decode_filepath_language(self, filepath):
        match = re.match(r'.*values([-a-z]{0,3})', filepath)
        if match:
            postfix = match.group(1)
            if len(postfix) == 3:
                postfix = postfix[-2:]
            else:
                postfix = self.default_language
        return postfix

    def _decode_file_entries(self, filepath):
        entries = []
        xml = ET.parse(filepath)
        root = xml.getroot()
        for child in root:
            key = child.get('name')
            value = child.text
            entries.append((key, value))
        return entries


class IOSStringsLoader(DataLoader):
    def __init__(self, path, **kwargs):
        self.path = path
        self.filename = kwargs['filename'] if 'filename' in kwargs.keys() else 'Localizable.strings'

    def execute(self):
        filepaths = find_files(path=self.path, filename_regex=self.filename)
        dictionary = Dictionary()

        for filepath in filepaths:
            language = self._decode_filepath_language(filepath)
            entries = self._decode_file_entries(filepath)

            for key, word in entries:
                dictionary.add_translation(key, language, word)

        return dictionary

    def _decode_filepath_language(self, path):
        match = re.match(r"""(.*)\.lproj""", path)
        if match:
            prefix = match.group(1)
            if len(prefix) > 2:
                prefix = prefix[-2:]
            return prefix
        else:
            raise NotFoundException

    def _decode_file_entries(self, filepath):
        entries = []
        file = open(filepath)

        for line in file:
            match = re.match(r'"(.*)".*=.*"(.*)";', line)
            if match:
                entries.append((match.group(1), match.group(2)))
        return entries


# PRODUCERS
class Producer(Command):
    def execute(self):
        pass


class AndroidProducer(Producer):
    def __init__(self, google_doc_handler, google_doc_name, export_path=".", default_language="en",
                 xml_name="strings.xml"):

        self.xml_name = xml_name
        self.default_language = default_language
        self.export_path = export_path
        self.google_doc_name = google_doc_name
        self.google_doc_handler = google_doc_handler

    def execute(self):
        dictionary = self.google_doc_handler.read(self.google_doc_name)
        self._export(dictionary)

    def _export(self, dictionary):
        log_step("Exporting Android strings")
        cwd = os.getcwd()
        if self.export_path:
            try:
                os.makedirs(self.export_path, exist_ok=True)
            except Exception:
                pass
            os.chdir(self.export_path)

        for i, lang in enumerate(dictionary.languages):
            xml = ET.Element('resources')
            for key in dictionary.keys():
                value = dictionary.get_translation(key, lang)
                string_row = ET.SubElement(xml, 'string')
                string_row.set('name', key)
                string_row.text = value

            dom = minidom.parseString(ET.tostring(xml, 'utf-8'))
            pretty_dom = dom.toprettyxml()

            dir_name = "values".format(self.default_language) if self.default_language == lang else "values-{}".format(
                lang)
            save_file(pretty_dom, dir_name, self.xml_name)

        os.chdir(cwd)


class SwiftProducer(Producer):
    def __init__(self, google_doc_handler, google_doc_name, export_path=".", filename="Localizable.strings"):
        self.filename = filename
        self.export_path = export_path
        self.google_doc_name = google_doc_name
        self.google_doc_handler = google_doc_handler

    def execute(self):
        dictionary = self.google_doc_handler.read(self.google_doc_name)
        self._export(dictionary)

    def _export(self, dictionary):
        log_step("Exporting iOS strings")
        cwd = os.getcwd()
        if self.export_path:
            try:
                os.makedirs(self.export_path, exist_ok=True)
            except:
                pass

            os.chdir(self.export_path)

        for i, lang in enumerate(dictionary.languages):
            output = io.StringIO()
            for key in dictionary.keys():
                value = dictionary.get_translation(key, lang)
                output.write('"{}" = "{}";\n'.format(key, value))

            language_dir = "{}.lproj".format(lang)
            save_file(output.getvalue(), language_dir, self.filename)

        os.chdir(cwd)


APP_NAME = "stringify"
APP_VERSION = "0.0.3"

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

settings = dict()

G_CLIENT_ID = 'ENTER_CLIENT_ID'
G_CLIENT_SECRET = 'ENTER_CLIENT_SECRET'
G_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
G_REDIRECT = 'http://localhost/'
G_FILE = ".credentials"


def log_exception(message, force_quit=False):
    print("EXCEPTION: {}".format(message))
    if force_quit:
        sys.exit()


def log_step(message):
    if settings[SETTINGS_KEY_LOGS_ON]:
        pass
    print("[stringify]:\t{}".format(message))


def log_version():
    log_step("version: " + APP_VERSION)
    log_step("-----------------")
    log_step("")


def decode_sys_args():
    global settings

    settings.update({SETTINGS_KEY_DEFAULT_LANG: SETTINGS_DEFAULT_LANG})
    settings.update({SETTINGS_KEY_MODE: SETTINGS_DEFAULT_MODE})
    settings.update({SETTINGS_KEY_LOGS_ON: SETTINGS_DEFAULT_LOGS_ON})
    settings.update({SETTINGS_KEY_EXPORT_PATH: '.'})
    settings.update({SETTINGS_KEY_CREDENTIALS_LOCATION: G_FILE})

    parser = argparse.ArgumentParser(description='Stringify parser')
    parser.add_argument("-d", "--default-lang", help="Android default language. Default language sets values folder "
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

    parser.add_argument("-u", "--oauth-credentials-location", help="oauth credentials location. Default: .credentials")

    args = parser.parse_args()

    if args.mode:
        settings.update({SETTINGS_KEY_MODE: args.mode.lower()})

    if args.spreadsheet_name:
        settings.update({SETTINGS_KEY_GDOC_NAME: args.spreadsheet_name})
    else:
        log_exception("'Spreadsheet name' shouldn't be empty", force_quit=True)

    if args.default_lang:
        settings.update({SETTINGS_KEY_DEFAULT_LANG: args.default_lang})

    if args.dest_path:
        settings.update({SETTINGS_KEY_EXPORT_PATH: args.dest_path})

    if args.xml_filename:
        settings.update({SETTINGS_KEY_XML_NAME: args.xml_filename})

    if args.logs_off:
        settings.update({SETTINGS_KEY_LOGS_ON, False})

    if args.oauth_credentials_location:
        settings.update({SETTINGS_KEY_CREDENTIALS_LOCATION: args.oauth_credentials_location})


# todo use os.walk instead?
def find_files(path='.', filename_regex=None):
    found_files = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            list = find_files(filepath, filename_regex)
            found_files.extend(list)
        elif os.path.isfile(filepath):
            if filename_regex and filename.startswith(filename_regex):
                found_files.append(filepath)
            elif filename_regex is None:
                found_files.append(filepath)

    return found_files


def save_file(content, dir_name, file_name):
    log_step("Saving file {}/{}".format(dir_name, file_name))
    cwd = os.getcwd()
    try:
        os.mkdir(dir_name)
    except Exception:
        pass

    try:
        os.chdir(dir_name)
    except Exception:
        pass

    file = open(file_name, "w")
    file.write(content)
    file.close()
    os.chdir(cwd)


def main():
    start_seconds = time.time()

    decode_sys_args()
    log_version()

    credentials_location = settings[SETTINGS_KEY_CREDENTIALS_LOCATION]
    mode = settings[SETTINGS_KEY_MODE]

    google_doc_name = settings[SETTINGS_KEY_GDOC_NAME]
    google_docs_handler = GoogleDocsHandler(credentials_location)

    if mode == Mode.IMPORT_ANDROID:
        export_path = settings[SETTINGS_KEY_EXPORT_PATH]
        default_language = settings[SETTINGS_KEY_DEFAULT_LANG]

        filename = settings[
            SETTINGS_KEY_XML_NAME] if SETTINGS_KEY_XML_NAME in settings.keys() else SETTINGS_DEFAULT_XML_NAME

        AndroidProducer(google_docs_handler, google_doc_name,
                        export_path=export_path,
                        xml_name=filename,
                        default_language=default_language).execute()

    if mode == Mode.IMPORT_IOS:
        export_path = settings[SETTINGS_KEY_EXPORT_PATH]
        filename = settings[
            SETTINGS_KEY_XML_NAME] if SETTINGS_DEFAULT_XML_NAME in settings.keys() else SETTINGS_DEFAULT_LOCALIZABLE_NAME

        SwiftProducer(google_docs_handler, google_doc_name,
                      export_path=export_path,
                      filename=filename).execute()

    if mode in (Mode.EXPORT_IOS, Mode.EXPORT_ANDROID):
        path = settings[SETTINGS_KEY_EXPORT_PATH]
        default_language = settings[SETTINGS_KEY_DEFAULT_LANG]

        if mode == Mode.EXPORT_ANDROID:
            xml_name = settings[SETTINGS_KEY_XML_NAME] if SETTINGS_KEY_XML_NAME in settings.keys() \
                else SETTINGS_DEFAULT_XML_NAME
            loader = AndroidStringsLoader(path=path, xml_name=xml_name, default_language=default_language)

        if mode == Mode.EXPORT_IOS:
            filename = settings[SETTINGS_KEY_XML_NAME] if SETTINGS_KEY_XML_NAME in settings.keys() \
                else SETTINGS_DEFAULT_LOCALIZABLE_NAME
            loader = IOSStringsLoader(path=path, filename=filename)

        dictionary = loader.load()
        google_docs_handler.write(google_doc_name, dictionary)

    log_step("Done (took: {} seconds)".format(int(time.time() - start_seconds)))


if __name__ == '__main__':
    main()
