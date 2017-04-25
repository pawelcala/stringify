import re

import pygsheets
import time

from pygsheets import Cell

from model.Base import Command
from model.Models import Dictionary
from utils import cell_decorator
from utils.LogUtils import log_step


class GoogleDocsHandler(Command):
    def __init__(self, credentials_path):
        self.client = None
        self.credentials_path = credentials_path

    def _authorize(self):
        if not self.client:
            self.client = pygsheets.authorize(outh_file=self.credentials_path, outh_nonlocal=True)
        return self.client

    def write(self, google_doc_name, dictionary):
        worksheet = self._get_worksheet(google_doc_name)

        log_step("Clear spreadsheet...")
        self._clear_worksheet(worksheet)
        log_step("Writing cells...")
        start_time = time.time()

        cells = []
        row = 1
        languages = dictionary.languages
        languages = sorted(languages)
        for index, lang in enumerate(languages):
            column = index + 2
            cell = Cell((row, column))
            cell.value = lang
            cells.append(cell)

        row = 2
        for key in dictionary.keys():
            cell = Cell((row, 1))
            cell.value = key
            cells.append(cell)

            for index, lang in enumerate(languages):
                column = index + 2
                translated_value = dictionary.get_translation(key, lang)
                translated_value = cell_decorator.encode(translated_value)
                cell = Cell((row, column))
                cell.value = translated_value
                cells.append(cell)
            row += 1
        worksheet.update_cells(cell_list=cells)
        log_step("Done writing cells ({} seconds)".format(int(time.time() - start_time)))

    def _get_worksheet(self, google_doc_name):
        google_doc_client = self._authorize()
        try:
            spreadsheet = google_doc_client.open(google_doc_name).sheet1
        except Exception:
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
                key = row[0]
                value = row[i + 1]
                value = cell_decorator.decode(value)
                dictionary.add_translation(key, lang, value)
        return dictionary

    def _clear_worksheet(self, worksheet):
        worksheet.clear()

    def _load_languages(self, sheet):
        log_step("Reading languages")
        column = 2
        languages = []
        while True:
            lang_code = sheet.cell((1, column)).value
            if len(lang_code.strip()) > 0:
                languages.append(lang_code)
                column += 1
            else:
                return languages

    def _read_row(self, sheet, row, langs_count):
        row_data = list()
        for column in range(1, langs_count + 2):
            cell_value = sheet.cell((row, column)).value
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
