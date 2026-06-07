"""
This module establishes the preconditions for Markdown block processing.

By strictly parsing and classifying Markdown blocks into precise `BlockType` enumerations,
this module enforces a contract: any block returned and typed by these functions is
guaranteed to adhere to its defined structural invariant. This guarantees downstream
consumers (like `markdown.py`) can trust the classification and execute their parsing
logic without needing to perform redundant validation checks.
"""
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    # remove empty blocks and strips whitespace from each block
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.ULIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(block.split("\n"), 1)):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH