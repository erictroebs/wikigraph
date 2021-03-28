from functools import reduce
from sys import argv

from wikigraph.cli.NamedArgumentError import NamedArgumentError
from wikigraph.cli.NamedParameter import NamedParameter
from wikigraph.cli.SlotArgumentError import SlotArgumentError
from wikigraph.cli.SlotParameter import SlotParameter


class ArgumentParser:
    def __init__(self):
        self.named_parameters = []
        self.slot_parameters = []

        self.help = self.add_named_parameter('help', 'show help')
        self.help_md = self.add_named_parameter('help-md', 'show help formatted as markdown')

    def add_named_parameter(self, name, description, expects=None, default=None, parse=None):
        """
        add named parameter which is identified by a char sequence

        :param name: parameter identifier without starting dashes
        :param description: description which is shown in help
        :param expects: brief description what is expected (None for switches)
        :param default: default value (None for no default value)
        :param parse: function to call if parameter value is found
        :return: NamedParameter object (value is set when calling parse)
        """
        parameter = NamedParameter(name, description, expects, default, parse)
        self.named_parameters.append(parameter)

        return parameter

    def add_slot_parameter(self, name, description, example=None, parse=None):
        """
        add slot parameter which is identified by its position

        :param name: slot name which is shown in help
        :param description: description which is shown in help
        :param example: example value which is shown in help
        :param parse: function to call if parameter value is found
        :return: SlotParameter object (value is set when calling parse)
        """
        parameter = SlotParameter(name, description, example, parse)
        self.slot_parameters.append(parameter)

        return parameter

    def parse(self):
        """
        parse parameters from sys.argv
        """
        # define some helper functions to handle incoming arguments
        last = None
        slot = 0

        def named(name):
            nonlocal last
            if last is not None:
                raise NamedArgumentError(name)

            for p in self.named_parameters:
                if name in p.name:
                    if p.expects is None:
                        p.add(True)
                    else:
                        last = p
                    return

            raise NamedArgumentError(name)

        def slotted(value):
            nonlocal slot
            if slot == len(self.slot_parameters):
                raise SlotArgumentError(slot + 1, value)

            self.slot_parameters[slot].set(value)
            slot += 1

        # iterate over arguments
        for arg in argv[1:]:
            # --
            if arg.startswith('--'):
                named(arg[2:])
            # -
            elif arg.startswith('-') and len(arg) > 1:
                for letter in arg[1:]:
                    named(letter)
            # value
            elif last is not None:
                last.add(arg)
                last = None
            # slot
            else:
                slotted(arg)

        # set default values
        for p in self.named_parameters:
            if p.value is None:
                p.value = p.default

        # print help and exit program if desired
        if self.help.value is True:
            self.print()
            exit(0)
        if self.help_md.value is True:
            self.print(markdown=True)
            exit(0)

    def print(self, indent=4, markdown=False):
        """
        print all known parameters to stdout

        :param indent: indent on new lines
        :param markdown: output as markdown
        :return:
        """
        # print generic call
        slot_names = map(lambda p: f'<{p.name}>', self.slot_parameters)
        slot_names = ' '.join(slot_names)

        if markdown:
            print(f'```wikigraph <additional parameters> {slot_names}```')
            print()
        else:
            print(f'wikigraph <additional parameters> {slot_names}')
            print()

        # print example call
        slot_values = map(lambda p: p.example, self.slot_parameters)
        slot_values = ' '.join(slot_values)

        if markdown:
            print(f'{"#" * indent} example:')
            print(f'```wikigraph {slot_values}```')
            print()
        else:
            print('example:')
            print(f'{" " * indent}wikigraph {slot_values}')
            print()

        # print additional parameters
        name_list_length = max(len('parameter'), reduce(
            max,
            map(lambda p: len(', '.join(p.normalized_name)), self.named_parameters),
        ))
        expects_length = max(len('expects'), reduce(
            max,
            map(lambda p: 0 if p.expects is None else len(str(p.expects)), self.named_parameters)
        ))
        default_length = max(len('default'), reduce(
            max,
            map(lambda p: 0 if p.default is None else len(str(p.default)), self.named_parameters)
        ))
        description_length = max(len('description'), reduce(
            max,
            map(lambda p: len(p.description), self.named_parameters)
        ))

        if markdown:
            print(f'{"#" * indent} additional parameters:')
            print(
                'parameter'.ljust(name_list_length),
                'expects'.ljust(expects_length),
                'default'.ljust(default_length),
                'description',
                sep=' | '
            )
            print(
                '-' * name_list_length,
                '-' * expects_length,
                '-' * default_length,
                '-' * description_length,
                sep=' | '
            )
        else:
            print('additional parameters:')

        for p in self.named_parameters:
            name_list = ', '.join(p.normalized_name)

            if markdown:
                expects = '' if p.expects is None else f'{p.expects}'
                default = '' if p.default is None else f'{p.default}'
                print(
                    name_list.ljust(name_list_length),
                    expects.ljust(expects_length),
                    default.ljust(default_length),
                    p.description,
                    sep=' | '
                )
            else:
                expects = '' if p.expects is None else f' <{p.expects}>'
                default = '' if p.default is None else f' (default: {p.default})'
                print(f'{" " * indent}{name_list}{expects}{default}')
                print(f'{"  " * indent}{p.description}')
