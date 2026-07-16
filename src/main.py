import os
from copystatic import copystatic

def main():
    copystatic(os.path.abspath('static'),  os.path.abspath('public'))



main()