import ply.yacc as yacc
from lexer import tokens

symbol_table = {}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

#Producciones

def p_statement(p):
    '''statement : declaration
                 | print_statement'''
    pass

def p_declaration(p):
    'declaration : type ID ASSIGN expression SEMICOLON'
    var_type = p[1]
    var_name = p[2]
    value = p[4]

    if var_type == 'int' and isinstance(value, int):
        symbol_table[var_name] = value
        print("Parsing Success!\nSDT Verified!")
    elif var_type == 'float' and isinstance(value, (int, float)):
        symbol_table[var_name] = float(value)
        print("Parsing Success!\nSDT Verified!")
    else:
        print("Parsing Success!\nSDT error... (Type mismatch)")

def p_print_string(p):
    'print_statement : PRINT LPAREN STRING RPAREN SEMICOLON'
    print(f'Output: {p[3]}')
    print("Parsing Success!\nSDT Verified!")

def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]

def p_expression_plus_minus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
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
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        try:
            p[0] = p[1] / p[3]
        except ZeroDivisionError:
            print("SDT error... Division by zero")
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
        print(f"SDT error... Variable '{p[1]}' not declared.")
        p[0] = 0

def p_factor_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Parsing error...")

parser = yacc.yacc()
