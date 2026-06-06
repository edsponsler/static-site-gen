from htmlnode import HTMLNode, ParentNode
from blocks import BlockType, markdown_to_blocks, block_to_block_type
from nodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_html_node_paragraph(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)

def block_to_html_node_code(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code_node])


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            child_nodes.append(block_to_html_node_paragraph(block))
        elif block_type == BlockType.CODE:
            child_nodes.append(block_to_html_node_code(block))
        else:
            raise ValueError(f"Invalid block type: {block_type}")

    return ParentNode("div", child_nodes)