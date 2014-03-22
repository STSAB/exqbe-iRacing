import exproto_pb2 as proto


class Config:

    def __init__(self, config_file):
        self.configuration = proto.Configuration()
        self.configuration.ParseFromString(open(config_file, 'rb').read())

        # Map sensor id to

    def get_definition(self, address):
        # Find the correct sensor definition
        definitions = filter(lambda x: x.HasField('sensor_address') and x.sensor_address == address,
                             self.configuration.sensor_definitions)
        if len(definitions) == 0:
            raise ValueError('Address {} not in configuration'.format(address))
        elif len(definitions) > 1:
            raise ValueError('Address {} appears multiple times in configuration'.format(address))
        return definitions[0]

    def apply_formulas(self, address, value):
        definition = self.get_definition(address)
        # Apply formulas in reverse
        for formula in reversed(definition.sensor_formulas):
            if formula.HasField('linear_equation'):
                m = 1.0 if not formula.linear_equation.HasField('M') else formula.linear_equation.M
                b = 0.0 if not formula.linear_equation.HasField('B') else formula.linear_equation.B
                value = value / m - b

        return value
