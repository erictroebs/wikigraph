class SlotArgumentError(Exception):
    def __init__(self, index, value):
        self.index = index
        self.value = value
