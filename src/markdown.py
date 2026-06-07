"""
This module is responsible for parsing and rendering Markdown content into HTML Nodes.

It acts as a downstream consumer of the contract established by `blocks.py`. Because
`blocks.py` guarantees the strict preconditioning and type validation of each Markdown
block, this module can safely execute its domain-specific transformation logic (such as
stripping prefixes and parsing inline syntax) without performing redundant defensive
validation steps on the structure of the blocks themselves.
"""
import re
from blocks import BlockType, markdown_to_blocks, block_to_block_type
from nodes import text_to_textnodes
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown = sanitize_markdown(markdown)
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            child_nodes.append(block_to_html_node_paragraph(block))
        elif block_type == BlockType.CODE:
            child_nodes.append(block_to_html_node_code(block))
        elif block_type == BlockType.HEADING:
            child_nodes.append(block_to_html_node_heading(block))
        elif block_type == BlockType.QUOTE:
            child_nodes.append(block_to_html_node_quote(block))
        elif block_type == BlockType.ULIST:
            child_nodes.append(block_to_html_node_ulist(block))
        elif block_type == BlockType.OLIST:
            child_nodes.append(block_to_html_node_olist(block))
        else:
            raise ValueError(f"Invalid block type: {block_type}")

    return ParentNode("div", child_nodes)

def sanitize_markdown(markdown: str) -> str:
    """Strips bold formatting from around and inside links/images."""
    # Strip ** from outside standard links: **[link](url)** -> [link](url)
    markdown = re.sub(r'\*\*\[(.*?)\]\((.*?)\)\*\*', r'[\1](\2)', markdown)
    # Strip ** from outside image links: **![image](url)** -> ![image](url)
    markdown = re.sub(r'\*\*!\[(.*?)\]\((.*?)\)\*\*', r'![\1](\2)', markdown)
    
    # Strip ** from inside standard links: [**link**](url) -> [link](url)
    markdown = re.sub(r'\[\*\*(.*?)\*\*\]\((.*?)\)', r'[\1](\2)', markdown)
    # Strip ** from inside image links: ![**image**](url) -> ![image](url)
    markdown = re.sub(r'!\[\*\*(.*?)\*\*\]\((.*?)\)', r'![\1](\2)', markdown)
    
    return markdown

def block_to_html_node_paragraph(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)

def block_to_html_node_heading(block: str) -> HTMLNode:
    levels, heading_text = block.split(" ", 1)
    level = len(levels)    
    children = text_to_children(heading_text)
    return ParentNode(f"h{level}", children)

def block_to_html_node_quote(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:        
        new_lines.append(line.lstrip(">").strip())
    quote_text = " ".join(new_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)

def block_to_html_node_ulist(block: str) -> HTMLNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        _, list_item_text = line.split(" ", 1)
        children = text_to_children(list_item_text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)    

def block_to_html_node_olist(block: str) -> HTMLNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        _, list_item_text = line.split(" ", 1)
        children = text_to_children(list_item_text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def block_to_html_node_code(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code_node])

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
    