import unittest
from textnode import TextNode, TextType
from nodes import split_nodes_on_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_multiple_delimiters(self):
        node = TextNode("This is **bold** and **bold again** word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold again", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_unclosed_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_on_delimiter([node], "`", TextType.CODE)

    def test_split_multiple_nodes(self):
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        node2 = TextNode("Already formatted", TextType.BOLD)
        node3 = TextNode("Normal text", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("Already formatted", TextType.BOLD),
                TextNode("Normal text", TextType.TEXT),
            ]
        )

if __name__ == "__main__":
    unittest.main()
