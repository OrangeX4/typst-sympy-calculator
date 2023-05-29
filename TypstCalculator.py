import sympy
from TypstConverter import TypstMathConverter


class TypstCalculator:

    def __init__(self, precision: int=15, return_text=False, enable_subs=True):
        self.converter = TypstMathConverter()
        self.precision = precision
        self.return_text = return_text
        self.enable_subs = enable_subs
        self.var = {}

    def define(self, name: str, type: str, value: str):
        self.converter.define(name, type, value)

    def undefine(self, name: str):
        self.converter.undefine(name)

    def define_accent(self, accent_name: str):
        self.converter.define_accent(accent_name)

    def define_symbol_base(self, symbol_base_name: str):
        self.converter.define_symbol_base(symbol_base_name)

    def set_variance(self, name: str, value: str, simplify=True):
        if simplify:
            self.var[name] = self.converter.sympy(value).simplify()
        else:
            self.var[name] = self.converter.sympy(value)

    def unset_variance(self, name: str):
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

    def subs(self, typst_math: str):
        expr = self.converter.sympy(typst_math)
        result = expr.subs(self.variances, simultaneous=True)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def simplify(self, typst_math: str):
        expr = self.converter.sympy(typst_math)
        if self.enable_subs:
            expr = expr.subs(self.variances, simultaneous=True)
        result = sympy.simplify(self.doit(expr))
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def evalf(self, typst_math: str, n: int=None):
        expr = self.converter.sympy(typst_math)
        if self.enable_subs:
            expr = expr.subs(self.variances, simultaneous=True)
        result = sympy.N(sympy.simplify(self.doit(expr)), n=n if n else self.precision)
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