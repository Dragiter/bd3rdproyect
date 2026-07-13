def markdown_to_blocks(markdown):
    split_list = []
    block = markdown.split("\n\n")
    for x in block:
        if x == "":
            continue
        x = x.strip()
        split_list.append(x)
    return split_list