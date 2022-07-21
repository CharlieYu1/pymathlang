from abc import abstractmethod
from typing import List, Union


def _pad_braces(string: str):
    return "{" + string + "}"


class Element(object):
    tag_name = None
    latex_tag_name = None

    def __init__(self, element):
        self._element = element

    def _render_to_mathml(self):
        cls = self.__class__
        return f"<{cls.tag_name}>{self._element}</{cls.tag_name}>"

    def _render_to_latex(self):
        cls = self.__class__
        if cls.latex_tag_name:
            return "\\{}{{{}}}".format(cls.latex_tag_name, self._element())
        return f"{self._element}"


class Identifier(Element):
    tag_name = "mi"


class Operator(Element):
    tag_name = "mo"


class Number(Element):
    tag_name = "mn"


class Text(Element):
    tag_name = "mtext"
    latex_tag_name = "textnormal"


class ElementList(object):
    tag_name = None
    latex_tag_name = None

    def __init__(self, elements: Union[List[Element], Element]):
        if isinstance(elements, Element):
            elements = [elements]
        self._elements = elements

    def append(self, element: Element):
        self._elements.append(element)

    def _render_to_mathml(self):
        cls = self.__class__
        rendered_elements = [element._render_to_mathml() for element in self._elements]
        return f'<{cls.tag_name}>{"".join(rendered_elements)}</{cls.tag_name}>'

    def _render_to_latex(self, braces=False):
        cls = self.__class__
        if braces:
            rendered_elements = [
                _pad_braces(element._render_to_latex()) for element in self._elements
            ]
        else:
            rendered_elements = [
                element._render_to_latex() for element in self._elements
            ]
        if cls.latex_tag_name:
            print(cls.latex_tag_name)
            if not braces:
                return (
                    "\\{}".format(cls.latex_tag_name)
                    + f'{_pad_braces("".join(rendered_elements))}'
                )
            else:
                return (
                    "\\{}".format(cls.latex_tag_name) + f'{"".join(rendered_elements)}'
                )
        return f'{"".join(rendered_elements)}'


class ElementListOfLengthTwo(ElementList):
    def __init__(self, _elements):
        super().__init__(_elements)
        if len(self._elements) != 2:
            raise Exception("The number of provided elements must be 2")

    def _render_to_latex(self):
        return super()._render_to_latex(braces=True)


class ElementListOfLengthThree(ElementList):
    def __init__(self, _elements):
        super().__init__(_elements)
        if len(self._elements) != 3:
            raise Exception("The number of provided elements must be 3")

    def _render_to_latex(self):
        return super()._render_to_latex(braces=True)


class Row(ElementList):
    tag_name = "mrow"


class Fraction(ElementListOfLengthTwo):
    tag_name = "mfrac"
    latex_tag_name = "frac"


class Subscript(ElementListOfLengthTwo):
    tag_name = "msub"

    def _render_to_latex(self):
        first, second = self._elements
        first_rendered = first._render_to_latex()
        second_rendered = second._render_to_latex()
        if len(first_rendered) > 1:
            first_rendered = _pad_braces(first_rendered)
        if len(second_rendered) > 1:
            second_rendered = _pad_braces(second_rendered)
        return f"{first_rendered}_{second_rendered}"


class Superscript(ElementListOfLengthTwo):
    tag_name = "msup"

    def _render_to_latex(self):
        first, second = self._elements
        first_rendered = first._render_to_latex()
        second_rendered = second._render_to_latex()
        if len(first_rendered) > 1:
            first_rendered = _pad_braces(first_rendered)
        if len(second_rendered) > 1:
            second_rendered = _pad_braces(second_rendered)
        return f"{first_rendered}^{second_rendered}"


class SubSuperscript(ElementListOfLengthThree):
    tag_name = "msubsup"

    def _render_to_latex(self):
        first, second, third = self._elements
        first_rendered = first._render_to_latex()
        second_rendered = second._render_to_latex()
        third_rendered = third._render_to_latex()
        if len(first_rendered) > 1:
            first_rendered = _pad_braces(first_rendered)
        if len(second_rendered) > 1:
            second_rendered = _pad_braces(second_rendered)
        if len(third_rendered) > 1:
            third_rendered = _pad_braces(third_rendered)
        return f"{first_rendered}_{second_rendered}^{third_rendered}"


class Sqrt(ElementList):
    tag_name = "msqrt"
    latex_tag_name = "sqrt"


e = Identifier("x")
print(e._render_to_latex())

e = Row([Identifier("x"), Operator("+"), Number(2)])
print(e._render_to_mathml())

e = Sqrt(Identifier("ab"))
print(e._render_to_mathml())
print(e._render_to_latex())

e = Fraction([Identifier("x"), Number(2)])
print(e._render_to_latex())
