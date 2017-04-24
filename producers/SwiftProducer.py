import os
import io

from producers.AndroidProducer import Producer
from utils.FileUtils import save_file
from utils.LogUtils import log_step


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
