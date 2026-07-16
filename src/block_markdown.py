from enum import Enum

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