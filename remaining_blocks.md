# Guide to Implementing the Remaining Markdown Block Types

This document serves as a reference for implementing the remaining `BlockType` logic in `markdown_to_html_node`.

### 1. Heading Blocks (`BlockType.HEADING`)
*   **Tag Determination:** Count the number of `#` characters prefixing the block (e.g., `##` means level 2). The HTML tag will be `f"h{level}"` (`h1` through `h6`).
*   **Clean Text:** Strip the leading `#` characters and the single space that follows it.
*   **Create Node:** Pass the cleaned text through `text_to_children(text)`. Return a `ParentNode` with your computed `h*` tag, passing in those parsed children.

### 2. Quote Blocks (`BlockType.QUOTE`)
*   **Clean Text:** Since every line in a quote block is prefixed with `> `, you'll want to split the block by `\n` to iterate through the lines. For each line, strip the `> ` prefix.
*   **Reconstruct Text:** Join the cleaned lines back together (usually with a space or a newline, depending on your preferred spacing) to form a single string.
*   **Create Node:** Pass the string to `text_to_children()` and wrap the returned list of children in a single `ParentNode` using the `blockquote` tag.

### 3. Unordered Lists (`BlockType.ULIST`)
*   **Process Items:** Split the block by `\n` to isolate each list item.
*   **Clean and Parse each Item:** For every line, strip the leading `- ` or `* `. Pass the remaining text of the item into `text_to_children()`.
*   **Create Node (Nested):** First, take the children from `text_to_children()` and wrap them in a `ParentNode` with the `li` tag. Collect all of these `li` parent nodes into a list.
*   **Wrap the List:** Wrap that entire list of `li` nodes inside an overarching `ParentNode` with the `ul` tag.

### 4. Ordered Lists (`BlockType.OLIST`)
*   **Process Items:** Split the block by `\n` to grab each list item.
*   **Clean and Parse each Item:** For every line, strip the leading number, dot, and space (e.g., `1. ` or `10. `). An easy way to do this is to strip the text starting from the first space. Pass the remaining text into `text_to_children()`.
*   **Create Node (Nested):** Just like unordered lists, wrap the parsed children for each item in a `ParentNode` with the `li` tag, and collect them into a list.
*   **Wrap the List:** Wrap your list of `li` nodes inside a single `ParentNode` with the `ol` tag.
