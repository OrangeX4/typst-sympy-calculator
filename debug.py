import os
from TypstCalculatorServer import TypstCalculatorServer

server = TypstCalculatorServer()
typst_file = os.path.abspath(r'./tests/debug.typ')
server.init(typst_file)
server.return_text = True
expr = server.simplify('null(mat(1, 2; 2, 4))', typst_file)
print(expr)