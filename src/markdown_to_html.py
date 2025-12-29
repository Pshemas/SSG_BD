from markdown_blocks import *
from markdown_ops import *
from htmlnode import *
from textnode import *
import pprint


def markdown_to_html_node(markdown: str) -> ParentNode:
    pass


def test_conversion():
    md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

> quoted line first
> quoted line second
> quoted line third

"""
    blocks = markdown_to_blocks(md)
    master_htmlnode = ParentNode("div", children=[])
    tags = {
        BlockType.PARAGRAPH: "p",
        BlockType.HEADING: "h",
        BlockType.CODE: "code",
        BlockType.QUOTE: "blockquote",
    }

    pprint.pprint(blocks)

    for block in blocks:
        # bloki rozbic na inline node i stworzyć dla nich parent node
        new_html_node = ParentNode(tags[block_to_block_type(block)], [])
        children_text_nodes = text_to_textnodes(block)
        children_html_nodes = [
            text_node_to_html_node(node) for node in children_text_nodes
        ]

        new_html_node.children.extend(children_html_nodes)
        master_htmlnode.children.append(new_html_node)
    # cytaty mogą wymagać specjalnego traktowania - usunięcia > i dodania br?
    pprint.pprint(master_htmlnode)
    html = master_htmlnode.to_html()
    print(html)
    print(type(html))


if __name__ == "__main__":
    test_conversion()
