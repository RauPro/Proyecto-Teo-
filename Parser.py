# ------------------------------------------------------------
# Lexer para C
# ------------------------------------------------------------
import ply.lex as lex
from CGrammar import *

# List of token names.   This is always required
import ply.lex as lex
from SymbolTable import SymbolTable

tokens = (
    'ID',
    'DOT',
    'COMMENT',
    'PLUS',
    'MINUS',
    'PRODUCT',
    'DIVISION',
    'PAREN_L',
    'PAREN_R',
    'BRACE_L',
    'BRACE_R',
    'SEMICOLON',
    'COMMA',
    'PREPROCESSOR',
    'BLOCK_COMMENT',
    'EQUALS',
    'GREATER_THAN',
    'LESS_THAN',
    'GREATER_THAN_EQUAL',
    'LESS_THAN_EQUAL',
    'EQUAL_EQUAL',
    'NOT_EQUAL',
    'AND',
    'OR',
)

reserved = {
    'void': 'VOID',
    'struct': 'STRUCT',
    'using': 'USING',
    'auto': 'AUTO',
    'else': 'ELSE',
    'if': 'IF',
    'return': 'RETURN',
    'while': 'WHILE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'cout': 'COUT',
    'endl': 'ENDL',
    'cin': 'CIN',
}

tokens += tuple(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_PRODUCT = r'\*'
t_EQUALS = r'\='
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_GREATER_THAN_EQUAL = r'\>\='
t_LESS_THAN_EQUAL = r'\<\='
t_EQUAL_EQUAL = r'\=\='
t_NOT_EQUAL = r'\!\='
t_AND = r'\&\&'
t_OR = r'\|\|'
t_DIVISION = r'\/'
t_BRACE_L = r'\{'
t_BRACE_R = r'\}'
t_PREPROCESSOR = r'\#\w+'


symbol_table = SymbolTable()
is_declaring = False
var_type = None
var_name = None
scope_tracking = 0


def t_ID(t):
    r'\b[A-Za-z_][A-Za-z0-9_]*\b'
    t.type = reserved.get(t.value, 'ID')
    global is_declaring
    global var_type
    global var_name
    if t.type in ['INT', 'FLOAT', 'DOUBLE', 'CHAR']:
        is_declaring = True
        var_type = t.type
    elif is_declaring and t.type == 'ID':
        var_name = t.value
    return t


def t_SEMICOLON(t):
    r';'
    global is_declaring
    global var_type
    global var_name
    if is_declaring and var_name:
        symbol_table.add_symbol(var_name, var_type, "Sin asignación", scope_tracking)
        is_declaring = False
    return t


def t_COMMA(t):
    r','
    global is_declaring
    global var_type
    global var_name
    if is_declaring and var_name:
        symbol_table.add_symbol(var_name, var_type, "Sin asignación", scope_tracking)
        is_declaring = False
    return t


def t_PAREN_R(t):
    r'\)'
    global is_declaring
    global var_type
    global var_name
    if is_declaring and var_name:
        symbol_table.add_symbol(var_name, var_type, "Sin asignación", scope_tracking)
        is_declaring = False
    return t


def t_DOT(t):
    r'\.'
    return t


def t_PAREN_L(t):
    r'\('
    global is_declaring
    is_declaring = False
    return t


def t_COMMENT(t):
    r'//.*'
    pass


def t_BLOCK_COMMENT(t):
    r'\/\*(.|\n)*\*\/'
    # return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    #print(f"Caracter no contemplado '{t.value[0]}' linea {t.lineno}")
    t.lexer.skip(1)


t_ignore = ' \t'

lexer = lex.lex()

list_tockens = []

def analyze(data):
    global is_declaring
    global var_type
    global scope_tracking
    global var_name
    count_iterations = 0
    lexer.prev_token_type = None
    is_declaring = False
    var_type = None
    var_name = None
    lexer.input(data)
    print("+------------------ Lista de elementos lexicográficos -------------------+")
    print("+----------------------+-----------------+-----------------+-------------+")
    print("| Type                 | Value           | Line            | Locatio     |")
    print("+----------------------+-----------------+-----------------+-------------+")
    while True:
        tok = lexer.token()
        if not tok:
            break
        count_iterations += 1
        if not is_declaring:
            count_iterations = 0
        if count_iterations == 4 and is_declaring:
            is_declaring = False
            count_iterations = 0
        lexer.prev_token_type = tok.type

        print(f"| {tok.type:20} | {tok.value:15} | {tok.lineno:15} | {tok.lexpos:11} |")
        list_tockens.append(tok.type)

        if tok.value == "{":
            scope_tracking += 1
        elif tok.value == "}":
            scope_tracking -= 1
    print("+----------------------+-----------------+-----------------+-------------+", "\n")

def get_symbol_table():
    return symbol_table.print_table()



def miParser(tokens, ll1_table, start_symbol):
    list_tockens.append('$')
    stack = ['$' , start_symbol]
    while tokens:
        current_token = tokens[0]
        stack_top = stack[-1]

        if stack_top == current_token:
            tokens.pop(0)
            stack.pop()
        elif (stack_top in ll1_table) and (current_token in ll1_table[stack_top]):
            production = ll1_table[stack_top][current_token]
            stack.pop()
            if production != 'ε':
                stack.extend(production.split()[::-1])
        else:
            # Manejo de errores: Activar modo panic?
            raise SyntaxError(f"Error de sintaxis en el token '{current_token}'.")

        # Check if DONE
        if stack == ['$'] and tokens == ['$']:
            return True  # Análisis sintáctico exitoso

    return False  # Análisis sintáctico fallido



from tkinter import Tk
from tkinter.filedialog import askopenfilename
from CGrammar import *
from GenerateLL1Table import *

if __name__ == "__main__":
    Tk().withdraw()
    filename = askopenfilename()
    f = open(filename, 'r')
    code = f.read()
    analyze(code)
    print(list_tockens)
    symbols = get_symbol_table()
    start_symbol = 'Program'
    parser = LL1Parser(grammar)
    parser.print_pretty_ll1_table()
    table = parser.get_ll1_table()
    miParser(list_tockens, table, start_symbol)
