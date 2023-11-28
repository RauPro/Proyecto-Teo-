from prettytable import PrettyTable

class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = self.calculate_first()
        self.follow = self.calculate_follow()
        self.table = self.create_ll1_table()

    def calculate_first(self):
        first = {key: set() for key in self.grammar.keys()}

        def first_of(symbol):
            if symbol not in self.grammar:
                return {symbol}

            if not first[symbol]:
                for production in self.grammar[symbol]:
                    for prod_symbol in production.split():
                        first_set = first_of(prod_symbol)
                        first[symbol].update(first_set - {"ε"})
                        if "ε" not in first_set:
                            break
                        else:
                            first[symbol].add("ε")

            return first[symbol]

        for non_terminal in self.grammar:
            first_of(non_terminal)

        return first

    def calculate_follow(self):
        follow = {key: set() for key in self.grammar.keys()}
        start_symbol = next(iter(self.grammar))
        follow[start_symbol].add("$")

        while True:
            follow_before = {k: v.copy() for k, v in follow.items()}
            for head, productions in self.grammar.items():
                for production in productions:
                    production_symbols = production.split()
                    for i, symbol in enumerate(production_symbols):
                        if symbol in follow:
                            next_symbols = production_symbols[i + 1:]
                            first_of_next = set()
                            for next_symbol in next_symbols:
                                if next_symbol in self.grammar:
                                    first_of_next.update(self.first[next_symbol] - {"ε"})
                                    if "ε" not in self.first[next_symbol]:
                                        break
                                else:
                                    first_of_next.add(next_symbol)
                                    break
                            else:
                                first_of_next.add("ε")

                            follow[symbol].update(first_of_next - {"ε"})
                            if "ε" in first_of_next:
                                follow[symbol].update(follow[head])

            if follow_before == follow:
                break

        return follow

    def create_ll1_table(self):
        terminals = set()
        for productions in self.grammar.values():
            for production in productions:
                for symbol in production.split():
                    if symbol not in self.grammar and symbol != 'ε':
                        terminals.add(symbol)
        terminals.add('$')

        table = {non_terminal: {terminal: "" for terminal in terminals} for non_terminal in self.grammar}
        for non_terminal, productions in self.grammar.items():
            for production in productions:
                first_of_production = set()
                production_symbols = production.split()
                for symbol in production_symbols:
                    if symbol in self.grammar:
                        first_of_production.update(self.first[symbol] - {'ε'})
                        if 'ε' not in self.first[symbol]:
                            break
                    else:
                        first_of_production.add(symbol)
                        break
                else:
                    first_of_production.add('ε')

                for terminal in first_of_production:
                    if terminal != 'ε':
                        table[non_terminal][terminal] = production

                if 'ε' in first_of_production or production == 'ε':
                    for terminal in self.follow[non_terminal]:
                        table[non_terminal][terminal] = production

        return table

    def print_pretty_ll1_table(self):
        pretty_table = PrettyTable()
        terminals = sorted(list(self.table[next(iter(self.table))].keys()))
        pretty_table.field_names = ["Non-Terminal"] + terminals
        for non_terminal, row in self.table.items():
            pretty_table.add_row([non_terminal] + [row[terminal] for terminal in terminals])
        print(pretty_table)

    def get_ll1_table(self):
        return self.first, self.follow, self.table

if __name__ == '__main__':
    """grammar = {
        "E": ["T E'"],
        "E'": ["+ T E'", "ε"],
        "T": ["F T'"],
        "T'": ["* F T'", "ε"],
        "F": ["( E )", "id"]
    }"""


