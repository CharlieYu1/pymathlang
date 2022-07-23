from ast import Num
from pymathlang.main import (
    _pad_braces,
    Row,
    Identifier,
    Operator,
    Number,
    Fraction,
    MathEnvironment,
    InlineMathEnvironment,
    Table,
    Tr,
    Td,
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


def test_table_element():
    table_element = Td(Identifier("x"))
    assert table_element._render_to_mathml() == "<mtd><mi>x</mi></mtd>"


def test_table_row():
    table_row_element = Tr(
        [
            Td([Identifier("x"), Operator("+"), Number(3)]),
            Td(Operator("=")),
            Td(Number(8)),
        ]
    )
    assert (
        table_row_element._render_to_mathml()
        == "<mtr><mtd><mi>x</mi><mo>+</mo><mn>3</mn></mtd><mtd><mo>=</mo></mtd><mtd><mn>8</mn></mtd></mtr>"
    )


def test_table_list_of_list():
    table = Table(
        [[Number(1), Number(2), Number(3)], [Number(4), Number(5), Number(6)]]
    )
    assert (
        table._render_to_mathml()
        == "<mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd><mtd><mn>3</mn></mtd></mtr><mtr><mtd><mn>4</mn></mtd><mtd><mn>5</mn></mtd><mtd><mn>6</mn></mtd></mtr></mtable>"
    )


def test_table_align_at_equal():
    first_row = Tr(
        [
            Td([Identifier("x"), Operator("+"), Number(3)]),
            Td(Operator("=")),
            Td(Number(8)),
        ]
    )
    second_row = Tr([Td(Identifier("x")), Td(Operator("=")), Td(Number(5))])
    table = Table([first_row, second_row], columnalign="right middle left")
    assert (
        table._render_to_mathml()
        == '<mtable columnalign="right middle left"><mtr><mtd><mi>x</mi><mo>+</mo><mn>3</mn></mtd><mtd><mo>=</mo></mtd><mtd><mn>8</mn></mtd></mtr><mtr><mtd><mi>x</mi></mtd><mtd><mo>=</mo></mtd><mtd><mn>5</mn></mtd></mtr></mtable>'
    )
