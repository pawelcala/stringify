class NotFoundException(Exception):
    pass


class Command:
    def execute(self):
        pass


class DataImporter(Command):
    def execute(self):
        raise NotImplemented

    def load(self):
        return self.execute()
