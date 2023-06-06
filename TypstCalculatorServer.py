import itertools
from typing import Iterable
import sympy
import math
import re
import os
from TypstCalculator import TypstCalculator
from DefaultTypstCalculator import get_default_calculator

VERSION = '0.5.0'


class TypstCalculatorServer:

    def __init__(self, calculator: TypstCalculator = None) -> None:
        if calculator is None:
            calculator = get_default_calculator()
        self.calculator = calculator
        self.cache_variance_names = []
        self.cache_mode = True

    @property
    def var(self):
        return self.calculator.var

    @property
    def variances(self):
        return self.calculator.variances

    @property
    def return_text(self):
        return self.calculator.return_text

    @return_text.setter
    def return_text(self, value):
        self.calculator.return_text = value

    @property
    def enable_subs(self):
        return self.calculator.enable_subs

    @enable_subs.setter
    def enable_subs(self, value):
        self.calculator.enable_subs = value

    def init(self, typst_file: str) -> list:
        self.cache_mode = False
        typst_content = ''
        assert os.path.exists(typst_file), 'File not found: ' + typst_file
        with open(typst_file, 'r', encoding='utf-8') as f:
            typst_content = f.read()
        import_paths = self.find_import_and_include(typst_content)
        res = []
        for import_path in import_paths:
            # TYPST_ROOT environment variable
            if import_path.startswith('/'):
                if 'TYPST_ROOT' in os.environ:
                    root = os.environ['TYPST_ROOT']
                    absolute_path = os.path.join(root, import_path[1:])
                else:
                    absolute_path = import_path
            else:
                # Convert '../../path/to/typst'
                absolute_path = os.path.abspath(os.path.join(
                    os.path.dirname(typst_file), import_path))
            res.append(absolute_path)
            self.load_with_file(absolute_path)
        self.cache_mode = True
        return res

    def load_with_file(self, typst_file: str):
        typst_content = ''
        assert os.path.exists(typst_file), 'File not found: ' + typst_file
        with open(typst_file, 'r', encoding='utf-8') as f:
            typst_content = f.read()
        self.find_and_define_accent(typst_content)
        self.find_and_define_func(typst_content)
        self.find_and_define_symbol(typst_content)
        self.find_and_exec(typst_content)
        self.find_and_set_variance(typst_content)

    def sympy(self, typst_math: str, typst_file: str = None):
        if typst_file is not None:
            if self.cache_mode:
                self.clear_cache()
            self.load_with_file(typst_file)
        return self.calculator.sympy(typst_math)

    def typst(self, sympy_expr):
        return self.calculator.typst(sympy_expr)

    def doit(self, sympy_expr):
        return self.calculator.doit(sympy_expr)

    def subs(self, typst_math: str, typst_file: str = None):
        expr = self.sympy(typst_math, typst_file)
        result = self.calculator._subs(expr)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def simplify(self, typst_math: str, typst_file: str = None):
        expr = self.sympy(typst_math, typst_file)
        result = self.calculator._simplify(expr)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def evalf(self, typst_math: str, typst_file: str = None, n: int = None):
        expr = self.sympy(typst_math, typst_file)
        result = self.calculator._evalf(expr, n)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def solve(self, typst_math: str, typst_file: str = None):
        expr = self.sympy(typst_math, typst_file)
        result = self.calculator._solve(expr)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def clear_cache(self):
        for name in self.cache_variance_names:
            self.unset_variance(name)
        self.cache_variance_names = []

    def set_variance(self, name: str, value, simplify=False):
        if self.cache_mode:
            self.cache_variance_names.append(name)
        self.calculator.set_variance(name, value, simplify)

    def unset_variance(self, name: str):
        self.calculator.unset_variance(name)

    def clear_variance(self):
        self.calculator.clear_variance()

    def exec(self, python_code: str):
        calc = self.calculator
        set_variance, unset_variance, clear_variance = self.set_variance, self.unset_variance, self.clear_variance
        operator, relation_op, additive_op, mp_op, postfix_op, reduce_op, func, func_mat, constant = calc.get_decorators()
        # replace all \t with 4 spaces
        python_code = python_code.replace('\t', '    ')
        # remove leading indent from python code
        lines = python_code.split('\n')
        indent = len(lines[0]) - len(lines[0].lstrip())
        new_python_code = ''
        for line in lines:
            assert set(' ' + line[:indent]) == set(' '), 'IndentationError'
            new_python_code += line[indent:] + '\n'
        exec(new_python_code)

    def find_and_exec(self, typst_content: str):
        '''
        ```python
        # typst-calculator
        test()
        ```

        ```typst-calculator
        test()
        ```
        '''
        typst_content = self.remove_comments(typst_content)
        pattern1 = r'[\t ]*```python[\t ]*\n[\t ]*# typst-calculator[\t ]*\n([\d\D]*?)```'
        pattern2 = r'[\t ]*```py[\t ]*\n[\t ]*# typst-calculator[\t ]*\n([\d\D]*?)```'
        pattern3 = r'[\t ]*```typst-calculator[\t ]*\n([\d\D]*?)```'
        pattern4 = r'[\t ]*```typst-sympy-calculator[\t ]*\n([\d\D]*?)```'
        for match in re.finditer(pattern1, typst_content):
            self.exec(match.group(1))
        for match in re.finditer(pattern2, typst_content):
            self.exec(match.group(1))
        for match in re.finditer(pattern3, typst_content):
            self.exec(match.group(1))
        for match in re.finditer(pattern4, typst_content):
            self.exec(match.group(1))

    def find_and_define_accent(self, typst_content: str):
        '''
        #let acc(x) = math.accent(x, math.grave)
        '''
        typst_content = self.remove_comments(typst_content)
        pattern = r'#let[\t ]+([a-zA-z][a-zA-z0-9]*)\([\t ]*([_a-zA-z][_\-a-zA-z0-9]*)[\t ]*\)[\t ]*=[\t ]*math\.accent'
        for match in re.finditer(pattern, typst_content):
            accent_name = match.group(1)
            accent_arg = match.group(2)
            self.calculator.define_accent(accent_name)

    def find_and_define_func(self, typst_content: str):
        '''
        #let fn = math.op("fn")
        '''
        typst_content = self.remove_comments(typst_content)
        pattern = r'#let[\t ]+([a-zA-z][a-zA-z0-9]*)[\t ]*=[\t ]*math\.op'
        for match in re.finditer(pattern, typst_content):
            func_name = match.group(1)
            self.calculator.define_function(func_name)

    def find_and_define_symbol(self, typst_content: str):
        '''
        #let xy = math.italic("xy")
        #let xy = symbol("🖂", ("stamped", "🖃"),)
        '''
        typst_content = self.remove_comments(typst_content)
        pattern1 = r'#let[\t ]+([a-zA-z][a-zA-z0-9]*)[\t ]*=[\t ]*math\.(?!op)'
        pattern2 = r'#let[\t ]+([a-zA-z][a-zA-z0-9]*)[\t ]*=[\t ]*symbol(\(.+\))[\t ]*\n'
        pattern3 = r'\("(.+?)"[\t ]*,[\t ]*"(.+?)"\)'
        for match in re.finditer(pattern1, typst_content):
            symbol_name = match.group(1)
            self.calculator.define_symbol_base(symbol_name)
        for match in re.finditer(pattern2, typst_content):
            symbol_name = match.group(1)
            self.calculator.define_symbol_base(symbol_name)
            for m in re.finditer(pattern3, match.group(2)[1:-1]):
                modify = m.group(1)
                self.calculator.define_symbol_base(symbol_name + '.' + modify)

    def find_and_set_variance(self, typst_content: str):
        '''
        #let var = 2.0
        #let var = $x + y$
        '''
        typst_content = self.remove_comments(typst_content)
        pattern1 = r'#let[\t ]+([a-zA-z][._a-zA-z0-9]*)[\t ]*=[\t ]*([-+]?[\t ]*[0-9]+(\.[0-9]*)?\%?)[\t ]*\n'
        pattern2 = r'#let[\t ]+([a-zA-z][._a-zA-z0-9]*)[\t ]*=[\t ]*\$(.+?)\$[\t ]*\n'
        for match in re.finditer(pattern1, typst_content):
            symbol_name = match.group(1)
            self.set_variance(symbol_name, match.group(2))
        for match in re.finditer(pattern2, typst_content):
            symbol_name = match.group(1)
            self.set_variance(symbol_name, match.group(2))

    def find_import_and_include(self, typst_content: str) -> list:
        '''
        #import "../../../Typst/report-template.typ"
        #include "../../../Typst/report-template.typ"
        '''
        typst_content = self.remove_comments(typst_content)
        pattern1 = r'#import[\t ]+"(.+?)"'
        pattern2 = r'#include[\t ]+"(.+?)"'
        paths = []
        for match in re.finditer(pattern1, typst_content):
            paths.append(match.group(1))
        for match in re.finditer(pattern2, typst_content):
            paths.append(match.group(1))
        return paths

    def remove_comments(self, typst_content: str) -> str:
        '''
        // #let var = 2.0
        /* #let var = 2.0 */
        '''
        pattern1 = r'\/\/.*?\n'
        pattern2 = r'\/\*[\d\D]*?\*\/'
        return re.sub(pattern2, '', re.sub(pattern1, '', typst_content))


if __name__ == '__main__':
    server = TypstCalculatorServer()
    typst_file = os.path.abspath(r'./tests/test.typ')
    server.init(typst_file)
    server.return_text = True
    expr = server.simplify('1 + 1', typst_file)
    print(expr)
    server.enable_subs = False
    expr = server.simplify('#a + 1', typst_file)
    print(expr)
    server.enable_subs = True
    expr = server.simplify('#a + 1', typst_file)
    print(expr)
    expr = server.simplify('b + 1', typst_file)
    print(expr)
    expr = server.simplify('#cmat(1, 2)', typst_file)
    print(expr)
    expr = server.simplify('f(1) + f(1)', typst_file)
    print(expr)
    expr = server.simplify('xy + mail + mail.stamped', typst_file)
    print(expr)
    expr = server.solve('x + y + z = 1')
    print(expr)
    expr = server.solve('cases(x + y + z = 1, x = 2)')
    print(expr)
    expr = server.solve('cases(x^2 + y = 4, y = 2)')
    print(expr)
    expr = server.solve('cases(x < 2, x > 1)')
    print(expr)
