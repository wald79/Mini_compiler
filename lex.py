from enum import Enum
import sys

class TokenType(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

class Token:

    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind

    def checkIfkeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value <= 200:
                return kind
        return None

class Lexer:

    def __init__(self, source):
        self.source = source + "\n"  # Add a newline to the end of the source
        self.curPos = -1
        self.curChar = ""
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"  # FIXED: Backslash \0 for EOF
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return "\0"  # FIXED: Backslash \0 for EOF
        return self.source[self.curPos + 1]

    def error(self, message):
        sys.exit("Lexing error. " + message)

    def skipWhitespace(self):
        while self.curChar in (" ", "\t", "\r"):
            self.nextChar()

    def skipComment(self):
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()

    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # FIXED: Use elif so execution doesn't fall through to the else block
        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token("", TokenType.EOF)

        elif self.curChar == "=":
            #check this token is == or just =
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == "<":
             #check this token is =< or just <
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)

        elif self.curChar == ">":
            #check this token is >= or just >
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == "!":
            #check this token is != or just !
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.error("Unknown token: " + self.curChar)

        elif self.curChar == '\"':
            #check this token is a string literal
            self.nextChar()
            startPos = self.curPos
            while self.curChar != '\"':
                if self.curChar in ("\n", "\r", "\t", "\\", "%"):
                    self.error("Illegal character in string literal")
                self.nextChar()
            tokenText = self.source[startPos:self.curPos]
            token = Token(tokenText, TokenType.STRING)

        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".":
                self.nextChar()
                if not self.peek().isdigit():
                    self.error("Illegal character in number literal")
                while self.peek().isdigit():
                    self.nextChar()
            tokenText = self.source[startPos:self.curPos + 1]
            token = Token(tokenText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            #Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            # Check if the token is in the list of keywords.
            tokenText = self.source[startPos: self.curPos + 1]
            keyword = Token.checkIfkeyword(tokenText)
            if keyword == None:
                token = Token(tokenText, TokenType.IDENT)
            else:
                token = Token(tokenText, keyword)


        else:
            self.error("Unknown token: " + self.curChar)

        self.nextChar()  # Consume the current character
        return token
    
      
