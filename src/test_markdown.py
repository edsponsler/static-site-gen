import unittest
from markdown import markdown_to_html_node

class TestMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

### Heading 3 with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3 with <b>bold</b> text</h3></div>",
        )

    def test_quotes(self):
        md = """
>This is a quote
>with multiple lines
>and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_lists(self):
        md = """
- This is a list item
- This is another list item with **bold**
- And a third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list item</li><li>This is another list item with <b>bold</b></li><li>And a third item</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """
1. First item
2. Second item
3. Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item with <code>code</code></li></ol></div>",
        )
