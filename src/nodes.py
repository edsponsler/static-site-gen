import re
from textnode import TextNode, TextType

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_image(nodes)    
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)        
    nodes = split_nodes_on_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_on_delimiter(nodes, "`", TextType.CODE)
    return nodes

def split_nodes_on_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: delimiter '{delimiter}' not closed in text: '{node.text}'")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for image in images:
            alt, url = image
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image not found in text")
            before, after = sections
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(
                TextNode(
                    alt,
                    TextType.IMAGE,
                    url,
                )
            )
            remaining_text = after
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        for link in links:
            alt, url = link
            sections = remaining_text.split(f"[{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not found in text")
            before, after = sections
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(
                TextNode(
                    alt,
                    TextType.LINK,
                    url,
                )
            )
            remaining_text = after
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
