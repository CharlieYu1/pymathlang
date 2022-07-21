from pymathlang.main import (
    _pad_braces,
    Row,
    Identifier,
    Operator,
    Number,
    Fraction,
    MathEnvironment,
    InlineMathEnvironment,
)


def test_pad_braces():
    string = "abc123"
    assert _pad_braces(string) == "{abc123}"


def test_simple_expression():
    expression = Row([Identifier("x"), Operator("+"), Number(3)])
    assert (
        expression._render_to_mathml() == "<mrow><mi>x</mi><mo>+</mo><mn>3</mn></mrow>"
    )
    assert expression._render_to_latex() == "x+3"


def test_math_environment():
    expression = MathEnvironment(Row([Identifier("x"), Operator("+"), Number(3)]))
    assert isinstance(expression._elements[0], Row)
    assert (
        expression._render_to_mathml()
        == '<math display="block"><mrow><mi>x</mi><mo>+</mo><mn>3</mn></mrow></math>'
    )
    assert expression._render_to_latex() == "\\[x+3\\]"


def test_inline_math_environment():
    expression = InlineMathEnvironment(Row([Identifier("x"), Operator("+"), Number(3)]))
    assert isinstance(expression._elements[0], Row)
    assert (
        expression._render_to_mathml()
        == '<math display="inline"><mrow><mi>x</mi><mo>+</mo><mn>3</mn></mrow></math>'
    )
    assert expression._render_to_latex() == "\\(x+3\\)"


def test_fractions():
    expression = Fraction(
        [Identifier("x"), Row([Identifier("p"), Operator("-"), Identifier("q")])]
    )
    assert (
        expression._render_to_mathml()
        == "<mfrac><mi>x</mi><mrow><mi>p</mi><mo>-</mo><mi>q</mi></mrow></mfrac>"
    )
    assert expression._render_to_latex() == "\\frac{x}{p-q}"
