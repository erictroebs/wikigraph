class SlotParameter:
    def __init__(self, name, description, example=None, parse=None):
        self.name = name
        self.description = description
        self.example = example
        self.parse = parse

        self.value = None

    def set(self, value):
        if self.parse is not None:
            value = self.parse(value)

        self.value = value
