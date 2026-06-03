import unittest
from blocks import BlockType, block_to_block_type, markdown_to_blocks

class TestBlocks(unittest.TestCase):
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

    def test_split_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_split_blocks_only_whitespace(self):
        md = "   \n   \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_split_blocks_leading_and_trailing_whitespace(self):
        md = "   This is a paragraph   \n\nThis is another paragraph   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph", "This is another paragraph"])

    def test_block_to_block_type(self):
        # Headings (1 to 6 hashes followed by space)
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Invalid headings (should be paragraphs)
        self.assertEqual(block_to_block_type("#HeadingNoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("######HeadingNoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("######"), BlockType.PARAGRAPH)

        # Other types
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("code\n```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> quote line 1\n> quote line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">quote line 1\n> quote line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> quote line 1\nquote line 2 without greater than"), BlockType.PARAGRAPH)        
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)