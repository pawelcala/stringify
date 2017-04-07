#!/usr/bin/env python3

# system imports
import argparse
import io
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from enum import Enum

# Dependency imports
import gspread
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


class NotFoundException(Exception):
    pass


class Mode(Enum):
    EXPORT_ALL = 0
    EXPORT_ANDROID = 1
    EXPORT_IOS = 2
    IMPORT_ANDROID = 3
    IMPORT_IOS = 4


APP_NAME = "stringify"
APP_VERSION = "0.0.2"

SETTINGS_KEY_GDOC_NAME = "spreadsheet_name"
SETTINGS_KEY_DEFAULT_LANG = "default_language"
SETTINGS_KEY_EXPORT_PATH = "locale"
SETTINGS_KEY_XML_NAME = "xml_name"
SETTINGS_KEY_MODE = "mode"
SETTINGS_KEY_LOGS_ON = "logs_on"

SETTINGS_DEFAULT_LANG = "en"
SETTINGS_DEFAULT_MODE = Mode.EXPORT_ALL.name
SETTINGS_DEFAULT_XML_NAME = "strings.xml"
SETTINGS_DEFAULT_LOGS_ON = True

settings = dict()
settings.update({SETTINGS_KEY_DEFAULT_LANG: SETTINGS_DEFAULT_LANG})
settings.update({SETTINGS_KEY_MODE: SETTINGS_DEFAULT_MODE})
settings.update({SETTINGS_KEY_XML_NAME: SETTINGS_DEFAULT_XML_NAME})
settings.update({SETTINGS_KEY_LOGS_ON: SETTINGS_DEFAULT_LOGS_ON})
settings.update({SETTINGS_KEY_EXPORT_PATH: None})

G_CLIENT_ID = 'GOOGLE API CONSOLE ID'
G_CLIENT_SECRET = 'GOOGLE API CONSOLE SECRET'
G_SCOPE = 'https://spreadsheets.google.com/feeds'
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
    log_step("Decoding script arguments")
    global settings

    parser = argparse.ArgumentParser(description='Stringify parser')
    parser.add_argument("-d", "--default-lang", help="Android default language")
    parser.add_argument("-n", "--spreadsheet-name", help="Google Spreadsheet name")
    parser.add_argument("-p", "--export-path", help="Localized strings destination path")
    parser.add_argument("-x", "--export-xml-name", help="Android xml name. Default: strings.xml")
    parser.add_argument("-m", "--mode",
                        help="Available modes: "
                             "EXPORT_IOS - exports ios strings,\n"
                             "EXPORT_ANDROID - exports android strings,\n"
                             "IMPORT_ANDROID - import Android strings and create Google Spreadsheet,\n"
                             "IMPORT_IOS - import iOS strings and create Google Spreadsheet,\n"
                             "EXPORT_ALL (default) - exports both Android and iOS\n")
    parser.add_argument("-o", "--logs-off", help="Turns progress logs off")

    args = parser.parse_args()

    if args.mode:
        settings.update({SETTINGS_KEY_MODE: args.mode})

    if args.spreadsheet_name:
        settings.update({SETTINGS_KEY_GDOC_NAME: args.spreadsheet_name})
    else:
        log_exception("'Spreadsheet name' shouldn't be empty", force_quit=True)

    if args.default_lang:
        settings.update({SETTINGS_KEY_DEFAULT_LANG: args.default_lang})

    if args.export_path:
        settings.update({SETTINGS_KEY_EXPORT_PATH: args.export_path})

    if args.export_xml_name:
        settings.update({SETTINGS_KEY_XML_NAME: args.export_xml_name})

    if args.logs_off:
        settings.update({SETTINGS_KEY_LOGS_ON, False})


def oauth_load_credentials():
    log_step("Loading saved credentials")
    try:
        storage = Storage(G_FILE)
        return storage.locked_get()
    except Exception:
        log_step("No saved credentials")
        return None


def oauth_save_credentials(credentials):
    log_step("Saving credentials")
    storage = Storage(G_FILE)
    storage.locked_put(credentials)


def oauth():
    log_step("Authorizing user")
    credentials = oauth_load_credentials()
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
        oauth_save_credentials(credentials)
        return credentials


def load_languages(sheet):
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


def read_row(sheet, row, langs_count):
    row_data = list()
    for column in range(1, langs_count + 2):
        cell_value = sheet.cell(row, column).value
        if len(cell_value.strip()) == 0 and column == 1:
            return row_data
        else:
            row_data.append(cell_value)
    return row_data


def read_strings(sheet, langs_count):
    log_step("Reading spreadsheet cells")
    row = 2
    rows = []
    empty_row = False
    while True:
        row_data = read_row(sheet, row, langs_count)
        if len(row_data) == 0:
            if empty_row:
                return rows
            else:
                empty_row = True
        else:
            empty_row = False

        rows.append(row_data)
        row += 1


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


def export_android(languages, strings,
                   export_path=None,
                   default_language=SETTINGS_DEFAULT_LANG,
                   xml_file_name=SETTINGS_DEFAULT_XML_NAME):
    log_step("Exporting Android strings")
    cwd = os.getcwd()
    if export_path:
        try:
            os.mkdir(export_path)
        except Exception:
            pass
        os.chdir(export_path)

    for i, lang in enumerate(languages):
        xml = ET.Element('resources')
        for row in strings:
            if len(row) == 0:
                continue
            string_row = ET.SubElement(xml, 'string')
            string_row.set('name', row[0])
            string_row.text = row[i + 1]

        dom = minidom.parseString(ET.tostring(xml, 'utf-8'))
        pretty_dom = dom.toprettyxml()

        dir_name = "values".format(default_language) if default_language == lang else "values-{}".format(lang)
        save_file(pretty_dom, dir_name, xml_file_name)

    os.chdir(cwd)


def export_ios(languages, strings, export_path=None):
    log_step("Exporting iOS strings")
    cwd = os.getcwd()
    if export_path:
        try:
            os.mkdir(export_path)
        except:
            pass

        os.chdir(export_path)

    for i, lang in enumerate(languages):
        output = io.StringIO()
        for row in strings:
            if len(row) == 0:
                continue
            output.write('"{}" = "{}";\n'.format(row[0], row[i + 1]))

        language_dir = "{}.lproj".format(lang)
        save_file(output.getvalue(), language_dir, "Localizable.strings")

    os.chdir(cwd)


def handle_export(mode, gdoc_name):
    book = gc.open(gdoc_name)
    sheet = book.sheet1

    languages = load_languages(sheet)
    strings = read_strings(sheet, len(languages))

    if mode in (Mode.EXPORT_ANDROID.name, Mode.EXPORT_ALL.name):
        export_android(languages,
                       strings,
                       settings[SETTINGS_KEY_EXPORT_PATH],
                       settings[SETTINGS_KEY_DEFAULT_LANG],
                       settings[SETTINGS_KEY_XML_NAME])

    if mode in (Mode.EXPORT_IOS.name, Mode.EXPORT_ALL.name):
        export_ios(languages, strings, settings[SETTINGS_KEY_EXPORT_PATH])


if __name__ == '__main__':
    log_version()

    decode_sys_args()
    credentials = oauth()
    gc = gspread.authorize(credentials)

    script_mode = settings[SETTINGS_KEY_MODE]
    gdoc_name = settings[SETTINGS_KEY_GDOC_NAME]

    if script_mode in (Mode.EXPORT_ALL.name, Mode.EXPORT_ANDROID.name, Mode.EXPORT_IOS):
        handle_export(script_mode, gdoc_name)
    if script_mode in (Mode.IMPORT_ANDROID.name, Mode.IMPORT_IOS.name):
        raise NotImplemented

    log_step("Done")
