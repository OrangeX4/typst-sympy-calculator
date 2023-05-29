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


    # Enter a parse tree produced by TypstGrammarParser#subargs.
    def enterSubargs(self, ctx:TypstGrammarParser.SubargsContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#subargs.
    def exitSubargs(self, ctx:TypstGrammarParser.SubargsContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#subexpr.
    def enterSubexpr(self, ctx:TypstGrammarParser.SubexprContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#subexpr.
    def exitSubexpr(self, ctx:TypstGrammarParser.SubexprContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#supexpr.
    def enterSupexpr(self, ctx:TypstGrammarParser.SupexprContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#supexpr.
    def exitSupexpr(self, ctx:TypstGrammarParser.SupexprContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#subsupexpr.
    def enterSubsupexpr(self, ctx:TypstGrammarParser.SubsupexprContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#subsupexpr.
    def exitSubsupexpr(self, ctx:TypstGrammarParser.SubsupexprContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#subassign.
    def enterSubassign(self, ctx:TypstGrammarParser.SubassignContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#subassign.
    def exitSubassign(self, ctx:TypstGrammarParser.SubassignContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#supassign.
    def enterSupassign(self, ctx:TypstGrammarParser.SupassignContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#supassign.
    def exitSupassign(self, ctx:TypstGrammarParser.SupassignContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#subsupassign.
    def enterSubsupassign(self, ctx:TypstGrammarParser.SubsupassignContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#subsupassign.
    def exitSubsupassign(self, ctx:TypstGrammarParser.SubsupassignContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#eval_at.
    def enterEval_at(self, ctx:TypstGrammarParser.Eval_atContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#eval_at.
    def exitEval_at(self, ctx:TypstGrammarParser.Eval_atContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#transpose.
    def enterTranspose(self, ctx:TypstGrammarParser.TransposeContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#transpose.
    def exitTranspose(self, ctx:TypstGrammarParser.TransposeContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#postfix_op.
    def enterPostfix_op(self, ctx:TypstGrammarParser.Postfix_opContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#postfix_op.
    def exitPostfix_op(self, ctx:TypstGrammarParser.Postfix_opContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#postfix.
    def enterPostfix(self, ctx:TypstGrammarParser.PostfixContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#postfix.
    def exitPostfix(self, ctx:TypstGrammarParser.PostfixContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#exp.
    def enterExp(self, ctx:TypstGrammarParser.ExpContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#exp.
    def exitExp(self, ctx:TypstGrammarParser.ExpContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#comp.
    def enterComp(self, ctx:TypstGrammarParser.CompContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#comp.
    def exitComp(self, ctx:TypstGrammarParser.CompContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#group.
    def enterGroup(self, ctx:TypstGrammarParser.GroupContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#group.
    def exitGroup(self, ctx:TypstGrammarParser.GroupContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#abs_group.
    def enterAbs_group(self, ctx:TypstGrammarParser.Abs_groupContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#abs_group.
    def exitAbs_group(self, ctx:TypstGrammarParser.Abs_groupContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#args.
    def enterArgs(self, ctx:TypstGrammarParser.ArgsContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#args.
    def exitArgs(self, ctx:TypstGrammarParser.ArgsContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#mat_args.
    def enterMat_args(self, ctx:TypstGrammarParser.Mat_argsContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#mat_args.
    def exitMat_args(self, ctx:TypstGrammarParser.Mat_argsContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#func.
    def enterFunc(self, ctx:TypstGrammarParser.FuncContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#func.
    def exitFunc(self, ctx:TypstGrammarParser.FuncContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#matrix.
    def enterMatrix(self, ctx:TypstGrammarParser.MatrixContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#matrix.
    def exitMatrix(self, ctx:TypstGrammarParser.MatrixContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#reduceit.
    def enterReduceit(self, ctx:TypstGrammarParser.ReduceitContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#reduceit.
    def exitReduceit(self, ctx:TypstGrammarParser.ReduceitContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#lim.
    def enterLim(self, ctx:TypstGrammarParser.LimContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#lim.
    def exitLim(self, ctx:TypstGrammarParser.LimContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#log.
    def enterLog(self, ctx:TypstGrammarParser.LogContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#log.
    def exitLog(self, ctx:TypstGrammarParser.LogContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#integral.
    def enterIntegral(self, ctx:TypstGrammarParser.IntegralContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#integral.
    def exitIntegral(self, ctx:TypstGrammarParser.IntegralContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#text.
    def enterText(self, ctx:TypstGrammarParser.TextContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#text.
    def exitText(self, ctx:TypstGrammarParser.TextContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#accent.
    def enterAccent(self, ctx:TypstGrammarParser.AccentContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#accent.
    def exitAccent(self, ctx:TypstGrammarParser.AccentContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#symbol_base.
    def enterSymbol_base(self, ctx:TypstGrammarParser.Symbol_baseContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#symbol_base.
    def exitSymbol_base(self, ctx:TypstGrammarParser.Symbol_baseContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#symbol.
    def enterSymbol(self, ctx:TypstGrammarParser.SymbolContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#symbol.
    def exitSymbol(self, ctx:TypstGrammarParser.SymbolContext):
        pass


    # Enter a parse tree produced by TypstGrammarParser#atom.
    def enterAtom(self, ctx:TypstGrammarParser.AtomContext):
        pass

    # Exit a parse tree produced by TypstGrammarParser#atom.
    def exitAtom(self, ctx:TypstGrammarParser.AtomContext):
        pass


