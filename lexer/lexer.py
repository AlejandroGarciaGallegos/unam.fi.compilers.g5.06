from tok import Tok, TokenType, isKeyword

class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0        # current position in input
        self.read_position = 0   # current reading position in input
        self.ch = ''             # current char under examination
        self.readChar()
        self.total = 0

    def isEOF(self):
        return self.ch != ''

    def printTotal(self):
        print(f'\nTotal number of tokens: {self.total}')

    def readChar(self):
        if self.read_position >= len(self.input):
            self.ch = ''
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def readToken(self):
        tk = {}
        self.skipWhitespace()

        match self.ch:
            case '=':
                tk = Tok(TokenType.OPERATOR, self.ch)
                self.readChar()
                self.total += 1
                if self.ch=="=":
                    tk.literal="=="
                    self.readChar()
                    self.total += 1
                return tk
            case '+':
                tk = Tok(TokenType.OPERATOR, self.ch)
            case '-':
                tk = Tok(TokenType.OPERATOR, self.ch)
            case '/':
                tk = Tok(TokenType.OPERATOR, self.ch)
            case '*':
                tk = Tok(TokenType.OPERATOR, self.ch)
            case ';':
                tk = Tok(TokenType.PUNCTUATION, self.ch)
            case '(':
                tk = Tok(TokenType.PUNCTUATION, self.ch)
            case ')':
                tk = Tok(TokenType.PUNCTUATION, self.ch)
            case ',':
                tk = Tok(TokenType.PUNCTUATION, self.ch)
            case '{':
                tk = Tok(TokenType.PUNCTUATION, self.ch)
            case '}':
                tk = Tok(TokenType.PUNCTUATION, self.ch)
            case '"':
                tk = self.readString()
                self.total += 1
                return tk
            case '':
                tk = Tok(TokenType.EOF, '')
                return tk
            case _:
                if isIdentifierLetter(self.ch):
                    literal = self.readIdentifier()
                    type = isKeyword(literal)
                    tk = Tok(type, literal)
                    self.total += 1
                    return tk
                elif isDigit(self.ch):
                    tk = self.readNumber()
                    self.total += 1
                    return tk
                else:
                    tk = Tok(TokenType.INVALID, self.ch)

        self.readChar()
        self.total += 1
        return tk

    def readIdentifier(self):
        start = self.position
        while isIdentifierLetter(self.ch) or '0' <= self.ch and self.ch <= '9':
            self.readChar();

        return self.input[start:self.position]

    def readNumber(self):
        start = self.position
        while isDigit(self.ch):
            self.readChar();

        return Tok(TokenType.CONSTANT, self.input[start:self.position])

    def readString(self):
        start = self.position
        self.readChar()
        while self.ch != '"' and self.ch != '':
            self.readChar()
            if (self.ch == ''):
                return Tok(TokenType.INVALID, self.input[start:self.position])
        self.readChar()
        return Tok(TokenType.LITERAL, self.input[start:self.position])

    def skipWhitespace(self):
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.readChar()

def isIdentifierLetter(ch):
    return ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z') or ch == '_'

def isDigit(ch):
    return '0' <= ch and ch <= '9'
