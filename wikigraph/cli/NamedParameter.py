class NamedParameter:
    def __init__(self, name, description, expects=None, default=None, parse=None):
        if not isinstance(name, list):
            name = [name]

        self.name = name
        self.description = description
        self.expects = expects
        self.default = default
        self.parse = parse

        self.value = None

    @property
    def normalized_name(self):
        return list(map(lambda n: ('-' if len(n) == 1 else '--') + n, self.name))

    def add(self, value):
        if self.parse is not None:
            value = self.parse(value)

        if self.value is None:
            self.value = value
            return
        if not isinstance(self.value, list):
            self.value = [self.value]

        self.value.append(value)
