# ------------------------------------------------------------
# Lexer para C
# ------------------------------------------------------------
import ply.lex as lex
from ParseTable import *

# List of token names.   This is always required
import ply.lex as lex
from SymbolTable import SymbolTable

tokens = (
    'ID',
    'NUMBER',
    'STRING',
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
    'END_INSTRUCTION',
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
t_END_INSTRUCTION = r'\;'


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


def t_PAREN_L(t):
    r'\('
    global is_declaring
    is_declaring = False
    return t


def t_NUMBER(t):
    r'\b\d+\b'
    global is_declaring
    global var_type
    global var_name
    if is_declaring and var_name:
        t.value = int(t.value)
        symbol_table.add_symbol(var_name, var_type, t.value, scope_tracking)
        is_declaring = False
    return t


def t_STRING(t):
    r'"[^"]*"'
    global is_declaring
    global var_type
    global var_name
    if is_declaring and var_name:
        symbol_table.add_symbol(var_name, f"Variable: {var_type} with value {t.value}")
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

table = parse_table


stack = ['eof', 0]


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


        if tok.value == "{":
            scope_tracking += 1
        elif tok.value == "}":
            scope_tracking -= 1
    print("+----------------------+-----------------+-----------------+-------------+", "\n")

def get_symbol_table():
    return symbol_table.print_table()



def miParser():
    # f = open('fuente.c','r')
    # lexer.input(f.read())
    lexer.input('total_mujeres+total_hombres$')

    tok = lexer.token()
    x = stack[-1]  # primer elemento de der a izq
    while True:
        print(tok.type)
        print(x)
        if x == tok.type and x == 'eof':
            print("Cadena reconocida exitosamente")
            return  # aceptar
        else:
            if x == tok.type and x != 'eof':  # llegué a un camino de derivación completo
                stack.pop()
                x = stack[-1]
                tok = lexer.token()
            if x in tokens and x != tok.type:
                print("Error: se esperaba ", tok.type)
                print('en la posicion: ', tok.lexpos);
                return 0;
            if x not in tokens:  # es no terminal
                celda = buscar_en_tabla(x, tok.type)
                if celda is None:
                    print("Error: NO se esperaba", tok.type)
                    print('en la posicion: ', tok.lexpos);
                    return 0;
                else:
                    stack.pop()
                    agregar_pila(celda)
                    x = stack[-1]
        print(stack)
        print()

        # if not tok:
        # break
        # print(tok)
        # print(tok.type, tok.value, tok.lineno, tok.lexpos)


def buscar_en_tabla(no_terminal, terminal):
    for i in range(len(table)):
        if (table[i][0] == no_terminal and table[i][1] == terminal):
            return table[i][2]  # retorno la celda


def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != 'vacia':  # la vacía no la inserta
            stack.append(elemento)




from tkinter import Tk
from tkinter.filedialog import askopenfilename


if __name__ == "__main__":
    Tk().withdraw()
    filename = askopenfilename()
    f = open(filename, 'r')
    code = f.read()
    analyze(code)
    symbols = get_symbol_table()
