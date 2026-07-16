import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestInLineMarkdown(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is text with a ", TextType.TEXT),
                             TextNode("code block", TextType.CODE),
                             TextNode(" word", TextType.TEXT)
                         ]
                         )
        
    def test_split_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is text with a ", TextType.TEXT),
                             TextNode("bold block", TextType.BOLD),
                             TextNode(" word", TextType.TEXT)
                         ]
                         )
        
    def test_split_multiple_bold(self):
        node = TextNode("This is *text* with two *italic* words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is ", TextType.TEXT),
                             TextNode("text", TextType.ITALIC),
                             TextNode(" with two ", TextType.TEXT),
                             TextNode("italic", TextType.ITALIC),
                             TextNode(" words", TextType.TEXT),
                         ]
                         )
    
    def test_split_no_closing_delimiter(self):
        node = TextNode("This is text with a **bold block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)  