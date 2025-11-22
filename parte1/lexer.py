"""
Disciplina: Compiladores - INE5622
Trabalho 1 - Parte 1: Analisador Léxico
Grupo:
    - Gustavo Luiz Kohler
    - Cleverson Borges dos passos
    - Breno Juliano Sayão
"""

import sys


class Tag:
    # Fim de arquivo
    EOF = 255

    # Palavras-chave
    KW_DEF = 256
    KW_INT = 257
    KW_IF = 258
    KW_ELSE = 259
    KW_PRINT = 260
    KW_RETURN = 261

    #Tokens complexosa
    ID = 262
    NUM = 263

    # Operadores de 2 caracteres
    LE = 264  # <=
    GE = 265  # >=
    NE = 266  # !=
    EQ = 267  # ==

    # Erro
    ERROR = 268

class Token:
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return f"<{self.tag}>"

    __repr__ = __str__


class Num(Token):
    def __init__(self, value: int):
        super().__init__(Tag.NUM)
        self.value = value

    def __str__(self):
        return f"<{self.tag}, {self.value}>"

    __repr__ = __str__


class Word(Token):
    def __init__(self, tag: int, lexeme: str):
        super().__init__(tag)
        self.lexeme = lexeme

    def __str__(self):
        return f"<{self.tag}, '{self.lexeme}'>"

    __repr__ = __str__

class Lexer:
    def __init__(self, path):
        try:
            self.content = open(path, 'r').read()
        except FileNotFoundError:
            print(f"Erro: Arquivo {path} não encontrado.")
            sys.exit(1)

        self.index = 0
        self.peek = ' '
        self.line = 1
        self.column = 0

        self.words = {}
        self._reserve(Word(Tag.KW_DEF, "def"))
        self._reserve(Word(Tag.KW_INT, "int"))
        self._reserve(Word(Tag.KW_IF, "if"))
        self._reserve(Word(Tag.KW_ELSE, "else"))
        self._reserve(Word(Tag.KW_PRINT, "print"))
        self._reserve(Word(Tag.KW_RETURN, "return"))

    def _reserve(self, w:Word):
        self.words[w.lexeme] = w

    def readch(self):
        if self.index < len(self.content):
            self.peek = self.content[self.index]
            self.index += 1
            self.column += 1
        else:
            self.peek = ''

    def readch_check(self, char):
        self.readch()
        if self.peek != char:
            return False
        self.peek = ' '
        return True

    def scan(self):
        while self.peek != '':
            if self.peek == ' ' or self.peek == '\t':
                self.readch()
            elif self.peek == '\n':
                self.line += 1
                self.column = 0
                self.readch()
            else:
                break

        match self.peek:
            case '=':
                if self.readch_check('='):
                    return Token(Tag.EQ)
                return Token(ord('='))
            case '!':
                if self.readch_check('='):
                    return Token(Tag.NE)
                print(f"Erro na linha {self.line}, coluna {self.column}: '!' sozinho não esperado.")
                return Token(Tag.ERROR)

            case '<':
                if self.readch_check('='):
                    return Token(Tag.LE)
                return Token(ord('<'))
            case '>':
                if self.readch_check('='):
                    return Token(Tag.GE)
                return Token(ord('>'))
            case '+' | '-' | '*' | '/' | '(' | ')' | '{' | '}' | ',' | ';':
                char = self.peek
                self.peek = ' '
                return Token(ord(char))
            case _ if self.peek.isdigit():
                acm = 0
                while self.peek.isdigit():
                    acm = acm*10 + int(self.peek)
                    self.readch()
                return Num(acm)
            case _ if self.peek.isalpha():
                lex = ''
                while self.peek.isalnum():
                    lex += self.peek
                    self.readch()
                if lex in self.words:
                    return self.words[lex]
                w = Word(Tag.ID, lex)
                self._reserve(w)
                return w
            case '':
                return Token(Tag.EOF)
            case _:
                print(f"Erro na linha {self.line}, coluna {self.column}: caractere {self.peek} desconhecido.")
                self.readch()
                return Token(Tag.ERROR)


    def run(self):
        tokens = []
        while True:
            tkn = self.scan()
            tokens.append(tkn)
            if tkn.tag == Tag.EOF:
                return tokens

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Para usar o programa utilize: `python3 lexer.py [CAMINHO_ARQUIVO]`")
    else:
        l = Lexer(sys.argv[1])
        tkn_list = l.run()

        if not any(t.tag == Tag.ERROR for t in tkn_list):
            print("\nLista de tokens:\n")
            print(tkn_list)
            print("\nTabela de Símbolos:\n")
            print(l.words)
