from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        if old_node.text_type == TextType.TEXT:
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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text_type == TextType.TEXT:
            current_text = old_node.text

            images = extract_markdown_images(current_text)
            if not images:
                new_nodes.append(old_node)
                continue

            if images:
                for image_alt, image_link in images:
                    image_markdown = f"![{image_alt}]({image_link})"

                    parts = current_text.split(image_markdown, 1)

                    if len(parts) != 2:
                        raise ValueError("Invalid markdown, image section not closed")

                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

                    current_text = parts[1]

                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text_type == TextType.TEXT:
            current_text = old_node.text

            images = extract_markdown_links(current_text)
            if not images:
                new_nodes.append(old_node)
                continue

            if images:
                for link_text, link_url in images:
                    image_markdown = f"[{link_text}]({link_url})"

                    parts = current_text.split(image_markdown, 1)

                    if len(parts) != 2:
                        raise ValueError("Invalid markdown, image section not closed")

                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

                    current_text = parts[1]

                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes