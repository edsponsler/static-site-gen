class HTMLNode:
    """
    Base class representing a node in an HTML document tree.
    
    This class defines the foundational structure for an HTML element, 
    including its tag, inner value, nested children, and attributes. 
    While not typically instantiated directly, its subclasses (`LeafNode` 
    and `ParentNode`) are heavily utilized and instantiated by the `markdown.py` 
    and `textnode.py` modules during the parsing process.
    """
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented for HTMLNode")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
    Represents an HTML node that contains no children.
    
    Leaf nodes represent the innermost elements of the HTML tree (e.g., raw text, 
    `<a>`, `<img>`, `<b>` tags). Objects of this type are primarily instantiated 
    by `text_node_to_html_node` in `textnode.py` and inline parsing functions 
    within `markdown.py`.
    """
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    """
    Represents an HTML node that contains nested child nodes.
    
    Parent nodes act as structural containers (e.g., `<div>`, `<ul>`, `<blockquote>`) 
    and dictate the nested hierarchy of the HTML tree. Objects of this type are 
    primarily instantiated by the block-level parser functions in `markdown.py`.
    """
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        child_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"