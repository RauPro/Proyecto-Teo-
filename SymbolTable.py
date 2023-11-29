from collections import defaultdict

class SymbolTable:
    def __init__(self):
        self.table = defaultdict(lambda: None)

    def add_symbol(self, symbol, symbol_type=None, value="", scope="0"):
        if symbol not in self.table:
            self.table[symbol] = {
                'type': symbol_type,
                'value': value,
                'scope': scope,
            }
    def add_value(self, symbol, value):
        if symbol in self.table:
            self.table[symbol]['value'] = value
    def print_table(self):
        print("+----------------------- Tabla de Simbolos --------------------------+")
        print("+----------------------+-------------+-----------------+-------------+")
        print("| Identifier           | Type        | Value           | Scope       |")
        print("+----------------------+-------------+-----------------+-------------+")
        for symbol, details in self.table.items():
            print(f"| {symbol:20} | {details['type']:11} | {details['value']:15} | {details['scope']:11} |")
        print("+----------------------+-------------+-----------------+-------------+")

    def get_table(self):
        return self.table