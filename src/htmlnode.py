

class HTMLNode():
    def __init__(self, 
                 tag: str | None = None, 
                 value: str | None = None, 
                 children: list | None = None, 
                 props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is not None:
            prop_str = ""
            for key, value in self.props.items():
                prop_str += f' {key}="{value}"'
            return prop_str
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
                

class LeafNode(HTMLNode):
    def __init__(self, 
                 tag: str | None, 
                 value: str,  
                 props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
