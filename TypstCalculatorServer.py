import sympy
import math
import re
import os
from TypstCalculator import TypstCalculator
from DefaultCalculator import get_default_calculator


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

    def init(self, typst_file: str):
        self.cache_mode = False
        typst_content = ''
        assert os.path.exists(typst_file), 'File not found: ' + typst_file
        with open(typst_file, 'r', encoding='utf-8') as f:
            typst_content = f.read()
        import_paths = self.find_import_and_include(typst_content)
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
                absolute_path = os.path.abspath(os.path.join(os.path.dirname(typst_file), import_path))
            self.load_with_file(absolute_path)
        self.cache_mode = True

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
        result = expr.subs(self.variances, simultaneous=True)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def simplify(self, typst_math: str, typst_file: str = None):
        expr = self.sympy(typst_math, typst_file)
        if self.enable_subs:
            expr = expr.subs(self.variances, simultaneous=True)
        result = sympy.simplify(self.doit(expr))
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def evalf(self, typst_math: str, typst_file: str = None, n: int = None):
        expr = self.sympy(typst_math, typst_file)
        if self.enable_subs:
            expr = expr.subs(self.variances, simultaneous=True)
        result = sympy.N(sympy.simplify(self.doit(expr)),
                         n=n if n else self.precision)
        if self.return_text:
            return self.typst(result)
        else:
            return result

    def clear_cache(self):
        for name in self.cache_variance_names:
            self.unset_variance(name)
        self.cache_variance_names = []

    def set_variance(self, name: str, value, simplify=True):
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
        pattern1 = r'\s*```python\s*\n\s*# typst-calculator\s*\n([\d\D]*?)```'
        pattern2 = r'\s*```py\s*\n\s*# typst-calculator\s*\n([\d\D]*?)```'
        pattern3 = r'\s*```typst-calculator\s*\n([\d\D]*?)```'
        for match in re.finditer(pattern1, typst_content):
            self.exec(match.group(1))
        for match in re.finditer(pattern2, typst_content):
            self.exec(match.group(1))
        for match in re.finditer(pattern3, typst_content):
            self.exec(match.group(1))

    def find_and_define_accent(self, typst_content: str):
        '''
        #let acc(x) = math.accent(x, math.grave)
        '''
        pattern = r'#let\s+([a-zA-z][a-zA-z0-9]*)\(\s*([_a-zA-z][_\-a-zA-z0-9]*)\s*\)\s*=\s*math\.accent'
        for match in re.finditer(pattern, typst_content):
            accent_name = match.group(1)
            accent_arg = match.group(2)
            self.calculator.define_accent(accent_name)

    def find_and_define_func(self, typst_content: str):
        '''
        #let fn = math.op("fn")
        '''
        pattern = r'#let\s+([a-zA-z][a-zA-z0-9]*)\s*=\s*math\.op'
        for match in re.finditer(pattern, typst_content):
            func_name = match.group(1)
            self.calculator.define_function(func_name)

    def find_and_define_symbol(self, typst_content: str):
        '''
        #let xy = math.italic("xy")
        #let xy = symbol("🖂", ("stamped", "🖃"),)
        '''
        pattern1 = r'#let\s+([a-zA-z][a-zA-z0-9]*)\s*=\s*math\.(?!op)'
        pattern2 = r'#let\s+([a-zA-z][a-zA-z0-9]*)\s*=\s*symbol(\(.+\))\s*\n'
        pattern3 = r'\("(.+?)"\s*,\s*"(.+?)"\)'
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
        pattern1 = r'#let\s+([a-zA-z][._a-zA-z0-9]*)\s*=\s*([0-9]+(\.[0-9]*)?\%?)\s*\n'
        pattern2 = r'#let\s+([a-zA-z][._a-zA-z0-9]*)\s*=\s*\$(.+?)\$\s*\n'
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
        pattern1 = r'#import\s+"(.+?)"'
        pattern2 = r'#include\s+"(.+?)"'
        paths = []
        for match in re.finditer(pattern1, typst_content):
            paths.append(match.group(1))
        for match in re.finditer(pattern2, typst_content):
            paths.append(match.group(1))
        return paths


if __name__ == '__main__':
    server = TypstCalculatorServer()
    typst_file = os.path.abspath(r'./tests/test.typ')
    server.init(typst_file)
    server.return_text = True
    expr = server.simplify('1 + 1', typst_file)
    server.enable_subs = False
    expr = server.simplify('a + 1', typst_file)
    print(expr)
    server.enable_subs = True
    print(expr)
    expr = server.simplify('a + 1', typst_file)
    print(expr)
    expr = server.simplify('b + 1', typst_file)
    print(expr)
    expr = server.simplify('cmat(1, 2)', typst_file)
    print(expr)
    expr = server.simplify('f(1) + f(1)', typst_file)
    print(expr)
    expr = server.simplify('xy + mail + mail.stamped', typst_file)
    print(expr)