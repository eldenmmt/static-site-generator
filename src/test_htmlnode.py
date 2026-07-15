import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(
            tag="a", 
            props={
                "href": "https://www.google.com"
                }
                )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode(
            tag="a",
            props={

            }
        )
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(
            tag="p", 
            value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            tag="a", 
            value="Hello, world!", 
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
            )
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Hello, world!</a>')

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(
            tag=None,
            value="Hello, raw text!"
        )
        self.assertEqual(node.to_html(), "Hello, raw text!")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_deeply_nested(self):
        node_b = LeafNode(
            tag="b",
            value="deep text"
        )
        node_span = ParentNode(
            tag="span",
            children=[node_b],
        )
        node_p = ParentNode(
            tag="p",
            children=[node_span],
        )
        node_div = ParentNode(
            tag="div",
            children=[node_p],
        )
        self.assertEqual(node_div.to_html(), '<div><p><span><b>deep text</b></span></p></div>')

    def test_to_html_mixed_children(self):
        text_1 = LeafNode(
            tag=None,
            value="Texto normal "
        )
        node_b = LeafNode(
            tag="b",
            value="negrito"
        )
        text_2 = LeafNode(
            tag=None,
            value=" e "
        )
        node_i = LeafNode(
            tag="i",
            value="itálico"
        )
        node_span = ParentNode(
            tag="span",
            children=[node_i]
        )
        text_3 = LeafNode(
            tag=None,
            value="."
        )
        node_p = ParentNode(
            tag="p",
            children=[text_1, node_b, text_2, node_span, text_3]
        )
        self.assertEqual(node_p.to_html(), '<p>Texto normal <b>negrito</b> e <span><i>itálico</i></span>.</p>')


    def test_to_html_no_tag_raises_error(self):
        text_1 = LeafNode(
            tag=None,
            value="Text"
        )
        node = ParentNode(
            tag=None, # type: ignore
            children=[text_1]
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises_error(self):
        node = ParentNode(
            tag="p",
            children=None # type: ignore
        )
        with self.assertRaises(ValueError):
            node.to_html()
