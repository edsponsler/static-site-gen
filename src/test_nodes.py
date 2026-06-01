import unittest
from textnode import TextNode, TextType
from nodes import (
    split_nodes_on_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)

class TestSplitNodes(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
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
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_on_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    
    def test_split_multiple_delimiters(self):
        node = TextNode("This is **bold** and **bold again** word", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold again", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_multiple_nodes(self):
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        node2 = TextNode("Already formatted", TextType.BOLD)
        node3 = TextNode("Normal text", TextType.TEXT)
        new_nodes = split_nodes_on_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("Already formatted", TextType.BOLD),
                TextNode("Normal text", TextType.TEXT),
            ]
        )

    def test_split_unclosed_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_on_delimiter([node], "`", TextType.CODE)

class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_extract_markdown_images_simple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![image](https://www.google.com) ![alt text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://www.google.com"),
                ("alt text", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )
    
    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_mixed_content(self):
        matches = extract_markdown_images("This is text with an ![alt text](image.jpg) image and ![alt text](image.jpg) another image")
        self.assertListEqual(
            [("alt text", "image.jpg"), ("alt text", "image.jpg")],
            matches,
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    
    def test_extract_markdown_links_simple(self):
        matches = extract_markdown_links("[alt text](image.jpg)")
        self.assertListEqual([("alt text", "image.jpg")], matches)
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links("[alt text](image.jpg)[alt text](image.jpg)")
        self.assertListEqual([("alt text", "image.jpg"), ("alt text", "image.jpg")], matches)
    
    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_mixed_content(self):
        matches = extract_markdown_links("This is text with an [alt text](image.jpg) link and [alt text](image.jpg) another link")
        self.assertListEqual([("alt text", "image.jpg"), ("alt text", "image.jpg")], matches)

if __name__ == "__main__":
    unittest.main()
