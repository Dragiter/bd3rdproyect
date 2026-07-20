from markdown_blocks import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path, Basepath):
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
    template = template.replace('href="/', f'href="{Basepath}')
    template = template.replace('src="/', f'src="{Basepath}')

    if os.path.exists(os.path.dirname(dest_path)):
        to_file = open(dest_path, "w")
        to_file.write(template)
    else:
        os.makedirs(dest_path)
        to_file = open(dest_path, "w")
        to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, Basepath):
    md_list = get_md_list(dir_path_content)
    for md in md_list:
        rel_path = os.path.relpath(md, dir_path_content)
        dest = os.path.join(dest_dir_path, rel_path.replace("index.md", "index.html"))
        os.makedirs(os.path.dirname(dest),0o777,True)
        generate_page(md, template_path, dest, Basepath)


def get_md_list(content_directory):
    rl = []
    for x in os.listdir(content_directory):
        current_path = os.path.join(content_directory, x)
        if x.endswith(".md"):
            rl.append(current_path)
        elif os.path.isdir(current_path):
            il = get_md_list(current_path)
            rl.extend(il)
    return rl
