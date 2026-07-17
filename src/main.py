import os
from copystatic import copystatic
from page_gen import generate_page

cont_path = "./content"
temp_path = "./template.html"
dest_path = "./public"

def main():
    copystatic(os.path.abspath('static'),  dest_path)
    generate_page(os.path.join(cont_path, "index.md"), temp_path, os.path.join(dest_path, "index.html"))


main()