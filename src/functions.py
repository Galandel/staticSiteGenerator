from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # print(f"DEBUG: old_node: {old_node}")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text.split(delimiter)
        # print(f"DEBUG: Text: {text}")
        if len(text) % 2 == 0:
            raise ValueError(f"Invalid Markdown, formatted section not closed")
        for i, segment in enumerate(text):
            if segment == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                new_nodes.append(TextNode(segment, text_type))
    # print(f"DEBUG: new_nodes: {new_nodes}")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image_alt, image_link in images:
            sections = node_text.split(f"![{image_alt}]({image_link})",1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link_text, link_url in links:
            sections = node_text.split(f"[{link_text}]({link_url})",1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

# original code keeping for historical purposes
# def text_to_textnodes(text):
#     nodes_with_bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
#     nodes_with_bold_italics = split_nodes_delimiter(nodes_with_bold, "_", TextType.ITALIC)
#     nodes_with_bold_italics_code = split_nodes_delimiter(nodes_with_bold_italics, "`", TextType.CODE)
#     nodes_with_bold_italics_code_links = split_nodes_link(nodes_with_bold_italics_code)
#     nodes_with_bold_italics_code_links_images = split_nodes_image(nodes_with_bold_italics_code_links)
#     return nodes_with_bold_italics_code_links_images

# chaining the text_to_textnodes function to declutter variable names
def text_to_textnodes(text):
    return split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD),
                    "_", TextType.ITALIC
                ),
                "`", TextType.CODE
            )
        )
    )

def extract_title(markdown):
    h1 = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith('#') and not line.startswith('##'):
            h1 = line.lstrip("# ")
    if not h1:
        raise Exception("Missing h1 header")
    return h1