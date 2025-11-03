class Tok:
    def __init__(self, tokenType: str, literal: str):
        self.tokenType = tokenType
        self.literal = literal
    def __str__(self):
        return f"{self.tokenType}: {self.literal}"

class TokenType:
    KEYWORD = "KEYWORD"
    PUNCTUATION = "PUNCTUATION"
    IDENTIFIER = "IDENTIFIER"
    OPERATOR = "OPERATOR"
    CONSTANT = "CONSTANT"
    EOF = "EOF"
    INVALID = "INVALID"
    LITERAL = "LITERAL"

keywords = [
    "print",
    "int"
]

def isKeyword(identifier):
    if identifier in keywords:
        return TokenType.KEYWORD
    return TokenType.IDENTIFIER
