from parte1.lexer import Lexer, Tag
import sys

TAG_NAMES = {
    Tag.ID: "id",
    Tag.NUM: "num",
    Tag.KW_IF: "if",
    Tag.KW_ELSE: "else",
    Tag.KW_DEF: "def",
    Tag.KW_INT: "int",
    Tag.KW_PRINT: "print",
    Tag.KW_RETURN: "return",
    Tag.LE: "<=",
    Tag.GE: ">=",
    Tag.EQ: "==",
    Tag.NE: "!=",
    Tag.EOF: "EOF"
}


class Parser:
    def __init__(self, lexer:Lexer):
        self.lexer = lexer
        self.lookahead = lexer.scan()
        self.table = None
        self.init_table()
        self.stack = None

    def init_table(self):
        self.table = {
            "MAIN": {
                Tag.EOF: [],
                Tag.KW_DEF: ["FLIST"],
                Tag.ID: ["STMT"],
                Tag.KW_INT: ["STMT"],
                Tag.KW_PRINT: ["STMT"],
                Tag.KW_RETURN: ["STMT"],
                Tag.KW_IF: ["STMT"],
                ord('{'): ["STMT"],
                ord(';'): ["STMT"],
            },

            "FLIST": {
                Tag.KW_DEF: ["FDEF", "FLIST_LINHA"]
            },

            "FLIST_LINHA": {
                Tag.KW_DEF: ["FDEF", "FLIST_LINHA"],
                Tag.EOF: []
            },

            "FDEF": {
                Tag.KW_DEF: [Tag.KW_DEF, Tag.ID, ord('('), "PARLIST", ord(')'), ord('{'), "STMTLIST", ord('}')]
            },

            "PARLIST": {
                Tag.KW_INT: [Tag.KW_INT, Tag.ID, "PARLIST_LINHA"],
                ord(')'): []
            },

            "PARLIST_LINHA": {
                ord(','): [ord(','), "PARLIST"],
                ord(')'): []
            },

            "VARLIST": {
                Tag.ID: [Tag.ID, "VARLIST_LINHA"]
            },

            "VARLIST_LINHA": {
                ord(','): [ord(','), "VARLIST"],
                ord(';'): []
            },

            "STMTLIST": {
                Tag.ID: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_INT: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_PRINT: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_RETURN: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_IF: ["STMT", "STMTLIST_LINHA"],
                ord('{'): ["STMT", "STMTLIST_LINHA"],
                ord(';'): ["STMT", "STMTLIST_LINHA"],
            },

            "STMTLIST_LINHA": {
                Tag.ID: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_INT: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_PRINT: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_RETURN: ["STMT", "STMTLIST_LINHA"],
                Tag.KW_IF: ["STMT", "STMTLIST_LINHA"],
                ord('{'): ["STMT", "STMTLIST_LINHA"],
                ord(';'): ["STMT", "STMTLIST_LINHA"],
                ord('}'): []
            },

            "STMT": {
                Tag.KW_INT: [Tag.KW_INT, "VARLIST", ord(';')],
                Tag.ID: ["ATRIBST", ord(';')],
                Tag.KW_PRINT: ["PRINTST", ord(';')],
                Tag.KW_RETURN: ["RETURNST", ord(';')],
                Tag.KW_IF: ["IFSTMT"],
                ord('{'): [ord('{'), "STMTLIST", ord('}')],
                ord(';'): [ord(';')]
            },

            "ATRIBST": {
                Tag.ID: [Tag.ID, ord('='), "ATRIBST_CONTENT"]
            },

            "ATRIBST_CONTENT": {
                Tag.NUM: [Tag.NUM, "TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord('('): [ord('('), "TERM", "NUMEXPR_LINHA", ord(')'), "TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                Tag.ID: [Tag.ID, "ATRIBST_ID"]
            },

            "ATRIBST_ID": {
                ord('('): [ord('('), "PARLISTCALL", ord(')')],
                ord('*'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord('/'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord('+'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord('-'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord(';'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord(')'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"], 
                ord('<'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                ord('>'): ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                Tag.LE: ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                Tag.GE: ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                Tag.EQ: ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
                Tag.NE: ["TERM_LINHA", "NUMEXPR_LINHA", "EXPR_LINHA"],
            },

            "PARLISTCALL": {
                Tag.ID: [Tag.ID, "PARLISTCALL_LINHA"],
                ord(')'): []
            },

            "PARLISTCALL_LINHA": {
                ord(','): [ord(','), "PARLISTCALL"],
                ord(')'): []
            },

            "PRINTST": {
                Tag.KW_PRINT: [Tag.KW_PRINT, "EXPR"]
            },

            "RETURNST": {
                Tag.KW_RETURN: [Tag.KW_RETURN, "RETURNST_LINHA"]
            },

            "RETURNST_LINHA": {
                Tag.ID: [Tag.ID],
                ord(';'): []
            },

            "IFSTMT": {
                Tag.KW_IF: [Tag.KW_IF, ord('('), "EXPR", ord(')'), ord('{'), "STMT", ord('}'), "IFSTMT_LINHA"]
            },

            "IFSTMT_LINHA": {
                Tag.KW_ELSE: [Tag.KW_ELSE, ord('{'), "STMT", ord('}')],
                Tag.ID: [], Tag.KW_INT: [], Tag.KW_PRINT: [], Tag.KW_RETURN: [],
                Tag.KW_IF: [], ord('{'): [], ord(';'): [], ord('}'): [], Tag.EOF: []
            },

            "EXPR": {
                Tag.ID: ["NUMEXPR", "EXPR_LINHA"],
                Tag.NUM: ["NUMEXPR", "EXPR_LINHA"],
                ord('('): ["NUMEXPR", "EXPR_LINHA"]
            },

            "EXPR_LINHA": {
                ord('<'): [ord('<'), "NUMEXPR"],
                ord('>'): [ord('>'), "NUMEXPR"],
                Tag.LE: [Tag.LE, "NUMEXPR"],
                Tag.GE: [Tag.GE, "NUMEXPR"],
                Tag.EQ: [Tag.EQ, "NUMEXPR"],
                Tag.NE: [Tag.NE, "NUMEXPR"],
                ord(';'): [], ord(')'): []
            },

            "NUMEXPR": {
                Tag.ID: ["TERM", "NUMEXPR_LINHA"],
                Tag.NUM: ["TERM", "NUMEXPR_LINHA"],
                ord('('): ["TERM", "NUMEXPR_LINHA"]
            },

            "NUMEXPR_LINHA": {
                ord('+'): [ord('+'), "TERM", "NUMEXPR_LINHA"],
                ord('-'): [ord('-'), "TERM", "NUMEXPR_LINHA"],
                ord(';'): [], ord(')'): [],
                ord('<'): [], ord('>'): [], Tag.LE: [], Tag.GE: [], Tag.EQ: [], Tag.NE: []
            },

            "TERM": {
                Tag.ID: ["FACTOR", "TERM_LINHA"],
                Tag.NUM: ["FACTOR", "TERM_LINHA"],
                ord('('): ["FACTOR", "TERM_LINHA"]
            },

            "TERM_LINHA": {
                ord('*'): [ord('*'), "FACTOR", "TERM_LINHA"],
                ord('/'): [ord('/'), "FACTOR", "TERM_LINHA"],
                ord(';'): [], ord(')'): [], ord('+'): [], ord('-'): [],
                ord('<'): [], ord('>'): [], Tag.LE: [], Tag.GE: [], Tag.EQ: [], Tag.NE: []
            },

            "FACTOR": {
                Tag.ID: [Tag.ID],
                Tag.NUM: [Tag.NUM],
                ord('('): [ord('('), "NUMEXPR", ord(')')]
            }
        }

    def match(self, expected_token):
        if expected_token == self.lookahead.tag:
            self.lookahead = self.lexer.scan()
            return True

        return self.syntax_error(expected_token)

    def parse(self):
        self.stack = []
        self.stack.append(Tag.EOF)
        self.stack.append("MAIN")

        while self.stack:
            top = self.stack.pop()
            if isinstance(top, int):
                self.match(top)
            else:
                try:
                    [self.stack.append(x) for x in self.table[top][self.lookahead.tag][::-1]]
                except KeyError:
                    valid_tags = self.table[top].keys()
                    valid_names = []

                    for tag in valid_tags:
                        if tag < 255:
                            valid_names.append(chr(tag))
                        else:
                            valid_names.append(TAG_NAMES[tag])

                    expected_str = " ou ".join(valid_names)
                    self.syntax_error(expected_str)


    def syntax_error(self, expected):
        line = self.lexer.line
        col = self.lexer.column
        token_found = self.lookahead
        found_str = str(token_found)

        if isinstance(expected, str):
            expected_str = expected
        elif expected < 255:
            expected_str = f"'{chr(expected)}'"
        else:
            expected_str = TAG_NAMES.get(expected, f"Tag {expected}")

        print(f"Erro de Sintaxe na Linha {line}, Coluna {col}:")
        print(f"  Esperado: {expected_str}")
        print(f"  Encontrado: {found_str}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Para usar o programa utilize: `python3 -m parte3.parser [CAMINHO_ARQUIVO]`")
    else:
        l = Lexer(sys.argv[1])
        p = Parser(l)
        p.parse()
        print("Análise Sintática Concluída com Sucesso!")