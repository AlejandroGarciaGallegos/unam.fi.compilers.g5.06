from __future__ import annotations

from typing import List

import ply.yacc as yacc

from ast_nodes import (
    BasicType,
    CompileError,
    Program,
    VarDecl,
    Assign,
    Print,
    Literal,
    Var,
    BinOp,
    UnaryOp,
)
from lexer import tokens, lexer

# Precedencia de operadores
precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "UMINUS"),
)


def _token_value_to_basic_type(token_value: str) -> BasicType:
    if token_value == "int":
        return BasicType.INT
    elif token_value == "float":
        return BasicType.FLOAT
    raise ValueError(f"Unknown type keyword {token_value!r}")


def p_program(p):
    "program : stmt_list"
    line = p[1][0].line if p[1] else 1
    p[0] = Program(line=line, statements=p[1])


def p_stmt_list_single(p):
    "stmt_list : statement"
    if p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]


def p_stmt_list_multi(p):
    "stmt_list : stmt_list statement"
    if p[2] is not None:
        p[1].append(p[2])
    p[0] = p[1]


def p_statement_var_decl(p):
    "statement : type ID ASSIGN expr SEMICOLON"
    var_type = _token_value_to_basic_type(p[1])
    name = p[2]
    line = p.lineno(2)
    p[0] = VarDecl(line=line, name=name, var_type=var_type, expr=p[4])


def p_statement_assignment(p):
    "statement : ID ASSIGN expr SEMICOLON"
    name = p[1]
    line = p.lineno(1)
    p[0] = Assign(line=line, name=name, expr=p[3])


def p_statement_print_expr(p):
    "statement : PRINT LPAREN expr RPAREN SEMICOLON"
    line = p.lineno(1)
    p[0] = Print(line=line, expr=p[3])


def p_statement_print_string(p):
    "statement : PRINT LPAREN STRING RPAREN SEMICOLON"
    line = p.lineno(1)
    string_value = p[3]
    lit = Literal(line=line, value=string_value, lit_type=BasicType.STRING)
    p[0] = Print(line=line, expr=lit)


def p_statement_empty(p):
    "statement : SEMICOLON"
    p[0] = None


def p_type_int(p):
    "type : INT"
    p[0] = p[1]


def p_type_float(p):
    "type : FLOAT"
    p[0] = p[1]


def p_expr_binop(p):
    """expr : expr PLUS term
            | expr MINUS term"""
    op = p[2]
    line = p.lineno(2)
    p[0] = BinOp(line=line, op=op, left=p[1], right=p[3])


def p_expr_term(p):
    "expr : term"
    p[0] = p[1]


def p_term_binop(p):
    """term : term TIMES factor
            | term DIVIDE factor"""
    op = p[2]
    line = p.lineno(2)
    p[0] = BinOp(line=line, op=op, left=p[1], right=p[3])


def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


def p_factor_number(p):
    """factor : NUMBER
              | DECIMAL"""
    token_type = p.slice[1].type
    line = p.lineno(1)
    if token_type == "NUMBER":
        lit_type = BasicType.INT
    else:
        lit_type = BasicType.FLOAT
    p[0] = Literal(line=line, value=p[1], lit_type=lit_type)


def p_factor_id(p):
    "factor : ID"
    name = p[1]
    line = p.lineno(1)
    p[0] = Var(line=line, name=name)


def p_factor_group(p):
    "factor : LPAREN expr RPAREN"
    p[0] = p[2]


def p_factor_uminus(p):
    "factor : MINUS factor %prec UMINUS"
    line = p.lineno(1)
    p[0] = UnaryOp(line=line, op='-', operand=p[2])


def p_error(p):
    if p is None:
        line = lexer.lineno or 1
        raise CompileError(line=line-1, message="syntax error (missing ';')")
    else:
        # Si aparece un token que puede iniciar una nueva sentencia donde
        # el parser esperaba un ';'
        if p.type in ("INT", "FLOAT", "PRINT", "ID"):
            raise CompileError(line=p.lineno-1, message="syntax error (missing ';')")
        raise CompileError(
            line=p.lineno,
            message=f"syntax error at token {p.type!r} with value {p.value!r}",
        )


parser = yacc.yacc(start="program")


def parse_source(text: str) -> Program:
    return parser.parse(text, lexer=lexer, tracking=True)
