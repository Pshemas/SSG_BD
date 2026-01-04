from copystatic import replace_directory_tree
from textnode import *
from markdown_to_html import generate_pages
from pathlib import Path
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    content_source_dir = Path("content/")
    generated_target_dir = Path("docs/")
    page_template_filepath = Path("template.html")
    replace_directory_tree(destination=generated_target_dir)
    # generate_page(page_source_path, page_template_path, page_target_path)
    generate_pages(
        content_source_dir, page_template_filepath, generated_target_dir, basepath
    )


if __name__ == "__main__":
    main()
