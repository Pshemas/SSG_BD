from textnode import TextType, TextNode
import re


def split_node(
    old_node: TextNode,
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    resulting_nodes = []
    if delimiter not in old_node.text:
        raise ValueError("Delimeter not found in node")
    text_sections = old_node.text.split(delimiter)
    if len(text_sections) % 2 == 0:
        raise ValueError("Error in markdown - formatted section not closed.")
    for idx, text in enumerate(text_sections):
        if idx % 2 and text:
            resulting_nodes.append(TextNode(text=text, text_type=text_type))
        else:
            if text:
                resulting_nodes.append(TextNode(text=text, text_type=TextType.TEXT))
    return resulting_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_node(node, delimiter, text_type))
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    # TODO rozwazyc rozbicie tego na 2 funkcje
    # TODO implementacja - extract a potem split po znalezionym i sklejenie w calość?
    # .. zip_longest z itertools do sklejenia?
    pass


def split_nodes_link(old_nodes: list[TextNode]):
    pass


if __name__ == "__main__":
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)
