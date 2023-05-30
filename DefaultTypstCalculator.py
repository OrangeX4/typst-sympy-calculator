import sympy
from TypstCalculator import TypstCalculator


def get_default_calculator(calculator: TypstCalculator = None, complex_number: bool = True):
    if calculator is None:
        calculator = TypstCalculator(return_text=False, enable_subs=True)

    operator, relation_op, additive_op, mp_op, postfix_op, reduce_op, func, func_mat, constant = calculator.get_decorators()

    # Accents
    accents = ['cancel', 'grave', 'acute', 'hat', 'tilde', 'macron', 'breve', 'hdot', 'hdot.double',
               'hdot.triple', 'hdot.quad', 'diaer', 'circle', 'acute.double', 'caron', 'harrow', 'harrow.l']
    for accent in accents:
        calculator.define_accent(accent)

    # Styles
    styles = ['upright', 'italic', 'bold']
    for style in styles:
        calculator.define_accent(style)

    # Variants
    variants = ['serif', 'sans', 'frak', 'mono', 'bb', 'cal']
    for variant in variants:
        calculator.define_accent(variant)

    # Under/Over
    underover = ['underline', 'overline']
    for uo in underover:
        calculator.define_accent(uo)

    # Symbols
    abc = 'abcdefghijklmnopqrstuvwxyz'
    for c in abc:
        calculator.define_symbol_base(c)
        calculator.define_symbol_base(c.upper())

    greeks = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa',
              'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi',
              'chi', 'psi', 'omega']
    for greek in greeks:
        calculator.define_symbol_base(greek)
        calculator.define_symbol_base(greek[0].upper() + greek[1:])

    greek_alts = ['beta.alt', 'epsilon.alt', 'kappa.alt',
                  'phi.alt', 'pi.alt', 'rho.alt', 'theta.alt']
    for greek_alt in greek_alts:
        calculator.define_symbol_base(greek_alt)

    # Constants
    @constant()
    def convert_oo():
        return sympy.oo

    calculator.set_variance('pi', sympy.pi)
    calculator.set_variance('e', sympy.E)
    calculator.set_variance('E', sympy.E)

    # complex_number
    if complex_number:
        calculator.set_variance('i', sympy.I)
        calculator.set_variance('I', sympy.I)
        calculator.set_variance('j', sympy.I)

    # Relation Operators
    @relation_op()
    def convert_eq(a, b):
        return sympy.Eq(a, b)

    @relation_op()
    def convert_eq_dot_not(a, b):
        return sympy.Ne(a, b)

    @relation_op()
    def convert_gt(a, b):
        return sympy.Gt(a, b)

    @relation_op()
    def convert_lt(a, b):
        return sympy.Lt(a, b)

    @relation_op()
    def convert_gt_dot_eq(a, b):
        return sympy.Ge(a, b)

    @relation_op()
    def convert_lt_dot_eq(a, b):
        return sympy.Le(a, b)

    # Additive Operators
    @additive_op()
    def convert_plus(a, b):
        return a + b

    # Mp Operators
    @mp_op()
    def convert_times(a, b):
        return a * b

    @mp_op()
    def convert_times_dot(a, b):
        return a * b

    @mp_op()
    def convert_div(a, b):
        return a / b

    # Postfix Operators
    @postfix_op()
    def convert_degree(expr):
        return expr / 180 * sympy.pi

    # Matrix
    @func_mat()
    def convert_mat(mat):
        return sympy.Matrix(mat)

    @func()
    def convert_vec(*vec):
        return sympy.Matrix(vec)

    # Functions
    @func()
    def convert_binom(n, k):
        return sympy.binomial(n, k)

    @func()
    def convert_frac(n, d):
        return sympy.Rational(n, d)

    @func()
    def convert_lr(expr):
        return expr

    @func()
    def convert_sqrt(expr):
        return sympy.sqrt(expr)

    @func()
    def convert_root(n, expr):
        return sympy.root(expr, n)

    @func()
    def convert_round(expr):
        return sympy.Number(round(expr.evalf(), 0))

    @func()
    def convert_abs(expr):
        return sympy.Abs(expr)

    @func()
    def convert_arccos(expr):
        return sympy.acos(expr)

    @func()
    def convert_arcsin(expr):
        return sympy.asin(expr)

    @func()
    def convert_arctan(expr):
        return sympy.atan(expr)

    @func()
    def convert_arctan2(expr):
        return sympy.atan2(expr)

    @func()
    def convert_ceil(expr):
        return sympy.ceiling(expr)

    @func()
    def convert_cos(expr):
        return sympy.cos(expr)

    @func()
    def convert_cosh(expr):
        return sympy.cosh(expr)

    @func()
    def convert_fact(expr):
        return sympy.factorial(expr)

    @func()
    def convert_floor(expr):
        return sympy.floor(expr)

    @func()
    def convert_gcd(f, g):
        return sympy.gcd(f, g)

    @func()
    def convert_lcm(f, g):
        return sympy.lcm(f, g)

    @func()
    def convert_log(expr):
        return sympy.log(expr)

    @func()
    def convert_max(*args):
        return sympy.Max(*args)

    @func()
    def convert_min(*args):
        return sympy.Min(*args)

    @func()
    def convert_pow(b, e):
        return sympy.Pow(b, e)

    @func()
    def convert_quo(f, g):
        return sympy.quo(f, g)

    @func()
    def convert_rem(f, g):
        return sympy.rem(f, g)

    @func()
    def convert_sin(expr):
        return sympy.sin(expr)

    @func()
    def convert_sinh(expr):
        return sympy.sinh(expr)

    @func()
    def convert_tan(expr):
        return sympy.tan(expr)

    @func()
    def convert_tanh(expr):
        return sympy.tanh(expr)

    # Matrix Functions
    @func()
    def convert_rank(expr):
        return sympy.Matrix.rank(expr)

    @func()
    def convert_rref(expr):
        return sympy.Matrix.rref(expr)

    @func()
    def convert_det(expr):
        return sympy.det(expr)

    @func()
    def convert_transpose(expr):
        return sympy.transpose(expr)

    @func()
    def convert_inverse(expr):
        return expr ** -1

    @func()
    def convert_trace(expr):
        return sympy.trace(expr)

    return calculator


if __name__ == '__main__':

    calculator = get_default_calculator(complex_number=True)
    calculator.return_text = True

    operator, relation_op, additive_op, mp_op, postfix_op, \
        reduce_op, func, func_mat, constant = calculator.get_decorators()

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

    expr = calculator.evalf('pi', n=3)
    assert expr == '3.14'

    expr = calculator.simplify('max(1, 2)')
    assert expr == '2'

    calculator.define_function('f')
    expr = calculator.simplify('f(1) + f(1) - f(1)')
    assert expr == 'f(1)'

    expr = calculator.simplify('lim_(x -> oo) 1/x')
    assert expr == '0'
