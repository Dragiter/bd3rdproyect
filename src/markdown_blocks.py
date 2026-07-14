from enum import Enum


def markdown_to_blocks(markdown):
    split_list = []
    block = markdown.split("\n\n")
    for x in block:
        if x == "":
            continue
        x = x.strip()
        split_list.append(x)
    return split_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block) ->BlockType:
    lines = block.split("\n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for x in lines:
            if not x.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for x in lines:
            if not x.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        x = 1
        for y in lines:
            if not y.startswith(f"{x}. "):
                return BlockType.PARAGRAPH
            x += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH