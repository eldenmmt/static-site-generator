from enum import Enum

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")

    blocks = []
    
    for block in raw_blocks:
        block = block.strip()

        if block:
            blocks.append(block)
    return blocks

def block_to_block_type(block):

    parts = block.split(" ", 1)
    if len(parts) > 1:
        prefix = parts[0]
        if 1 <= len(prefix) <= 6 and prefix == "#" * len(prefix):
            return BlockType.HEADING
        
    if len(block) >= 6:
        if block.startswith("```") and block.endswith("```"):
            return BlockType.CODE
        
    lines = block.split("\n")
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
        i += 1
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children

def paragraph_to_html_node(block):
    paragraph_text = block.split("\n")
    paragraph_text = " ".join(paragraph_text)
    children = text_to_children(paragraph_text)

    return ParentNode("p", children)

def heading_to_html_node(block):
    parts = block.split(" ", 1)
    prefix = parts[0]
    text = parts[1]
    level = len(prefix)
    children = text_to_children(text)

    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    code_text = block[3:-3].strip("\n")
    text_node = TextNode(code_text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        elif line.startswith(">"):
            cleaned_lines.append(line[1:])
        else:
            cleaned_lines.append(line)
            
    quote_text = " ".join(cleaned_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        cleaned_line = line[2:]
        children = text_to_children(cleaned_line)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        parts = line.split(" ", 1)
        cleaned_line = ""
        if len(parts) > 1:
            cleaned_line = parts[1]
        children = text_to_children(cleaned_line)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        else:
            raise ValueError(f"Tipo de bloco inválido: {block_type}")
            
        block_nodes.append(node)
    return ParentNode("div", block_nodes)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("# "):
            parts = stripped_line.split(" ", 1)
            return parts[1].strip()
    
    raise Exception("H1 title not found")