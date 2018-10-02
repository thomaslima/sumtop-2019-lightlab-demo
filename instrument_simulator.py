from math import log
from random import random
from time import sleep
sign = lambda x: (1, -1)[x < 0]


class InvalidCommand(RuntimeError):
    pass


def get_diode_voltage(current):
    kT = 0.025  # eV
    n = 1.7  # efficiency term
    dark_current = 1e-9  # A
    Rseries = 0.1  # Ohm
    noise_current = current * 0.01  # % of current

    current += (2 * random() - 1) * noise_current

    sleep(0.2)

    if current < -dark_current:
        return current * Rseries  # 20 ohm series resistance
    return n * kT * log(1 + current / dark_current) + Rseries * current


class DemoActualInstrument(object):
    ''' This class simulates the instrument defined in Demo.ipynb
    '''

    state = None

    def __init__(self):
        self.state = {'ENABLE': '0',
                      'CURR': 0,
                      'PROTVOLT': None,
                      }

    def parse_command(self, command):
        # a command can be like COMMAND? or COMMAND XYZ, otherwise invalid

        split_command = command.split(' ')

        if len(split_command) > 0 and split_command[0].endswith('?'):
            command_key = split_command[0][:-1]
            if command_key not in ('VOLT'):
                try:
                    return self.state[command_key]
                except KeyError:
                    raise InvalidCommand('{} is not in {}'.format(split_command[0][:-1], list(self.state.keys())))
            else:
                if self.state['ENABLE'] == '1':
                    diode_voltage = get_diode_voltage(self.state['CURR'])
                    if abs(diode_voltage) > self.state['PROTVOLT']:
                        return sign(diode_voltage) * self.state['PROTVOLT']
                    else:
                        return diode_voltage
                else:
                    raise InvalidCommand('Instrument is disabled. Cannot measure voltage.')

        elif len(split_command) == 2:
            # procedure for setting command to x
            return self.parse_command_value(*split_command)

        # Catch all error
        raise InvalidCommand(command)

    def parse_command_value(self, command, value):
        if command == 'ENABLE':
            if value not in ('0', '1'):
                raise InvalidCommand("Invalid value '{}'. Should be '0' or '1'.")
            if self.state['ENABLE'] == '1':
                self.state['ENABLE'] = value
            elif value == '1':
                if self.state['PROTVOLT'] is None:
                    raise InvalidCommand("Undefined protection voltage. Set it before turning on equipment.")
                self.state['ENABLE'] = value
        elif command in ('CURR', 'PROTVOLT'):
            self.state[command] = float(value)
