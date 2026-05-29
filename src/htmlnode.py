class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, 
                 children: list[HTMLNode] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented for HTMLNode")
    
    def _prop_to_html(self) -> str:
        if self.props is None:
            return ""
        
        prop_strings = []
        for key, value in self.props.items():
            prop_strings.append(f'{key}="{value}"')
        
        return " ".join(prop_strings)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
                
        prop_string = self._prop_to_html()
        if prop_string:
            return f"<{self.tag} {prop_string}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        prop_string = self._prop_to_html()
        child_html = "".join(child.to_html() for child in self.children)
        
        if prop_string:
            return f"<{self.tag} {prop_string}>{child_html}</{self.tag}>"
        return f"<{self.tag}>{child_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"