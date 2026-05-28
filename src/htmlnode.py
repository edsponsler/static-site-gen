class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict[str, str] = None):
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
        