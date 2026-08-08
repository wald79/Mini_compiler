import sys
from typing import NoReturn
from lex import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set() #variables declared till now
        self.labelsDeclared = set() #lables declared so far
        self.labelsGotoed = set() # labels goto'ed so far

        self.currentToken = None
        self.peekToken = None

        self.nextToken()  # Current token is the first token
        self.nextToken()  # Peek token is the second token

    # nl ::= '\n'+
    def nl(self):
        
        if self.checkToken(TokenType.EOF):
            return 
        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

    # Return true if the current token matches.
    def checkToken(self, kind):
        return self.currentToken.kind == kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return self.peekToken.kind == kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.currentToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.currentToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")
        
        # Since some newlines are required in our grammar, need to skip the excess.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()
            while self.checkToken(TokenType.NEWLINE):
                self.nextToken()
            
        # Wrap things up.
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
    
        # Check that each label referenced in a GOTO is declared.
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

        
    def comparison(self):
        print("COMPARISON")
        self.expression()

        #Must be atleast 1 comparison operator and another expression
        if self.isComparisonOperator():
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)
        while self.isComparisonOperator():
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.expression()
       
    def isComparisonOperator(self):
        comparison_operators = [TokenType.GT,TokenType.GTEQ, TokenType.LT, TokenType.LTEQ,TokenType.EQEQ, TokenType.NOTEQ,] 
        return self.currentToken.kind in comparison_operators

    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.term()

     # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")
        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()        
        self.primary()

    def primary(self):
        print(f"Primary + {self.currentToken.text}")
        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            #Check if the variable already exist 
            if self.currentToken.text not in self.symbols:
                self.abort("Rerferencing variable before assignment "+self.currentToken.text)
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
        else:
            #error
            self.abort(f"Unexpected token at: {self.currentToken.text}")

    def statement(self):
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()
            if self.checkToken(TokenType.STRING):
                # simple string, so then we print it
                self.emitter.emitLine("printf(\"" + self.currentToken.text + "\\n\");")
                self.nextToken()
            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")
    

        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine("){")

            #If there are zero statements
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")

        #while statement
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine("){")

            #Zero or more statements in the loop
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")

        #label indentification
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()

            # Make sure this label doesn't already exist.
            if self.currentToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.currentToken.text)
            self.labelsDeclared.add(self.currentToken.text)

            self.emitter.emitLine(self.currentToken.text +":")
            self.match(TokenType.IDENT)

        #goto identififcation
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.labelsGotoed.add(self.currentToken.text)
            self.emitter.emitLine("goto" + self.currentToken.text + ";")
            self.match(TokenType.IDENT)

        # "LET" ident = "EXPRESSION"
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            #  Check if ident exists in symbol table. If not, declare it.
            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)
                self.emitter.headerLine("float " + self.currentToken.text + ";")

            self.emitter.emit(self.currentToken.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emitLine(";")

        #"INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()

            #if variable already does not exist, declare it
            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)
                self.emitter.headerLine("float " + self.currentToken.text + ";")

            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.currentToken.text + ")) {")
            self.emitter.emitLine(self.currentToken.text + " =0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")
            self.match(TokenType.IDENT)
        

        #This aint a valid statement
        else:
            self.abort("Invalid statement at " + self.currentToken.text + " (" + self.currentToken.kind.name + ")")

        self.nl()    


        