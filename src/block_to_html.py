from block_markdown import block_to_block_type, BlockType, markdown_to_blocks
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes

# BEST CODE BY PRATHAM, EFFICIENT SMALL AND COOL
# def markdown_to_html_node(markdown):
#     # Split the markdown into blocks (you already have a function for this)
#     blocks = markdown_to_blocks(markdown)
#     list_of_block_nodes = []
#     # Loop over each block:
#     for block in blocks:
#         # Determine the type of block (you already have a function for this)
#         blocktype = block_to_block_type(block)
#         # Based on the type of block, create a new HTMLNode with the proper data
#         if blocktype == BlockType.HEADING:
#             block_node = ParentNode("h" + str(block.count("#")), text_to_children(block.strip("# ")))
#         elif blocktype == BlockType.CODE:
#             block_text_node = TextNode((block.strip("```"))[1:], TextType.CODE)
#             code_block_node = text_node_to_html_node(block_text_node)
#             block_node = ParentNode("pre", [code_block_node])
#         elif blocktype == BlockType.QUOTE:
#             list_items_node_list = []
#             for line in block.split("\n"):
#                 list_items_node_list.append(line.lstrip(">").strip())
#             block_node = ParentNode("blockquote", text_to_children(" ".join(list_items_node_list)))
#         elif blocktype == BlockType.OLIST:
#             list_items_node_list = []
#             for line in block.split("\n"):
#                 list_items_node_list.append(ParentNode("li", text_to_children(line.strip("- "))))
#             block_node = ParentNode("ol", list_items_node_list)
#         elif blocktype == BlockType.ULIST:
#             list_items_node_list = []
#             for line in block.split("\n"):
#                 list_items_node_list.append(ParentNode("li", text_to_children(line[3:].strip())))
#             block_node = ParentNode("ul", list_items_node_list)
#         elif blocktype == BlockType.PARAGRAPH:
#             paragraph_text = " ".join(block.split("\n"))
#             block_node = ParentNode("p", text_to_children(paragraph_text))
#         # Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
#         list_of_block_nodes.append(block_node)
#         # The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.

#     # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
#     parent_node = ParentNode("div", list_of_block_nodes)
#     return parent_node

# def text_to_children(text):
#     textnodes = text_to_textnodes(text)
#     return [text_node_to_html_node(textnode) for textnode in textnodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
