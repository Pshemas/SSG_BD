from markdown_blocks import *
from markdown_ops import *
from htmlnode import *
from textnode import *
from pathlib import Path
from loguru import logger


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    logger.info(
        f"Generating page from {from_path} to {dest_path} using {template_path}."
    )
    if not from_path.exists():
        raise ValueError("Source path not found.")
    with open(from_path) as source_file:
        md = source_file.read()

    if not template_path.exists():
        raise ValueError("Template path not found.")
    with open(template_path) as template_file:
        template = template_file.read()

    html_from_md = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    final_page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_from_md
    )

    dest_path.parent.mkdir(exist_ok=True, parents=True)
    dest_path.write_text(final_page)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    master_htmlnode = ParentNode("div", children=[])
    tags = {
        BlockType.PARAGRAPH: "p",
        BlockType.HEADING: "h",
        BlockType.CODEBLOCK: "pre",
        BlockType.QUOTE: "blockquote",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.ORDERED_LIST: "ol",
    }

    for block in blocks:
        blocktype = block_to_block_type(block)
        new_html_node = ParentNode(tags[blocktype], children=[])
        if blocktype == BlockType.QUOTE:
            quote_lines = block.split()
            cleaned_lines = []
            for line in quote_lines:
                cleaned_line = line.lstrip(">").rstrip()
                if cleaned_line:
                    cleaned_lines.append(cleaned_line)
            print(cleaned_lines)
            cleaned_block = " ".join(cleaned_lines)
            children_html_nodes = [LeafNode(None, cleaned_block)]
        elif blocktype == BlockType.CODEBLOCK:
            block = block.replace("```", "")
            children_html_nodes = [LeafNode("code", block)]
        elif blocktype == BlockType.UNORDERED_LIST:
            list_lines = block.split("\n")
            children_html_nodes = []
            for line in list_lines:
                line_nodes = text_to_textnodes(line.strip("- "))
                html_nodes = [text_node_to_html_node(node) for node in line_nodes]
                children_html_nodes.append(ParentNode("li", html_nodes))
        elif blocktype == BlockType.ORDERED_LIST:
            list_lines = block.split("\n")
            children_html_nodes = []
            for line in list_lines:
                list_nodes = text_to_textnodes(line.split(". ", maxsplit=1)[1])
                html_nodes = [text_node_to_html_node(node) for node in list_nodes]
                children_html_nodes.append(ParentNode("li", html_nodes))
        elif blocktype == BlockType.HEADING:
            children_html_nodes = []
            heading_type = 0
            for char in block:
                if char == "#":
                    heading_type += 1
                else:
                    break
            if heading_type + 1 >= len(block):
                raise ValueError("Missing text content after heading tag")
            content = block[heading_type + 1 :]
            new_html_node.tag = f"h{heading_type}"
            children_html_nodes.append(LeafNode(None, content))

        else:
            children_text_nodes = text_to_textnodes(block)
            children_html_nodes = [
                text_node_to_html_node(node) for node in children_text_nodes
            ]

        new_html_node.children.extend(children_html_nodes)
        master_htmlnode.children.append(new_html_node)
    return master_htmlnode
