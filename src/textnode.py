from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None ):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
        return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node:TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nl = []
    for x in old_nodes:
        nl2 = []
        if x.text_type != TextType.TEXT:
            nl.append(x)
            continue
        tl = x.text.split(delimiter)
        if len(tl) % 2 == 0:
            raise ValueError("no matching delimeter for close")
        for y in range(0, len(tl)):
            if tl[y] == "":
                continue
            if y % 2 == 0:
                nl2.append(TextNode(tl[y], TextType.TEXT))
            else:
                nl2.append(TextNode(tl[y], text_type))
        nl.extend(nl2)
    return nl

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    nl = []
    for x in old_nodes:
        if x.text_type != TextType.TEXT:
            nl.append(x)
            continue
        text = x.text
        image = extract_markdown_images(text)
        if len(image) == 0:
            nl.append(x)
            continue
        for y in image:
            split = text.split(f"![{y[0]}]({y[1]})", 1)
            if len(split) != 2:
                raise ValueError("image not closed")
            if split[0] != "":
                nl.append(TextNode(split[0], TextType.TEXT))
            nl.append(TextNode(y[0], TextType.IMAGE, y[1]))
            text = split[1]
        if text != "":
            nl.append(TextNode(text, TextType.TEXT))
    return nl

def split_nodes_links(old_nodes):
    nl = []
    for x in old_nodes:
        if x.text_type != TextType.TEXT:
            nl.append(x)
            continue
        text = x.text
        link = extract_markdown_links(text)
        if len(link) == 0:
            nl.append(x)
            continue
        for y in link:
            split = text.split(f"[{y[0]}]({y[1]})", 1)
            if len(split) != 2:
                raise ValueError("link not closed")
            if split[0] != "":
                nl.append(TextNode(split[0], TextType.TEXT))
            nl.append(TextNode(y[0], TextType.LINK, y[1]))
            text = split[1]
        if text != "":
            nl.append(TextNode(text, TextType.TEXT))
    return nl

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes