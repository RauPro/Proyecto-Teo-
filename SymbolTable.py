from prettytable import PrettyTable

class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_symbol(self, symbol, symbol_type=None, value="", scope="0", line="0"):
        if symbol not in self.table:
            self.table[symbol] = {
                'type': symbol_type,
                'value': value,
                'scope': scope,
                'line': line
            }

    def add_value(self, symbol, value):
        if symbol in self.table:
            self.table[symbol]['value'] = value

    def print_table(self):
        table = PrettyTable()
        table.field_names = ["Identifier", "Type", "Value", "Scope", "Line"]
        for symbol, details in self.table.items():
            table.add_row([symbol, details['type'], details['value'], details['scope'], details['line']])
        print(table)

    def get_table(self):
        return self.table
