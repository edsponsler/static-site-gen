# pyrefly: ignore [missing-import]
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_html_prop_to_html(self):
        node = HTMLNode("p", "Hello World", props={"class": "my-class"})
        self.assertEqual(node._prop_to_html(), "class=\"my-class\"")

    def test_html_prop_to_html_multiple(self):
        node = HTMLNode("p", "Hello World", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node._prop_to_html(), "class=\"my-class\" id=\"my-id\"")

    def test_html_prop_to_html_none(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node._prop_to_html(), "")

    def test_html_repr(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node.__repr__(), "HTMLNode(p, Hello World, None, None)")

    def test_html_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello World")
        with self.assertRaises(NotImplementedError):
            node.to_html()

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

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_repr(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.__repr__(), "LeafNode(p, Hello World, None)")
    
class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Hello"), LeafNode("i", "World")])
        self.assertEqual(node.to_html(), "<p><b>Hello</b><i>World</i></p>")
    
    def test_parent_to_html_with_props(self):
        node = ParentNode("p", [LeafNode("b", "Hello"), LeafNode("i", "World")], props={"class": "my-class"})
        self.assertEqual(node.to_html(), "<p class=\"my-class\"><b>Hello</b><i>World</i></p>")
    
    def test_parent_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Hello"), LeafNode("i", "World")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_parent_to_html_nested(self):
        node = ParentNode("p", [LeafNode("b", "Hello"), ParentNode("i", [LeafNode("u", "World")])])
        self.assertEqual(node.to_html(), "<p><b>Hello</b><i><u>World</u></i></p>")

    def test_parent_to_html_nested_with_props(self):
        node = ParentNode("div", [LeafNode("p", "Hello"), ParentNode("span", [LeafNode("b", "World")], props={"class": "my-class"})])
        self.assertEqual(node.to_html(), "<div><p>Hello</p><span class=\"my-class\"><b>World</b></span></div>")

    def test_parent_with_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_parent_with_empty_props(self):
        node = ParentNode("div", [LeafNode("p", "Hello World")], props={})
        self.assertEqual(node.to_html(), "<div><p>Hello World</p></div>")

    def test_parent_with_empty_props_and_empty_children(self):
        node = ParentNode("div", [], props={})
        self.assertEqual(node.to_html(), "<div></div>")

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("p", "Paragraph 1"),
            LeafNode("p", "Paragraph 2"),
        ])
        self.assertEqual(
            node.to_html(),
            "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>",
        )    

    def test_parent_repr(self):
        node = ParentNode("p", [LeafNode("b", "Hello"), LeafNode("i", "World")])
        self.assertEqual(node.__repr__(), "ParentNode(p, [LeafNode(b, Hello, None), LeafNode(i, World, None)], None)")
        

if __name__ == "__main__":
    unittest.main()
