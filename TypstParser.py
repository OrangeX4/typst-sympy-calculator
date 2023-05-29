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
        self.id2type['sum'] = 'REDUCE_OP'
        self.id2type['sin'] = 'FUNC'

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
    math = typst_parser.parse("sin(1 + 2) / 2")
    assert math.relation().expr().additive().mp().mp()[0].unary().postfix()[0].exp().comp().func().args().relation()[0].getText() == '1+2'
    math = typst_parser.parse("sin(2 + 3)")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().func().args().relation()[0].getText() == '2+3'
    math = typst_parser.parse("sin(2 + 3,)")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().func().args().relation()[0].getText() == '2+3'
    math = typst_parser.parse("mat(1,2;3,4)")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().matrix().mat_args().args()[0].getText() == '1,2'
    math = typst_parser.parse("integral_1^2 x^2 dif x")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().integral().additive().getText() == 'x^2'
    math = typst_parser.parse("integral_1^2 integral_1^2 x y dif y dif x")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().integral().additive().getText() == 'integral_1^2xydify'
    math = typst_parser.parse("2^2^3")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().getText() == '2'
    math = typst_parser.parse("x_2^3")
    assert math.relation().expr().additive().mp().unary().postfix()[0].exp().comp().getText() == 'x_2'
    math = typst_parser.parse("sum_(k=1)^2 k^2 + 1")
    assert math.relation().expr().additive().additive()[0].mp().unary().postfix()[0].exp().comp().reduceit().mp().getText() == 'k^2'
