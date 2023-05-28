from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from gen.TypstGrammarParser import TypstGrammarParser
from gen.TypstGrammarLexer import TypstGrammarLexer
from gen.TypstGrammarListener import TypstGrammarListener

class TypstMathParser:

    MATH_START = '<typst_math_start>'
    MATH_END = '<typst_math_end>'

    id2type = {}

    def __init__(self):
        # setup listener
        self.matherror = MathErrorListener()
        # setup lexer
        self.init_lex()

    def init_lex(self):
        self.id2type['plus'] = 'ADDITIVE_OP'

    def parse(self, typst_math):
        # set the input and matherror
        self.matherror.reset(typst_math, len(self.MATH_START))
        src = self.MATH_START + typst_math + self.MATH_END

        # stream input
        stream = InputStream(src)
        lex = TypstGrammarLexer(stream)
        lex.id2type = self.id2type
        lex.removeErrorListeners()
        lex.addErrorListener(self.matherror)

        tokens = CommonTokenStream(lex)
        parser = TypstGrammarParser(tokens)

        # remove default console error listener
        parser.removeErrorListeners()
        parser.addErrorListener(self.matherror)
        # process the input
        math = parser.math()

        return math


class MathErrorListener(ErrorListener):
    def __init__(self):
        super(ErrorListener, self).__init__()
        self.cur = 0
        self.src = ''

    def reset(self, src, cur):
        self.cur = cur
        self.src = src

    def syntaxError(self, recog, symbol, line, col, msg, e):
        fmt = "%s\n%s\n%s"
        marker = "~" * (col - self.cur) + "^"

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



if __name__ == '__main__':
    typst_parser = TypstMathParser()
    math = typst_parser.parse("2 plus 3")
    print(math.getText())
    math = typst_parser.parse("1 plus 2")
    print(math.getText())