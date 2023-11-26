def calculate_first(grammar):
    first = {key: set() for key in grammar.keys()}

    def first_of(symbol):
        # If the symbol is a terminal, return it
        if symbol not in grammar:
            return {symbol}

        # If it's a non-terminal and hasn't been calculated yet
        if not first[symbol]:
            for production in grammar[symbol]:
                for prod_symbol in production.split():
                    # Recursively calculate first of the symbol
                    first_set = first_of(prod_symbol)

                    # Add non-epsilon symbols to the first set
                    first[symbol].update(first_set - {"ε"})

                    # If epsilon is not in the first set, stop
                    if "ε" not in first_set:
                        break
                else:
                    # If we reached here, all symbols in production have epsilon in their first set
                    first[symbol].add("ε")

        return first[symbol]

    # Calculate first for all symbols
    for non_terminal in grammar:
        first_of(non_terminal)

    return first


def calculate_follow(grammar, first):
    follow = {key: set() for key in grammar.keys()}
    start_symbol = next(iter(grammar))  # Assuming the first symbol is the start symbol
    follow[start_symbol].add("$")  # EOF symbol

    def follow_of(non_terminal):
        for head, productions in grammar.items():
            for production in productions:
                production_symbols = production.split()
                for i, symbol in enumerate(production_symbols):
                    if symbol == non_terminal:
                        # Lookahead symbols in the production
                        next_symbols = production_symbols[i + 1:]

                        if next_symbols:
                            first_of_next = set()
                            for next_symbol in next_symbols:
                                # Consider terminals directly
                                if next_symbol not in grammar:
                                    first_of_next.add(next_symbol)
                                    break
                                else:
                                    first_set = first[next_symbol]
                                    first_of_next.update(first_set)
                                    if "ε" not in first_set:
                                        break
                            else:
                                first_of_next.add("ε")

                            follow[non_terminal].update(first_of_next - {"ε"})

                            # If epsilon is in first of the rest, add follow of head
                            if "ε" in first_of_next:
                                follow[non_terminal].update(follow[head])
                        else:
                            # If there's nothing after the non-terminal, add follow of head
                            follow[non_terminal].update(follow[head])

    # Calculate follow for all non-terminals, repeat until no changes
    while True:
        follow_before = {k: v.copy() for k, v in follow.items()}
        for non_terminal in grammar:
            follow_of(non_terminal)
        if follow_before == follow:
            break

    return follow


def create_ll1_table(grammar, first, follow):
    # Collect all terminals including $ for the columns of the table
    terminals = set()
    for productions in grammar.values():
        for production in productions:
            for symbol in production.split():
                if symbol not in grammar and symbol != 'ε':
                    terminals.add(symbol)
    terminals.add('$')  # End of file symbol

    # Initialize the table with empty entries
    table = {non_terminal: {terminal: "" for terminal in terminals} for non_terminal in grammar}

    # Fill the table
    for non_terminal, productions in grammar.items():
        for production in productions:
            first_of_production = set()

            # Split the production into symbols
            production_symbols = production.split()

            # Calculate FIRST of the production
            for symbol in production_symbols:
                if symbol in grammar:  # Non-terminal symbols
                    first_of_production.update(first[symbol] - {'ε'})
                    if 'ε' not in first[symbol]:
                        break
                else:  # Terminal symbol
                    first_of_production.add(symbol)
                    break
            else:
                # If we reached the end, add 'ε'
                first_of_production.add('ε')

            # Fill the table with the production
            for terminal in first_of_production:
                if terminal != 'ε':
                    table[non_terminal][terminal] = production

            if 'ε' in first_of_production or production == 'ε':
                for terminal in follow[non_terminal]:
                    table[non_terminal][terminal] = production

    return table


def print_ll1_table(table):
    terminals = sorted(list(table[next(iter(table))].keys()))
    print(f"{'':<10}", end="")
    for terminal in terminals:
        print(f"{terminal:<10}", end="")
    print()

    for non_terminal, row in table.items():
        print(f"{non_terminal:<10}", end="")
        for terminal in terminals:
            print(f"{row[terminal]:<10}", end="")
        print()

from prettytable import PrettyTable

def print_pretty_ll1_table(table):
    # Collect the terminals for the columns, sorted for consistent ordering
    terminals = sorted(list(table[next(iter(table))].keys()))

    # Create a pretty table with the first row as the headers
    pretty_table = PrettyTable()
    pretty_table.field_names = ["Non-Terminal"] + terminals

    # Fill the pretty table with data
    for non_terminal, row in table.items():
        pretty_table.add_row([non_terminal] + [row[terminal] for terminal in terminals])

    # Print the formatted table
    print(pretty_table)


if __name__ == '__main__':
    """grammar = {
        "E": ["T E'"],
        "E'": ["+ T E'", "ε"],
        "T": ["F T'"],
        "T'": ["* F T'", "ε"],
        "F": ["( E )", "id"]
    }"""
    grammar = {
        "Program": ["PreprocessorList GlobalDeclarationList"],
        "PreprocessorList": ["PreprocessorDirective PreprocessorList", "ε"],
        "PreprocessorDirective": ["PREPROCESSOR < ID >"],
        "GlobalDeclarationList": ["GlobalDeclaration GlobalDeclarationList", "ε"],
        "GlobalDeclaration": ["FunctionDec", "TypeDec", "VarDec"],
        "Statement": ["ID StatementRest", "IfStatement", "WhileStatement", "CoutStatement", "BlockStatement", "TypeDec",
                      "FunctionDec"],
        "StatementRest": ["= Expression ;", ". ID = Expression ;"],
        "IfStatement": ["if ( Expression ) Statement IfStatementRest"],
        "IfStatementRest": ["else Statement", "ε"],
        "WhileStatement": ["while ( Expression ) Statement"],
        "CoutStatement": ["cout << Expression CoutRest ;"],
        "CoutRest": ["<< endl", "ε"],
        "BlockStatement": ["{ StatementList }"],
        "StatementList": ["Statement StatementList", "ε"],
        "TypeDec": ["struct ID { VarDecList } ;"],
        "VarDec": ["Type ID VarDecRest ;"],
        "VarDecRest": ["= Expression", "ε"],
        "VarDecList": ["VarDec VarDecList", "ε"],
        "Type": ["int", "float", "char"],
        "FunctionDec": ["Type ID ( FormalList ) { VarDecList StatementList return Expression ; }"],
        "Expression": ["LogicalOrExpression"],
        "LogicalOrExpression": ["LogicalAndExpression MoreLogicalOr"],
        "MoreLogicalOr": ["|| LogicalAndExpression MoreLogicalOr", "ε"],
        "LogicalAndExpression": ["EqualityExpression MoreLogicalAnd"],
        "MoreLogicalAnd": ["&& EqualityExpression MoreLogicalAnd", "ε"],
        "EqualityExpression": ["RelationalExpression MoreEquality"],
        "MoreEquality": ["EqualityOperator RelationalExpression MoreEquality", "ε"],
        "EqualityOperator": ["==", "!="],
        "RelationalExpression": ["AdditiveExpression MoreRelational"],
        "MoreRelational": ["RelationalOperator AdditiveExpression MoreRelational", "ε"],
        "RelationalOperator": ["<", ">", "<=", ">="],
        "AdditiveExpression": ["Term MoreAdditive"],
        "MoreAdditive": ["AdditiveOperator Term MoreAdditive", "ε"],
        "AdditiveOperator": ["+", "-"],
        "Term": ["Factor MoreMultiplicative"],
        "MoreMultiplicative": ["MultiplicativeOperator Factor MoreMultiplicative", "ε"],
        "MultiplicativeOperator": ["*", "/"],
        "Factor": ["( Expression )", "ID"],
        "ExpList": ["Expression ExpRest", "ε"],
        "ExpRest": [", Expression ExpRest", "ε"],
        "FormalList": ["Parameter FormalRest", "ε"],
        "FormalRest": [", Parameter FormalRest", "ε"],
        "Parameter": ["Type ID"]
    }

    first = calculate_first(grammar)
    follow = calculate_follow(grammar, first)

    print("First:")
    for non_terminal, first_set in first.items():
        print(non_terminal, first_set)
    print("Follow:")
    for non_terminal, follow_set in follow.items():
        print(non_terminal, follow_set)

    ll1_table = create_ll1_table(grammar, first, follow)
    print("LL1 Table:")
    #print_ll1_table(ll1_table)
    print_pretty_ll1_table(ll1_table)
