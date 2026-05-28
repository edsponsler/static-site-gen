# pyrefly: ignore [missing-import]
import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode("p", "Hello World", props={"class": "my-class"})
        self.assertEqual(node._prop_to_html(), "class=\"my-class\"")

    def test_prop_to_html_multiple(self):
        node = HTMLNode("p", "Hello World", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node._prop_to_html(), "class=\"my-class\" id=\"my-id\"")

    def test_prop_to_html_none(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node._prop_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node.__repr__(), "HTMLNode(p, Hello World, None, None)")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello World", props={"class": "my-class"})
        self.assertEqual(node.to_html(), "<p class=\"my-class\">Hello World</p>")
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")
    
    def test_leaf_repr(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.__repr__(), "LeafNode(p, Hello World, None)")

if __name__ == "__main__":
    unittest.main()
