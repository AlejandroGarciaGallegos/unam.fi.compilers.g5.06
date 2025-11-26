from __future__ import annotations

import ply.lex as lex

# Palabras reservadas
reserved = {
    "int": "INT",
    "float": "FLOAT",
    "print": "PRINT",
}

tokens = [
    "ID",
    "NUMBER",
    "DECIMAL",
    "STRING",
    "ASSIGN",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "SEMICOLON",
] + list(reserved.values())

# Tokens simples
t_ASSIGN   = r'='
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_SEMICOLON = r';'

t_ignore = ' \t'


def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    # Quitamos comillas y procesamos escapes básicos
    raw = t.value[1:-1]
    t.value = bytes(raw, "utf-8").decode("unicode_escape")
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, "ID")
    return t


def t_comment(t):
    r'//[^\n]*'
    # Comentarios de una línea tipo C/C++: se ignoran
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character {t.value[0]!r} at line {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()
