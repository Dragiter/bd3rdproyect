from markdown_blocks import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print("Generating page from from_path to dest_path using template_path")
    
    from_file = open(from_path, "r")
    mrkd = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    HTML_string = markdown_to_html_node(mrkd).to_html()
    ext_title = extract_title(mrkd)
    template = template.replace("{{ Title }}", ext_title)
    template = template.replace("{{ Content }}", HTML_string)

    if os.path.exists(os.path.dirname(dest_path)):
        to_file = open(dest_path, "w")
        to_file.write(template)
    else:
        os.makedirs(dest_path)
        to_file = open(dest_path, "w")
        to_file.write(template)
