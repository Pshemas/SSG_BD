import unittest
from markdown_blocks import *


class TestSplitMarkdownBlocks(unittest.TestCase):
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


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        md = "# This is regular heading."
        self.assertEqual(BlockType.HEADING, block_to_block_type(md))

    def test_heading_negative(self):
        md = "This is not a heading."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

    def test_code(self):
        md = "```This is code.```"
        self.assertEqual(BlockType.CODE, block_to_block_type(md))

    def test_quote(self):
        md = ">This is a quote."
        self.assertEqual(BlockType.QUOTE, block_to_block_type(md))

    def test_unordered_list(self):
        md = "- item\n- another\n- one more"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(md))

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. Third"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(md))

    def test_not_ordered_list(self):
        md = "1. first\n5. second\n3. Third"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))


if __name__ == "__main__":
    unittest.main()
