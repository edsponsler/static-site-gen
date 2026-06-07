"""
Provides utilities to generate HTML pages from Markdown content.

Note: This module, alongside `copystatic.py`, exposes the core functionalities 
orchestrated by the `main.py` entrypoint to build the static site.
"""
import os
from markdown import markdown_to_html_node

def generate_page(from_path: str, to_path: str, template_path: str) -> None:
    """
    Generates an HTML page from a markdown file using a template file.
    
    Args:
        from_path: Path to the source markdown file.
        to_path: Path where the generated HTML file will be saved.
        template_path: Path to the HTML template file.
    """
    print(f"Generating page from {from_path} to {to_path} using template {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)
    html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)    
    dest_dir = os.path.dirname(to_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(to_path, "w") as f:
        f.write(html_page)

def extract_title(markdown_string: str) -> str:
    """
    Extracts the title from a Markdown string.
    
    Args:
        markdown_string: The Markdown string.
        
    Returns:
        The title of the Markdown string.
    """
    lines = markdown_string.split("\n")
    for line in lines:
        if line.startswith("# "):  
            return line[2:]
    raise ValueError("Title not found in Markdown string.")
