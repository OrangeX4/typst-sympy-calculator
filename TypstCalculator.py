import itertools
from typing import Iterable
import sympy
from TypstConverter import TypstMathConverter

def unfold_process(process, expr):
    if isinstance(expr, list):
        return [unfold_process(process, e) for e in expr]
    elif isinstance(expr, dict):
        return {k: unfold_process(process, v) for k, v in expr.items()}
    else:
        try:
            return process(expr)
        except Exception:
            return expr

class TypstCalculator:

    def __init__(self, precision: int = 15, return_text=False, enable_subs=True, max_sub_count=1):
        self.converter = TypstMathConverter()
        self.precision = precision
        self.return_text = return_text
        self.enable_subs = enable_subs
        self.max_sub_count = max_sub_count
        self.var = {}

    def define(self, name: str, type: str, value: str):
        self.converter.define(name, type, value)

    def undefine(self, name: str):
        self.converter.undefine(name)

    def define_accent(self, accent_name: str):
        self.converter.define_accent(accent_name)

    def define_symbol_base(self, symbol_base_name: str):
        self.converter.define_symbol_base(symbol_base_name)

    def define_function(self, func_name: str):
        self.converter.define_function(func_name)

    def set_variance(self, name: str, value, simplify=False):
        if name.startswith('#'):
            name = name[1:]
        if not isinstance(value, str):
            self.var[name] = value
            return
        if simplify:
            self.var[name] = self._simplify(self.converter.sympy(value))
        else:
            self.var[name] = self.converter.sympy(value)
        name = '#' + name
        if not isinstance(value, str):
            self.var[name] = value
            return
        if simplify:
            self.var[name] = self._simplify(self.converter.sympy(value))
        else:
            self.var[name] = self.converter.sympy(value)

    def unset_variance(self, name: str):
        if name.startswith('#'):
            name = name[1:]
        if name in self.var:
            del self.var[name]
        name = '#' + name
        if name in self.var:
            del self.var[name]

    def clear_variance(self):
        self.var.clear()

    @property
    def variances(self):
        return {sympy.Symbol(k): v for k, v in self.var.items()}

    def sympy(self, typst_math: str):
        return self.converter.sympy(typst_math)

    def typst(self, sympy_expr):
        return self.converter.typst(sympy_expr)

    def doit(self, sympy_expr):
        '''
        doit until the expression is simplified
        '''
        if not hasattr(sympy_expr, 'doit'):
            return sympy_expr
        last = None
        while last != sympy_expr:
            last = sympy_expr
            sympy_expr = sympy_expr.doit()
        return sympy_expr

    def _subs(self, expr):
        sub_count = 0
        last = None
        while last != expr and sub_count < self.max_sub_count:
            last = expr
            expr = unfold_process(lambda e: e.subs(self.variances, simultaneous=True), expr)
            sub_count += 1
        return expr

    def subs(self, typst_math: str):
        expr = self.sympy(typst_math)
        expr = self._subs(expr)
        if self.return_text:
            return self.typst(expr)
        else:
            return expr

    def _simplify(self, expr):
        if self.enable_subs:
            expr = self._subs(expr)
        result = unfold_process(lambda e: sympy.simplify(self.doit(e)), expr)
        return result

    def simplify(self, typst_math: str):
        expr = self.sympy(typst_math)
        result = self._simplify(expr)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def _evalf(self, expr, n: int = None):
        if self.enable_subs:
            expr = self._subs(expr)
        result = unfold_process(lambda e: sympy.N(sympy.simplify(self.doit(e)), n=n if n else self.precision), expr)
        return result

    def evalf(self, typst_math: str, n: int = None):
        expr = self.sympy(typst_math)
        result = self._evalf(expr, n)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def _solve(self, expr):
        if self.enable_subs:
            expr = self._subs(expr)
        if isinstance(expr, Iterable):
            # is all equations
            is_all_equations = True
            for e in expr:
                if not isinstance(e, sympy.Eq):
                    is_all_equations = False
                    break
            if is_all_equations:
                result = []
                free_symbols = set()
                for e in expr:
                    free_symbols.update(e.free_symbols)
                # subsets of free_symbols
                subsets = []
                for i in range(1, len(free_symbols) + 1):
                    subsets.extend(itertools.combinations(free_symbols, i))
                for subset in subsets:
                    result.extend(sympy.solve(expr, subset, dict=True))
            else:
                result = sympy.solve(expr, dict=True)
        else:
            if isinstance(expr, sympy.Eq):
                result = []
                free_symbols = expr.free_symbols
                # subsets of free_symbols
                subsets = []
                for i in range(1, len(free_symbols) + 1):
                    subsets.extend(itertools.combinations(free_symbols, i))
                for subset in subsets:
                    result.extend(sympy.solve(expr, subset, dict=True))
            else:
                result = sympy.solve(expr, dict=True)
        return result

    def solve(self, typst_math: str):
        expr = self.sympy(typst_math)
        result = self._solve(expr)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    @property
    def id2type(self):
        return self.converter.id2type

    @property
    def id2func(self):
        return self.converter.id2func

    @id2type.setter
    def id2type(self, value):
        self.converter.id2type = value

    @id2func.setter
    def id2func(self, value):
        self.converter.id2func = value

    def get_decorators(self):
        return self.converter.get_decorators()


if __name__ == '__main__':
    calculator = TypstCalculator(return_text=True, enable_subs=True)
    operator, relation_op, additive_op, mp_op, postfix_op, reduce_op, func, func_mat, constant = calculator.get_decorators()

    calculator.define_symbol_base('a')
    calculator.define_symbol_base('pi')

    expr = calculator.simplify('1 + 1')
    assert expr == '2'

    expr = calculator.evalf('1/2', n=3)
    assert expr == '0.500'

    calculator.set_variance('a', '1/2')
    expr = calculator.simplify('a + 1')
    assert expr == '3/2'

    calculator.unset_variance('a')
    expr = calculator.simplify('a + 1')
    assert expr == 'a + 1' or expr == '1 + a'

    @constant()
    def convert_pi():
        return sympy.pi

    expr = calculator.simplify('pi')
    assert expr == 'pi'
