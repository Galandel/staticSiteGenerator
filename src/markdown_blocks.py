

def markdown_to_blocks(markdown):
    return_blocks = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        if block == "":
            continue
        return_blocks.append(block.strip())
    return return_blocks
