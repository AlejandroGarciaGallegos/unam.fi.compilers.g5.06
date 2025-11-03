import ply.yacc as yacc
from lexer import tokens

symbol_table = {}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

#Producciones

def p_statement_int(p):
    'statement : INT ID ASSIGN expression'
    var_type = 'int'
    var_name = p[2]
    value = p[4]

    if isinstance(value, int):
        symbol_table[var_name] = value
        print("Parsing Success!\nSDT Verified!")
    else:
        print("Parsing Success!\nSDT error... (Type mismatch)")

def p_statement_float(p):
    'statement : FLOAT ID ASSIGN expression'
    var_type = 'float'
    var_name = p[2]
    value = p[4]

    if isinstance(value, (int, float)):
        symbol_table[var_name] = float(value)
        print("Parsing Success!\nSDT Verified!")
    else:
        print("Parsing Success!\nSDT error... (Type mismatch)")

# Expresiones

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        try:
            p[0] = p[1] / p[3]
        except ZeroDivisionError:
            print("SDT error... División entre cero")
            p[0] = 0

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUMBER
              | DECIMAL'''
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    if p[1] in symbol_table:
        p[0] = symbol_table[p[1]]
    else:
        print(f"SDT error... Variable '{p[1]}' no declarada.")
        p[0] = 0

def p_factor_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Parsing error...")

parser = yacc.yacc()
