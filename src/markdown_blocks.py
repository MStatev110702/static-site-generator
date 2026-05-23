from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH
    

def markdown_to_blocks(markdown):
    paragraphs = markdown.split('\n\n')
    blocks = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        blocks.append(paragraph)

    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                htmlnode = ParentNode(tag="p", children=text_to_children(block.replace("\n", " ")))
            case BlockType.HEADING:
                m = re.match(r"^(#{1,6})\s", block)
                header_count = len(m.group(1)) if m else 0
                htmlnode = ParentNode(tag=f"h{header_count}", children=text_to_children(re.sub(r"^(#{1,6})", "", block)))
            case BlockType.QUOTE:
                htmlnode = ParentNode(tag="blockquote", children=text_to_children(block.replace(">", "").rstrip()))
            case BlockType.ULIST:
                items = block.split("\n")
                children = []
                for item in items:
                    children.append(ParentNode(tag="li", children=text_to_children(item.replace("- ", ""))))
                htmlnode = ParentNode(tag="ul", children=children)
            case BlockType.OLIST:
                items = block.split("\n")
                children = []
                i = 1
                for item in items:
                    children.append(ParentNode(tag="li", children=text_to_children(item.replace(f"{i}. ", ""))))
                    i += 1
                htmlnode = ParentNode(tag="ol", children=children)
            case BlockType.CODE:
                block = block.replace("```", "", 1)
                block = "".join(block.rsplit("```", 1)).lstrip()
                text_node = TextNode(text=block, text_type=TextType.TEXT)
                child = ParentNode(tag="code", children=[text_node_to_html_node(text_node)])
                htmlnode = ParentNode(tag="pre", children=[child])
        htmlnodes.append(htmlnode)
    return ParentNode(tag="div", children=htmlnodes)
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children