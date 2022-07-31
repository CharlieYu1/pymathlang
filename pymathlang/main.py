from abc import abstractmethod
from typing import List, Union


def _pad_braces(string: str):
    return "{" + string + "}"


def _combine_mrows(string: str):
    return string.replace("</mrow><mrow>", "")


class Element(object):
    tag_name = None
    latex_tag_name = None

    def __init__(self, element, **kwargs):
        self._element = element
        self.attributes = kwargs

    def __eq__(self, other: "Element"):
        return (self._element == other._element) and (
            self.attributes == other.attributes
        )

    def _render_to_mathml(self):
        cls = self.__class__
        html_attributes = "".join(
            [
                " " + key + "=" + '"' + self.attributes[key] + '"'
                for key in self.attributes
            ]
        )
        return f"<{cls.tag_name}{html_attributes}>{self._element}</{cls.tag_name}>"

    def _render_to_latex(self):
        cls = self.__class__
        if cls.latex_tag_name:
            return "\\{}{{{}}}".format(cls.latex_tag_name, self._element())
        return f"{self._element}"


class EmptyElement(Element):
    def __init__(self):
        self._element = None
        self.attributes = {}

    def _render_to_mathml(self):
        return ""

    def _render_to_latex(self):
        return ""


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

    def __init__(self, elements: Union[List[Element], Element], **kwargs):
        if isinstance(elements, list):
            self._elements = elements
        else:
            self._elements = [elements]
        self.attributes = kwargs

    def __eq__(self, other: "ElementList"):
        return (self._elements == other._elements) and (
            self.attributes == other.attributes
        )

    def append(self, element: Element):
        self._elements.append(element)

    def _render_to_mathml(self):
        cls = self.__class__
        rendered_elements = [element._render_to_mathml() for element in self._elements]
        html_attributes = "".join(
            [
                " " + key + "=" + '"' + self.attributes[key] + '"'
                for key in self.attributes
            ]
        )
        return f"<{cls.tag_name}{html_attributes}>{''.join(rendered_elements)}</{cls.tag_name}>"

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


class MathEnvironment(ElementList):
    tag_name = "math"

    def __init__(self, _elements, **kwargs):
        super().__init__(_elements, **kwargs)
        self.attributes["display"] = "block"

    def _render_to_latex(self, braces=False):
        return "\\[" + super()._render_to_latex(braces) + "\\]"


class InlineMathEnvironment(ElementList):
    tag_name = "math"

    def __init__(self, _elements, **kwargs):
        super().__init__(_elements, **kwargs)
        self.attributes["display"] = "inline"

    def _render_to_latex(self, braces=False):
        return "\\(" + super()._render_to_latex(braces) + "\\)"


class ElementListOfLengthTwo(ElementList):
    def __init__(self, _elements, **kwargs):
        super().__init__(_elements, **kwargs)
        if len(self._elements) != 2:
            raise Exception("The number of provided elements must be 2")

    def _render_to_latex(self):
        return super()._render_to_latex(braces=True)


class ElementListOfLengthThree(ElementList):
    def __init__(self, _elements, **kwargs):
        super().__init__(_elements, **kwargs)
        if len(self._elements) != 3:
            raise Exception("The number of provided elements must be 3")

    def _render_to_latex(self):
        return super()._render_to_latex(braces=True)


class Row(ElementList):
    tag_name = "mrow"


class RowWithParentheses(ElementList):
    tag_name = "mrow"

    def __init__(self, elements: Union[List[Element], Element], **kwargs):
        super().__init__(elements, **kwargs)
        self._elements = [Operator("(")] + self._elements + [Operator(")")]


class RowWithBrackets(ElementList):
    tag_name = "mrow"

    def __init__(self, elements: Union[List[Element], Element], **kwargs):
        super().__init__(elements, **kwargs)
        self._elements = [Operator("[")] + self._elements + [Operator("]")]


class Fraction(ElementListOfLengthTwo):
    tag_name = "mfrac"
    latex_tag_name = "frac"


class Over(ElementListOfLengthTwo):
    tag_name = "mover"

    def _render_to_latex(self):
        raise NotImplemented


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


class Td(ElementList):
    tag_name = "mtd"

    def _render_to_latex(self):
        raise NotImplemented


class Tr(ElementList):
    tag_name = "mtr"

    def __init__(self, _elements, **kwargs):
        print(_elements)
        super().__init__(_elements, **kwargs)
        for i, element in enumerate(self._elements):
            if not isinstance(element, Td):
                self._elements[i] = Td(element)

    def _render_to_latex(self):
        raise NotImplemented


class Table(ElementList):
    tag_name = "mtable"

    def __init__(self, _elements, **kwargs):
        super().__init__(_elements, **kwargs)
        for i, element in enumerate(self._elements):
            if not isinstance(element, Tr):
                self._elements[i] = Tr(element)

    def _render_to_latex(self):
        raise NotImplemented
