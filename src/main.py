from copystatic import replace_directory_tree
from textnode import *
from markdown_to_html import generate_page
from pathlib import Path


def main():
    page_source_path = Path("content/index.md")
    page_target_path = Path("public/index.html")
    page_template_path = Path("template.html")
    replace_directory_tree()
    generate_page(page_source_path, page_template_path, page_target_path)


if __name__ == "__main__":
    main()
