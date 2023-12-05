from prettytable import PrettyTable
from CGSemantic import *
from collections import Counter

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
        semantic_errors = []
        table.field_names = ["Identifier", "Type", "Value", "Scope", "Line"]
        identifiers = list(map(lambda x: x[0], self.table.items()))
        identifiers_counters = Counter(identifiers)
        for symbol, details in self.table.items():
            variable_type = details['type']
            variable_value = details['value']
            table.add_row([symbol, details['type'], details['value'], details['scope'], details['line']])
            is_semantic_error = semantic_types[variable_type](variable_value) is not True
            if is_semantic_error:
                semantic_errors.append({
                    'symbol': symbol,
                    'type': variable_type,
                    'value': variable_value,
                    'scope': details['scope'],
                    'line': details['line']
                })
        print(table)
        if len(semantic_errors) > 0:
            print("Errores en semantica")
            semantic_table = PrettyTable()
            semantic_table.field_names = ["Identifier", "Type", "Value", "Scope", "Line"]
            for error in semantic_errors:
                semantic_table.add_row([error['symbol'], error['type'], error['value'], error['scope'], error['line']])
            print(semantic_table)
        else:
            print("No errores en semantica")

    def get_table(self):
        return self.table
