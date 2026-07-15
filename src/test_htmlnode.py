import unittest
from htmlnode import HTMLNode, LeafNode

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