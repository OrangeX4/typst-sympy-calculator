#let hidden(content) = {}

#let cmat(..args) = {
  let mat = if (type(args.pos().at(0)) != "array") { (args.pos(),) } else { args.pos() }
  let mat_t = ()
  for j in range(mat.at(0).len()) {
    mat_t.push(())
    for i in range(mat.len()) {
      mat_t.at(j).push(mat.at(i).at(j))
    }
  }
  math.mat(..mat_t)
}

// define accents
#let acc(x) = math.accent(x, math.grave)

// define operators
#let add = math.op("add")
#let f = math.op("f")

// define symbols
#let xy = math.italic("xy")
#let mail = symbol("🖂", ("stamped", "🖃"),)

```py
# typst-calculator
# ↑ the line is necessary for typst-calculator recognizing

@func()
def convert_add(a, b):
    return a + b
```

#hidden[

```typst-calculator
# ↑ or you can just use `typst-calculator` but not `py` or `python`

@func_mat()
def convert_cmat(matrix):
    return sympy.Matrix(matrix).T
```

]

