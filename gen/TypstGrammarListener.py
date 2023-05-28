# Generated from TypstGrammar.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TypstGrammarParser import TypstGrammarParser
else:
    from TypstGrammarParser import TypstGrammarParser

# This class defines a complete listener for a parse tree produced by TypstGrammarParser.
class TypstGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by TypstGrammarParser#math.
    def enterMath(self, ctx:TypstGrammarParser.MathContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#math.
    def exitMath(self, ctx:TypstGrammarParser.MathContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#relation.
    def enterRelation(self, ctx:TypstGrammarParser.RelationContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#relation.
    def exitRelation(self, ctx:TypstGrammarParser.RelationContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#expr.
    def enterExpr(self, ctx:TypstGrammarParser.ExprContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#expr.
    def exitExpr(self, ctx:TypstGrammarParser.ExprContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#additive.
    def enterAdditive(self, ctx:TypstGrammarParser.AdditiveContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#additive.
    def exitAdditive(self, ctx:TypstGrammarParser.AdditiveContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#mp.
    def enterMp(self, ctx:TypstGrammarParser.MpContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#mp.
    def exitMp(self, ctx:TypstGrammarParser.MpContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#unary.
    def enterUnary(self, ctx:TypstGrammarParser.UnaryContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#unary.
    def exitUnary(self, ctx:TypstGrammarParser.UnaryContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#postfix.
    def enterPostfix(self, ctx:TypstGrammarParser.PostfixContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#postfix.
    def exitPostfix(self, ctx:TypstGrammarParser.PostfixContext):
        pass


