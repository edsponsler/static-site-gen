import unittest
from textnode import TextNode, TextType
from nodes import (
    split_nodes_on_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_simple(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )
    
    def test_split_nodes_image_multiple(self):
        node = TextNode("![image](https://www.google.com)![alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://www.google.com"),
                TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )
    
    def test_split_nodes_image_multiple_with_space(self):
        node = TextNode("![image](https://www.google.com) ![alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://www.google.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )
    
    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no images", TextType.TEXT),
            ],
        )
    
    def test_split_nodes_image_mixed_content(self):
        node = TextNode("This is text with an ![alt text](image.jpg) image and ![alt text](image.jpg) another image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image.jpg"),
                TextNode(" image and ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image.jpg"),
                TextNode(" another image", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_only(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_simple(self):
        node = TextNode("This is text with an [link](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
        )

    def test_split_nodes_link_multiple(self):
        node = TextNode("[link](https://www.google.com)[alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode("alt text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_nodes_link_multiple_with_space(self):
        node = TextNode("[link](https://www.google.com) [alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("alt text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_mixed_content(self):
        node = TextNode("This is text with an [alt text](image.jpg) link and [alt text](image.jpg) another link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("alt text", TextType.LINK, "image.jpg"),
                TextNode(" link and ", TextType.TEXT),
                TextNode("alt text", TextType.LINK, "image.jpg"),
                TextNode(" another link", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_only(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
        )

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_mixed(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_plain(self):
        text = "This is just plain text with no formatting."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is just plain text with no formatting.", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_all_markdown(self):
        text = "**bold**_italic_`code`![image](url)[link](url)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode("link", TextType.LINK, "url"),
            ]
        )

if __name__ == "__main__":
    unittest.main()
