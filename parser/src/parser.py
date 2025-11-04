import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_statement(p):
    '''statement : declaration
                 | print_statement'''
    if p[1] is True:
        print("Parsing Success!")
        print("SDT Verified!")
    elif p[1] is False:
        print("Parsing Success!")
        print("SDT error...")
    else:
        print("Parsing Success!")

# Declaración
def p_declaration(p):
    'declaration : type ID ASSIGN expression SEMICOLON'
    var_type = p[1]
    value = p[4]

    if value is None:
        p[0] = False
        return

    if var_type == 'int' and isinstance(value, int):
        p[0] = True
    elif var_type == 'float' and isinstance(value, (int, float)):
        p[0] = True
    else:
        p[0] = False

# Declaración print
def p_print_string(p):
    'print_statement : PRINT LPAREN STRING RPAREN SEMICOLON'
    print(f'Output: {p[3]}')
    p[0] = True

def p_print_expr(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    if p[3] is None:
        p[0] = False
    else:
        print(f'Output: {p[3]}')
        p[0] = True

# Tipos
def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]

# Expresiones aritméticas
def p_expression_plus_minus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[1] is None or p[3] is None:
        p[0] = None
        return
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times_div(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[1] is None or p[3] is None:
        p[0] = None
        return
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        if p[3] == 0:
            p[0] = None
        else:
            p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUMBER
              | DECIMAL'''
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = 0

def p_factor_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Parsing error in token '{p.value}' (type {p.type})")
    else:
        print("Parsing error at EOF")

parser = yacc.yacc()
