import os
import sys
from copystatic import copystatic
from page_gen import generate_pages_recursive

cont_path = "./content"
temp_path = "./template.html"
dest_path = "./docs"

Basepath = sys.argv[1]

def main():
    copystatic(os.path.abspath('static'),  dest_path)
    generate_pages_recursive(cont_path, temp_path, dest_path, Basepath)


main()