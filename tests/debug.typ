#let null = math.op("N")

```typst-sympy-calculator
@func_mat()
def convert_null(mat):
    return sympy.Matrix(mat).nullspace()
```