# Generated from TypstGrammar.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\26")
        buf.write("C\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\7\3\33\n")
        buf.write("\3\f\3\16\3\36\13\3\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\7")
        buf.write("\5(\n\5\f\5\16\5+\13\5\3\6\3\6\3\6\3\6\3\6\3\6\7\6\63")
        buf.write("\n\6\f\6\16\6\66\13\6\3\7\3\7\3\7\6\7;\n\7\r\7\16\7<\5")
        buf.write("\7?\n\7\3\b\3\b\3\b\2\5\4\b\n\t\2\4\6\b\n\f\16\2\2\2@")
        buf.write("\2\20\3\2\2\2\4\24\3\2\2\2\6\37\3\2\2\2\b!\3\2\2\2\n,")
        buf.write("\3\2\2\2\f>\3\2\2\2\16@\3\2\2\2\20\21\7\3\2\2\21\22\5")
        buf.write("\4\3\2\22\23\7\4\2\2\23\3\3\2\2\2\24\25\b\3\1\2\25\26")
        buf.write("\5\6\4\2\26\34\3\2\2\2\27\30\f\4\2\2\30\31\7\26\2\2\31")
        buf.write("\33\5\4\3\5\32\27\3\2\2\2\33\36\3\2\2\2\34\32\3\2\2\2")
        buf.write("\34\35\3\2\2\2\35\5\3\2\2\2\36\34\3\2\2\2\37 \5\b\5\2")
        buf.write(" \7\3\2\2\2!\"\b\5\1\2\"#\5\n\6\2#)\3\2\2\2$%\f\4\2\2")
        buf.write("%&\7\7\2\2&(\5\b\5\5\'$\3\2\2\2(+\3\2\2\2)\'\3\2\2\2)")
        buf.write("*\3\2\2\2*\t\3\2\2\2+)\3\2\2\2,-\b\6\1\2-.\5\f\7\2.\64")
        buf.write("\3\2\2\2/\60\f\4\2\2\60\61\7\b\2\2\61\63\5\n\6\5\62/\3")
        buf.write("\2\2\2\63\66\3\2\2\2\64\62\3\2\2\2\64\65\3\2\2\2\65\13")
        buf.write("\3\2\2\2\66\64\3\2\2\2\678\7\7\2\28?\5\f\7\29;\5\16\b")
        buf.write("\2:9\3\2\2\2;<\3\2\2\2<:\3\2\2\2<=\3\2\2\2=?\3\2\2\2>")
        buf.write("\67\3\2\2\2>:\3\2\2\2?\r\3\2\2\2@A\7\25\2\2A\17\3\2\2")
        buf.write("\2\7\34)\64<>")
        return buf.getvalue()


class TypstGrammarParser ( Parser ):

    grammarFileName = "TypstGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'<typst_math_start>'", "'<typst_math_end>'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'('", "')'", "'{'", "'}'", "'['", "']'", "'\"'", "'_'", 
                     "'^'", "';'", "','", "'!'", "<INVALID>", "'='" ]

    symbolicNames = [ "<INVALID>", "MATH_START", "MATH_END", "WS", "ID", 
                      "ADDITIVE_OP", "MP_OP", "L_PAREN", "R_PAREN", "L_BRACE", 
                      "R_BRACE", "L_BRACKET", "R_BRACKET", "QUOTE", "UNDERSCORE", 
                      "CARET", "SEMICOLON", "COMMA", "BANG", "NUMBER", "RELATION_OP" ]

    RULE_math = 0
    RULE_relation = 1
    RULE_expr = 2
    RULE_additive = 3
    RULE_mp = 4
    RULE_unary = 5
    RULE_postfix = 6

    ruleNames =  [ "math", "relation", "expr", "additive", "mp", "unary", 
                   "postfix" ]

    EOF = Token.EOF
    MATH_START=1
    MATH_END=2
    WS=3
    ID=4
    ADDITIVE_OP=5
    MP_OP=6
    L_PAREN=7
    R_PAREN=8
    L_BRACE=9
    R_BRACE=10
    L_BRACKET=11
    R_BRACKET=12
    QUOTE=13
    UNDERSCORE=14
    CARET=15
    SEMICOLON=16
    COMMA=17
    BANG=18
    NUMBER=19
    RELATION_OP=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class MathContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MATH_START(self):
            return self.getToken(TypstGrammarParser.MATH_START, 0)

        def relation(self):
            return self.getTypedRuleContext(TypstGrammarParser.RelationContext,0)


        def MATH_END(self):
            return self.getToken(TypstGrammarParser.MATH_END, 0)

        def getRuleIndex(self):
            return TypstGrammarParser.RULE_math

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMath" ):
                listener.enterMath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMath" ):
                listener.exitMath(self)




    def math(self):

        localctx = TypstGrammarParser.MathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_math)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.match(TypstGrammarParser.MATH_START)
            self.state = 15
            self.relation(0)
            self.state = 16
            self.match(TypstGrammarParser.MATH_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(TypstGrammarParser.ExprContext,0)


        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TypstGrammarParser.RelationContext)
            else:
                return self.getTypedRuleContext(TypstGrammarParser.RelationContext,i)


        def RELATION_OP(self):
            return self.getToken(TypstGrammarParser.RELATION_OP, 0)

        def getRuleIndex(self):
            return TypstGrammarParser.RULE_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation" ):
                listener.enterRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation" ):
                listener.exitRelation(self)



    def relation(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TypstGrammarParser.RelationContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_relation, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.expr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 26
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = TypstGrammarParser.RelationContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_relation)
                    self.state = 21
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 22
                    self.match(TypstGrammarParser.RELATION_OP)
                    self.state = 23
                    self.relation(3) 
                self.state = 28
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additive(self):
            return self.getTypedRuleContext(TypstGrammarParser.AdditiveContext,0)


        def getRuleIndex(self):
            return TypstGrammarParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)




    def expr(self):

        localctx = TypstGrammarParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.additive(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mp(self):
            return self.getTypedRuleContext(TypstGrammarParser.MpContext,0)


        def additive(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TypstGrammarParser.AdditiveContext)
            else:
                return self.getTypedRuleContext(TypstGrammarParser.AdditiveContext,i)


        def ADDITIVE_OP(self):
            return self.getToken(TypstGrammarParser.ADDITIVE_OP, 0)

        def getRuleIndex(self):
            return TypstGrammarParser.RULE_additive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditive" ):
                listener.enterAdditive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditive" ):
                listener.exitAdditive(self)



    def additive(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TypstGrammarParser.AdditiveContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_additive, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.mp(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 39
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = TypstGrammarParser.AdditiveContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_additive)
                    self.state = 34
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 35
                    self.match(TypstGrammarParser.ADDITIVE_OP)
                    self.state = 36
                    self.additive(3) 
                self.state = 41
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class MpContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unary(self):
            return self.getTypedRuleContext(TypstGrammarParser.UnaryContext,0)


        def mp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TypstGrammarParser.MpContext)
            else:
                return self.getTypedRuleContext(TypstGrammarParser.MpContext,i)


        def MP_OP(self):
            return self.getToken(TypstGrammarParser.MP_OP, 0)

        def getRuleIndex(self):
            return TypstGrammarParser.RULE_mp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMp" ):
                listener.enterMp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMp" ):
                listener.exitMp(self)



    def mp(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TypstGrammarParser.MpContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_mp, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.unary()
            self._ctx.stop = self._input.LT(-1)
            self.state = 50
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = TypstGrammarParser.MpContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_mp)
                    self.state = 45
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 46
                    self.match(TypstGrammarParser.MP_OP)
                    self.state = 47
                    self.mp(3) 
                self.state = 52
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class UnaryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADDITIVE_OP(self):
            return self.getToken(TypstGrammarParser.ADDITIVE_OP, 0)

        def unary(self):
            return self.getTypedRuleContext(TypstGrammarParser.UnaryContext,0)


        def postfix(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TypstGrammarParser.PostfixContext)
            else:
                return self.getTypedRuleContext(TypstGrammarParser.PostfixContext,i)


        def getRuleIndex(self):
            return TypstGrammarParser.RULE_unary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnary" ):
                listener.enterUnary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnary" ):
                listener.exitUnary(self)




    def unary(self):

        localctx = TypstGrammarParser.UnaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_unary)
        try:
            self.state = 60
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [TypstGrammarParser.ADDITIVE_OP]:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.match(TypstGrammarParser.ADDITIVE_OP)
                self.state = 54
                self.unary()
                pass
            elif token in [TypstGrammarParser.NUMBER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 56 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 55
                        self.postfix()

                    else:
                        raise NoViableAltException(self)
                    self.state = 58 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(TypstGrammarParser.NUMBER, 0)

        def getRuleIndex(self):
            return TypstGrammarParser.RULE_postfix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfix" ):
                listener.enterPostfix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfix" ):
                listener.exitPostfix(self)




    def postfix(self):

        localctx = TypstGrammarParser.PostfixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_postfix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(TypstGrammarParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.relation_sempred
        self._predicates[3] = self.additive_sempred
        self._predicates[4] = self.mp_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def relation_sempred(self, localctx:RelationContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

    def additive_sempred(self, localctx:AdditiveContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def mp_sempred(self, localctx:MpContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         




