from pymathlang.main import _pad_braces, Row, Identifier, Operator, Number


def test_pad_braces():
    string = "abc123"
    assert _pad_braces(string) == "{abc123}"


def test_simple_expression():
    expression = Row([Identifier("x"), Operator("+"), Number(3)])
    assert expression._render_to_mathml() == "<mrow><mi>x</mi><mo>+</mo><mn>3</mn></mrow>"
    assert expression._render_to_latex() == "x+3"
