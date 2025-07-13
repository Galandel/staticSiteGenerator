from textnode import TextType, TextNode

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