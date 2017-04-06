import argparse
import io
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

import gspread
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

arg_doc_name = 'gspread'
arg_default_lang = "en"
arg_export_path = "res"
arg_ios_export_path = "ios"

G_CLIENT_ID = 'GOOGLE API CONSOLE ID'
G_CLIENT_SECRET = 'GOOGLE API CONSOLE SECRET'
G_SCOPE = 'https://spreadsheets.google.com/feeds'
G_REDIRECT = 'http://localhost/'
G_FILE = ".credentials"


def decode_sys_args():
    global arg_doc_name
    global arg_default_lang
    global arg_export_path
    global arg_ios_export_path

    parser = argparse.ArgumentParser(description='Stringify parser')
    parser.add_argument("-d", "--default", help="Android default language")
    parser.add_argument("-n", "--name", help="GSheet Name")
    parser.add_argument("-p", "--path", help="Export strings path")
    parser.add_argument("-i", "--ipath", help="Export swift path")

    args = parser.parse_args()

    if args.default:
        arg_default_lang = args.default

    if args.name:
        arg_doc_name = args.name

    if args.path:
        arg_export_path = args.path

    if args.ipath:
        arg_ios_export_path = args.ipath


def load_credentials():
    try:
        storage = Storage(G_FILE)
        return storage.locked_get()
    except Exception:
        return None


def save_credentials(credentials):
    storage = Storage(G_FILE)
    storage.locked_put(credentials)


def oauth():
    credentials = load_credentials()
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
        save_credentials(credentials)
        return credentials


def load_languages(sheet):
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


def export_android(languages, strings):
    cwd = os.getcwd()
    if arg_export_path:
        try:
            os.mkdir(arg_export_path)
        except Exception:
            pass
        os.chdir(arg_export_path)

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

        dir_name = "values".format(arg_default_lang) if arg_default_lang == lang else "values-{}".format(lang)
        save_file(pretty_dom, dir_name, "strings.xml")

    os.chdir(cwd)


def export_ios(languages, strings):
    cwd = os.getcwd()
    if arg_ios_export_path:
        try:
            os.mkdir(arg_ios_export_path)
        except Exception:
            pass
        os.chdir(arg_ios_export_path)

    for i, lang in enumerate(languages):
        output = io.StringIO()
        for row in strings:
            if len(row) == 0:
                continue
            output.write('"{}" = "{}";\n'.format(row[0], row[i + 1]))
        save_file(output.getvalue(), None, "{}.strings".format(lang))

    os.chdir(cwd)


if __name__ == '__main__':
    decode_sys_args()
    credentials = oauth()
    gc = gspread.authorize(credentials)
    book = gc.open(arg_doc_name)
    sheet = book.sheet1

    languages = load_languages(sheet)
    strings = read_strings(sheet, len(languages))

    export_android(languages, strings)
    export_ios(languages, strings)
