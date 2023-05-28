from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from gen.TypstGrammarParser import TypstGrammarParser
from gen.TypstGrammarLexer import TypstGrammarLexer
from gen.TypstGrammarListener import TypstGrammarListener

def typst_parser(typst_expr: str):
    # setup listener
    matherror = MathErrorListener(typst_expr)

    # stream input
    stream = InputStream(typst_expr)
    lex = TypstGrammarLexer(stream)
    lex.id2type['plus'] = 'ADDITIVE_OP'
    lex.removeErrorListeners()
    lex.addErrorListener(matherror)

    tokens = CommonTokenStream(lex)
    parser = TypstGrammarParser(tokens)

    # remove default console error listener
    parser.removeErrorListeners()
    parser.addErrorListener(matherror)

    # process the input
    return_data = None
    math = parser.math()

    return math


class MathErrorListener(ErrorListener):
    def __init__(self, src):
        super(ErrorListener, self).__init__()
        self.src = src

    def syntaxError(self, recog, symbol, line, col, msg, e):
        fmt = "%s\n%s\n%s"
        marker = "~" * col + "^"

        if msg.startswith("missing"):
            err = fmt % (msg, self.src, marker)
        elif msg.startswith("no viable"):
            err = fmt % ("I expected something else here", self.src, marker)
        elif msg.startswith("mismatched"):
            names = TypstGrammarParser.literalNames
            expected = [names[i] for i in e.getExpectedTokens() if i < len(names)]
            if len(expected) < 10:
                expected = " ".join(expected)
                err = (fmt % ("I expected one of these: " + expected,
                              self.src, marker))
            else:
                err = (fmt % ("I expected something else here", self.src, marker))
        else:
            err = fmt % ("I don't understand this", self.src, marker)
        raise Exception(err)
    


def convert_relation(relation):
    return relation


if __name__ == '__main__':
    math = typst_parser("2 plus 3")
    print(math.getText())