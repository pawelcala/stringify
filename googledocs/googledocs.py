import re

import pygsheets
import time

from pygsheets import Cell

from model.base import Command
from model.models import Dictionary
from utils.log_utils import log_step


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
        worksheet_cells = worksheet.get_all_values(returnas='cell', include_empty=False)

        languages_row = worksheet_cells[0]
        values_rows = worksheet_cells[1:]

        languages = self._load_languages(languages_row)
        entries = self._read_strings(values_rows)
        dictionary = Dictionary()

        for i, lang in enumerate(languages):
            for row in entries:
                if len(row) == 0:
                    continue
                dictionary.add_translation(row[0], lang, row[i + 1])
        return dictionary

    def _clear_worksheet(self, worksheet):
        worksheet.clear()

    def _load_languages(self, languages_row):
        log_step("Reading languages")
        languages = []
        for lang_cell in languages_row:
            lang_code = lang_cell.value.strip()
            if len(lang_code) > 0:
                languages.append(lang_code)

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

    def _read_strings(self, worksheet_cells):
        log_step("Reading spreadsheet cells")
        rows = []
        for row in worksheet_cells:
            rows.append([x.value for x in row])
        return rows
