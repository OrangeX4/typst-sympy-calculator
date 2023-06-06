import sympy
from sympy.printing.str import StrPrinter
from TypstParser import TypstMathParser
from functools import wraps, reduce
from typing import Callable


class TypstMathPrinter(StrPrinter):

    def paren(self, expr):
        return '(' + self.doprint(expr) + ')' if expr.is_Add else self.doprint(expr)

    def _print_list(self, lst):
        lst = list(set([self.doprint(item) for item in lst]))
        # lst = [self.doprint(item) for item in lst]
        return ', '.join(lst)

    def _print_tuple(self, tup):
        return ', '.join([self.doprint(item) for item in tup])
    
    def _print_dict(self, dic):
        if len(dic) == 0:
            return 'nothing'
        elif len(dic) == 1:
            k, v = dic.popitem()
            return self.doprint(k) + ' = ' + self.doprint(v)
        else:
            return 'cases(' + ', '.join([self.doprint(k) + ' = ' + self.doprint(v) for k, v in dic.items()]) + ')'

    def _print_Mul(self, expr):
        def mul(x, y):
            if x == '1':
                return y
            if x == '-1':
                return '-' + y
            return x + ' ' + y
        return reduce(mul, map(self.paren, expr.args))
    
    # matrix form: mat(1, 2; 3, 4)
    def _print_MatrixBase(self, expr):
        n, m, mat_flattern = expr.args
        res = 'mat('
        rows = [mat_flattern[i:i+m] for i in range(0, n*m, m)]
        res += '; '.join(map(lambda row: ', '.join(map(self.doprint, row)), rows))
        res += ')'
        return res

    def _print_Limit(self, expr):
        e, z = expr.args
        return "lim_(%s -> %s) %s" % (self._print(z), self._print(z), self._print(e))

    def _print_Integral(self, expr):
        e, lims = expr.args
        if len(lims) > 1:
            return "integral_%s^%s %s dif %s" % (self.paren(lims[1]), self.paren(lims[2]), self._print(e), self._print(lims[0]))
        else:
            return "integral %s dif %s" % (self._print(e), self._print(lims))
    
    def _print_Sum(self, expr):
        e, lims = expr.args
        return "sum_(%s = %s)^%s %s" % (self._print(lims[0]), self._print(lims[1]), self.paren(lims[2]), self._print(e))

    def _print_Product(self, expr):
        e, lims = expr.args
        return "product_(%s = %s)^%s %s" % (self._print(lims[0]), self._print(lims[1]), self.paren(lims[2]), self._print(e))

    def _print_factorial(self, expr):
        return "%s!" % self._print(expr.args[0])

    def _print_Derivative(self, expr):
        e = expr.args[0]
        wrt = expr.args[1]
        return "dif / (dif %s) (%s)" % (self._print(wrt), self._print(e))
    
    def _print_Abs(self, expr):
        return "|%s|" % self._print(expr.args[0])

    def _print_Equality(self, expr):
        return "%s = %s" % (self._print(expr.args[0]), self._print(expr.args[1]))

    # using ^ but not ** for power
    def _print_Pow(self, expr):
        b, e = expr.args
        base = self.doprint(b) if b.is_Atom else '(' + self.doprint(b) + ')'
        if e is sympy.S.Half:
            return "sqrt(%s)" % self.doprint(b)
        if -e is sympy.S.Half:
            return "1 / sqrt(%s)" % self.doprint(b)
        if e is -sympy.S.One:
            return "1 / %s" % base
        if e.is_Atom or e.is_Pow:
            return base + '^' + self.doprint(e)
        else:
            return base + '^' + '(' + self.doprint(e) + ')'
    
    def _print_And(self, expr):
        return ' and '.join([self.doprint(item) for item in expr.args])

    def _print_Or(self, expr):
        return ' or '.join([self.doprint(item) for item in expr.args])

    def _print_Not(self, expr):
        return 'not ' + self.doprint(expr.args[0])


class TypstMathConverter(object):

    id2type = {}
    id2func = {}

    def __init__(self) -> None:
        self.parser = TypstMathParser()
        self.printer = TypstMathPrinter()

    def define(self, name: str, type: str, func: Callable = None):
        if name.startswith('#'):
            name = name[1:]
        self.id2type[name.split('_')[0]] = type
        if isinstance(func, Callable):
            self.id2func[name] = func
        name = '#' + name
        self.id2type[name.split('_')[0]] = type
        if isinstance(func, Callable):
            self.id2func[name] = func

    def undefine(self, name: str):
        if name.startswith('#'):
            name = name[1:]
        if name in self.id2type:
            del self.id2type[name]
        if name in self.id2func:
            del self.id2func[name]
        name = '#' + name
        if name in self.id2type:
            del self.id2type[name]
        if name in self.id2func:
            del self.id2func[name]

    def define_accent(self, accent_name: str):
        self.define(accent_name, 'ACCENT_OP')

    def define_symbol_base(self, symbol_base_name: str):
        self.define(symbol_base_name, 'SYMBOL_BASE')

    def define_function(self, function_name: str):
        self.define(function_name, 'FUNC')

    def parse(self, typst_math: str):
        self.parser.id2type = self.id2type
        return self.parser.parse(typst_math)

    def sympy(self, typst_math: str):
        math = self.parse(typst_math)
        return self.convert_math(math)

    def typst(self, sympy_expr) -> str:
        return self.printer.doprint(sympy_expr)

    def convert_math(self, math):
        return self.convert_relation(math.relation())

    def convert_relation(self, relation):
        relation_op = relation.RELATION_OP()
        if relation_op:
            relations = relation.relation()
            assert len(relations) == 2
            op = relation_op.getText()

            def rel(i):
                return self.convert_relation(relations[i])
            if op == '=':
                return sympy.Eq(rel(0), rel(1))
            elif op == '==':
                return sympy.Eq(rel(0), rel(1))
            elif op == '!=':
                return sympy.Ne(rel(0), rel(1))
            elif op == '<':
                return sympy.Lt(rel(0), rel(1))
            elif op == '>':
                return sympy.Gt(rel(0), rel(1))
            elif op == '<=':
                return sympy.Le(rel(0), rel(1))
            elif op == '>=':
                return sympy.Ge(rel(0), rel(1))
            elif op in self.id2type and self.id2type[op] == 'RELATION_OP':
                assert op in self.id2func, f'function for {op} not found'
                return self.id2func[op](relation)
            else:
                raise Exception(f'unknown relation operator {op}')
        else:
            expr = relation.expr()
            assert expr
            return self.convert_expr(expr)

    def convert_expr(self, expr):
        return self.convert_additive(expr.additive())

    def convert_additive(self, additive):
        additive_op = additive.ADDITIVE_OP()
        if additive_op:
            additives = additive.additive()
            assert len(additives) == 2
            op = additive_op.getText()

            def additive_at(i):
                return self.convert_additive(additives[i])
            if op == '+':
                return additive_at(0) + additive_at(1)
            elif op == '-':
                return additive_at(0) - additive_at(1)
            elif op in self.id2type and self.id2type[op] == 'ADDITIVE_OP':
                assert op in self.id2func, f'function for {op} not found'
                return self.id2func[op](additive)
            else:
                raise Exception(f'unknown additive operator {op}')
        else:
            return self.convert_mp(additive.mp())

    def convert_mp(self, mp):
        mp_op = mp.MP_OP()
        if mp_op:
            mps = mp.mp()
            assert len(mps) == 2
            op = mp_op.getText()

            def mp_at(i):
                return self.convert_mp(mps[i])
            if op == '*':
                return mp_at(0) * mp_at(1)
            elif op == '/':
                return mp_at(0) / mp_at(1)
            elif op == '\\/':
                return mp_at(0) / mp_at(1)
            elif op in self.id2type and self.id2type[op] == 'MP_OP':
                assert op in self.id2func, f'function for {op} not found'
                return self.id2func[op](mp)
            else:
                raise Exception(f'unknown mp operator {op}')
        else:
            return self.convert_unary(mp.unary())

    def convert_unary(self, unary):
        additive_op = unary.ADDITIVE_OP()
        if additive_op:
            unary = unary.unary()
            assert unary
            op = additive_op.getText()
            if op == '+':
                return self.convert_unary(unary)
            elif op == '-':
                return -self.convert_unary(unary)
            else:
                raise Exception(f'unsupport unary operator {op}')
        else:
            postfixes = [self.convert_postfix(pos) for pos in unary.postfix()]
            assert len(postfixes) >= 1
            if len(postfixes) == 1:
                return postfixes[0]
            else:
                return reduce(lambda x, y: x * y, postfixes)
    
    def convert_eval_at(self, expr, eval_at):
        # eval_at: EVAL_BAR subsupassign;
        symbol, sub, sup = self.convert_subsupassign(eval_at.subsupassign())
        if symbol is None:
            symbol = expr.free_symbols.pop()
        assert sub or sup
        if sub is None or sup is None:
            val = sub or sup
            return expr.subs(symbol, val)
        else:
            return expr.subs(symbol, sup) - expr.subs(symbol, sub)

    def convert_postfix(self, postfix):
        exp = postfix.exp()
        assert exp
        result = self.convert_exp(exp)
        postfix_ops = postfix.postfix_op()
        for postfix_op in postfix_ops:
            if postfix_op.eval_at():
                result = self.convert_eval_at(result, postfix_op.eval_at())
            elif postfix_op.transpose():
                result = sympy.transpose(result)
            elif postfix_op.POSTFIX_OP():
                op = postfix_op.POSTFIX_OP().getText()
                if op == '!':
                    result = sympy.factorial(result)
                elif op == '%':
                    result = result / 100
                elif op in self.id2type and self.id2type[op] == 'POSTFIX_OP':
                    assert op in self.id2func, f'function for {op} not found'
                    # unsupport ast function
                    result = self.id2func[op](result)
                else:
                    raise Exception(f'unknown postfix operator {op}')
            else:
                raise Exception(
                    f'unknown postfix operator {postfix_op.getText()}')
        return result

    def convert_exp(self, exp):
        comp = exp.comp()
        assert comp
        supexpr = exp.supexpr()
        if supexpr:
            return self.convert_comp(comp) ** self.convert_supexpr(supexpr)
        else:
            return self.convert_comp(comp)

    def convert_supexpr(self, supexpr):
        exp = supexpr.exp()
        if exp:
            return self.convert_exp(exp)
        else:
            return self.convert_expr(supexpr.expr())

    def convert_comp(self, comp):
        if comp.group():
            return self.convert_group(comp.group())
        elif comp.abs_group():
            return self.convert_abs_group(comp.abs_group())
        elif comp.func():
            return self.convert_func(comp.func())
        elif comp.matrix():
            return self.convert_matrix(comp.matrix())
        elif comp.reduceit():
            return self.convert_reduceit(comp.reduceit())
        elif comp.lim():
            return self.convert_lim(comp.lim())
        elif comp.log():
            return self.convert_log(comp.log())
        elif comp.integral():
            return self.convert_integral(comp.integral())
        elif comp.atom():
            return self.convert_atom(comp.atom())

    def convert_group(self, group):
        return self.convert_expr(group.expr())

    def convert_abs_group(self, abs_group):
        return sympy.Abs(self.convert_expr(abs_group.expr()))

    def convert_func(self, func):
        func_base_name = func.FUNC().getText()
        if func.subargs():
            subargs = func.subargs().getText()
        else:
            subargs = ''
        func_name = func_base_name + subargs
        supexpr = None
        if func.supexpr():
            supexpr = self.convert_supexpr(func.supexpr())
        if func_base_name in self.id2type and self.id2type[func_base_name] == 'FUNC':
            if func_name in self.id2func:
                if supexpr:
                    return self.id2func[func_name](func) ** supexpr
                else:
                    return self.id2func[func_name](func)
            else:
                func_args = func.args()
                if func_args:
                    args = [self.convert_relation(
                        arg) for arg in func_args.relation()]
                else:
                    args = [self.convert_mp(func.mp())]
                if supexpr:
                    return sympy.Function(func_name)(*args) ** supexpr
                else:
                    return sympy.Function(func_name)(*args)
        else:
            raise Exception(f'unknown function {func_name}')

    def convert_matrix(self, matrix):
        func_name = matrix.FUNC_MAT().getText()
        if func_name in self.id2type and self.id2type[func_name] == 'FUNC_MAT':
            assert func_name in self.id2func, f'function for {func_name} not found'
            return self.id2func[func_name](matrix)
        else:
            raise Exception(f'unknown matrix function {func_name}')
        
    def convert_subassign(self, subassign):
        if subassign.atom():
            return None, self.convert_atom(subassign.atom())
        elif subassign.expr():
            return None, self.convert_expr(subassign.expr())
        elif subassign.relation():
            # assert relation is `symbol = expr`
            rel = self.convert_relation(subassign.relation())
            assert isinstance(rel, sympy.Equality)
            return rel.lhs, rel.rhs
        
    def convert_supassign(self, supassign):
        if supassign.exp():
            return None, self.convert_exp(supassign.exp())
        elif supassign.expr():
            return None, self.convert_expr(supassign.expr())
        elif supassign.relation():
            rel = self.convert_relation(supassign.relation())
            assert isinstance(rel, sympy.Equality)
            assert isinstance(rel.lhs, sympy.Symbol), f'lhs of {supassign.relation().getText()} is not a symbol'
            return rel.lhs, rel.rhs
    
    def convert_subsupassign(self, subsupassign):
        symbol = None
        sub = None
        sup = None
        # process sub
        if subsupassign.subassign():
            sym, sub = self.convert_subassign(subsupassign.subassign())
            if sym:
                symbol = sym
        # process sup
        if subsupassign.supexpr():
            sup = self.convert_supexpr(subsupassign.supexpr())
        elif subsupassign.supassign():
            sym, sup = self.convert_supassign(subsupassign.supassign())
            if sym:
                symbol = sym
        return (symbol, sub, sup)

    def convert_reduceit(self, reduceit):
        reduce_name = reduceit.REDUCE_OP().getText()
        if reduce_name in self.id2type and self.id2type[reduce_name] == 'REDUCE_OP':
            assert reduce_name in self.id2func, f'function for {reduce_name} not found'
            return self.id2func[reduce_name](reduceit)
        else:
            raise Exception(f'unknown reduce function {reduce_name}')

    def convert_lim(self, lim):
        symbol = self.convert_symbol(lim.symbol())
        expr = self.convert_expr(lim.expr())
        additive = self.convert_additive(lim.additive())
        return sympy.Limit(additive, symbol, expr)

    def convert_log(self, log):
        if log.expr():
            value = self.convert_expr(log.expr())
        else:
            assert log.mp()
            value = self.convert_mp(log.mp())
        if log.subexpr():
            subexpr = self.convert_subexpr(log.subexpr())
            return sympy.log(value, subexpr)
        else:
            return sympy.log(value)

    def convert_integral(self, integral):
        subsupexpr = integral.subsupexpr()
        additive = self.convert_additive(integral.additive())
        symbol = self.convert_symbol(integral.symbol())
        if subsupexpr:
            subexpr, supexpr = self.convert_subsupexpr(subsupexpr)
            return sympy.Integral(additive, (symbol, subexpr, supexpr))
        else:
            return sympy.Integral(additive, symbol)

    def convert_subsupexpr(self, subsupexpr):
        subexpr = self.convert_subexpr(subsupexpr.subexpr())
        supexpr = self.convert_supexpr(subsupexpr.supexpr())
        return subexpr, supexpr

    def convert_subexpr(self, subexpr):
        if subexpr.atom():
            return self.convert_atom(subexpr.atom())
        elif subexpr.expr():
            return self.convert_expr(subexpr.expr())
        else:
            raise Exception(f'unknown subexpr {subexpr.getText()}')

    def convert_supexpr(self, supexpr):
        if supexpr.exp():
            return self.convert_exp(supexpr.exp())
        elif supexpr.expr():
            return self.convert_expr(supexpr.expr())
        else:
            raise Exception(f'unknown supexpr {supexpr.getText()}')

    def convert_atom(self, atom):
        if atom.NUMBER():
            # convert to a rational number but not a float
            return sympy.Rational(atom.NUMBER().getText())
        elif atom.symbol():
            return self.convert_symbol(atom.symbol())
        else:
            raise Exception(f'unknown atom {atom.getText()}')

    def convert_symbol(self, symbol):
        symbol_name = symbol.getText()
        if symbol_name in self.id2func:
            # it is a constant function but not a symbol
            return self.id2func[symbol_name]()
        else:
            return sympy.Symbol(symbol_name)

    def get_decorators(env):

        class operator(object):
            def __init__(self, type: str, convert_ast: Callable, name: str = None, ast=False):
                self.type = type
                self.convert_ast = convert_ast
                self.name = name
                self.func = None
                self.ast = ast
                self.env = env

            def __call__(self, func):
                assert isinstance(func, Callable)
                if self.name is None:
                    name = func.__name__
                    assert name.startswith(
                        'convert_'), f'function name "{name}" should start with "convert_"'
                    assert len(name) > len('convert_')
                    self.name = name[len('convert_'):].replace('_dot_', '.')
                if self.ast:
                    self.func = func
                else:
                    # convert ast to args and kwargs
                    @wraps(func)
                    def ast_func(*args, **kwargs):
                        args, kwargs = self.convert_ast(*args, **kwargs)
                        return func(*args, **kwargs)
                    self.func = ast_func
                    # save to env
                    self.env.define(self.name, self.type, self.func)
                return self.func

            def __repr__(self):
                return f'{self.type}(name = {self.name}, ast = {self.ast})'

        class relation_op(operator):

            def __init__(self, name: str = None, ast=False):
                def convert_ast(relation):
                    return [self.env.convert_relation(relation) for relation in relation.relation()], {}
                super().__init__('RELATION_OP', convert_ast, name, ast)

        class additive_op(operator):

            def __init__(self, name: str = None, ast=False):
                def convert_ast(additive):
                    return [self.env.convert_additive(additive) for additive in additive.additive()], {}
                super().__init__('ADDITIVE_OP', convert_ast, name, ast)

        class mp_op(operator):

            def __init__(self, name: str = None, ast=False):
                def convert_ast(mp):
                    return [self.env.convert_mp(mp) for mp in mp.mp()], {}
                super().__init__('MP_OP', convert_ast, name, ast)

        class postfix_op(operator):

            def __init__(self, name: str = None, ast=False):
                # unsupported ast so do nothing
                def convert_ast(result):
                    return [result], {}
                super().__init__('POSTFIX_OP', convert_ast, name, ast)

        class reduce_op(operator):

            def __init__(self, name: str = None, ast=False):
                def convert_ast(reduceit):
                    # reduceit: REDUCE_OP subsupassign mp;
                    symbol, sub, sup = self.env.convert_subsupassign(reduceit.subsupassign())
                    assert sub is not None and sup is not None
                    mp = self.env.convert_mp(reduceit.mp())
                    if symbol is None:
                        # get the first symbol in mp
                        symbol = mp.free_symbols.pop()
                    return [mp, (symbol, sub, sup)], {}
                super().__init__('REDUCE_OP', convert_ast, name, ast)

        class func(operator):

            def __init__(self, name: str = None, ast=False):
                def convert_ast(func):
                    func_args = func.args()
                    if func_args:
                        args = [self.env.convert_relation(
                            arg) for arg in func_args.relation()]
                    else:
                        args = [self.env.convert_mp(func.mp())]
                    return args, {}
                super().__init__('FUNC', convert_ast, name, ast)

        class func_mat(operator):

            def __init__(self, name: str = None, ast=False):
                def convert_ast(matrix):
                    mat = [[self.env.convert_relation(
                        arg) for arg in args.relation()] for args in matrix.mat_args().args()]
                    return [mat], {}
                super().__init__('FUNC_MAT', convert_ast, name, ast)

        class constant:

            def __init__(self, name: str = None, ast=False):
                self.type = 'CONSTANT'
                self.name = name
                self.func = None
                self.env = env

            def __call__(self, func):
                assert isinstance(func, Callable)
                if self.name is None:
                    name = func.__name__
                    assert name.startswith(
                        'convert_'), f'function name "{name}" should start with "convert_"'
                    assert len(name) > len('convert_')
                    self.name = name[len('convert_'):].replace('_dot_', '.')
                self.func = func
                self.env.define_symbol_base(self.name.split('_')[0])
                self.env.id2func[self.name] = self.func
                return self.func

            def __repr__(self):
                return f'{self.type}(name = {self.name})'

        return operator, relation_op, additive_op, mp_op, postfix_op, reduce_op, func, func_mat, constant


if __name__ == '__main__':
    convertor = TypstMathConverter()
    operator, relation_op, additive_op, mp_op, postfix_op, reduce_op, func, func_mat, constant = convertor.get_decorators()

    @func()
    def convert_sin(x):
        return sympy.sin(x)

    @func_mat()
    def convert_mat(mat):
        return sympy.matrices.Matrix(mat)
    
    convertor.define_symbol_base('x')
    convertor.define_symbol_base('y')
    convertor.define_symbol_base('z')
    expr = convertor.sympy('1 + sin^2 1/2 + x + 1')
    typst = convertor.typst(sympy.simplify(expr))
    assert typst == 'x + (sin(1/2))^2 + 2'

    expr = convertor.sympy('(x y)^y^(z+1)')
    typst = convertor.typst(sympy.simplify(expr))
    assert typst == '(x y)^y^(z + 1)'

    expr = convertor.sympy('mat(x + y, 2; z, 4)')
    typst = convertor.typst(sympy.simplify(expr))
    assert typst == 'mat(x + y, 2; z, 4)'

    convertor.define_function('f_1')
    expr = convertor.sympy('f_1^2(1) + f_1(1)')
    typst = convertor.typst(sympy.simplify(expr))
    assert typst == '(f_1(1) + 1) f_1(1)'

    expr = convertor.sympy('x * y * z')
    typst = convertor.typst(expr)
    assert typst == 'x y z'

    expr = convertor.sympy('(x + 1) * y * z')
    typst = convertor.typst(expr)
    assert typst == 'y z (x + 1)'

    expr = convertor.sympy('(x + 1) * y^(1/2)')
    typst = convertor.typst(expr)
    assert typst == 'sqrt(y) (x + 1)'

    expr = convertor.sympy('|x|')
    typst = convertor.typst(expr)
    assert typst == '|x|'

    expr = convertor.sympy('integral_1^2 x^2 dif x')
    typst = convertor.typst(expr)
    assert typst == 'integral_1^2 x^2 dif x'