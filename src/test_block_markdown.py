import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )

    def test_block_to_block_types(self):
        # Test Headings
        self.assertEqual(block_to_block_type("# This is a H1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### This is a H3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### This is invalid"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

        # Test Code Blocks
        self.assertEqual(block_to_block_type("```\nThis is a code\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("``This is a invalid``"), BlockType.PARAGRAPH)

        # Test Quotes
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Quote 1 \n> Quote 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Quote with no space"), BlockType.QUOTE)

        # Test Unordered Lists
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-This list is invalid"), BlockType.PARAGRAPH)

        # Test Ordered Lists
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 3 (Broken Sequence)"), BlockType.PARAGRAPH)

        # Test Paragraph normal
        self.assertEqual(block_to_block_type("This is just a paragraph"), BlockType.PARAGRAPH)