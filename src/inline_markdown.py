from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
    
        elif old_node.text_type == TextType.TEXT:
            split_node = old_node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise ValueError("Invalid Markdown sintax: missing closing delimiter")

            for i in range(len(split_node)):
                if split_node[i] != "":
                    if i % 2 == 0:
                        node = TextNode(split_node[i], TextType.TEXT)
                    else:
                        node = TextNode(split_node[i], text_type)
                    new_nodes.append(node)
    return new_nodes