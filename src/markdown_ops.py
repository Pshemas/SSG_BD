from textnode import TextType, TextNode
import re


def split_node(
    old_node: TextNode,
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    resulting_nodes = []
    if delimiter not in old_node.text:
        return [old_node]
        # raise ValueError("Delimeter not found in node")
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


def sections_to_nodes(
    sections: list,
    url_data,
    not_even: int = 1,
    extracted_node_type: TextType = TextType.IMAGE,
) -> list[TextNode]:
    nodes = []
    for idx, section in enumerate(sections):
        if idx % 2 == not_even:
            nodes.append(TextNode(url_data[0], extracted_node_type, url_data[1]))
        if section:
            nodes.append(TextNode(section, TextType.TEXT))
    return nodes


def split_single_node_image(old_node: TextNode) -> list[TextNode]:
    image_tags = extract_markdown_images(old_node.text)
    if image_tags:
        sections = old_node.text.split(f"![{image_tags[0][0]}]({image_tags[0][1]})", 1)
        new_nodes = sections_to_nodes(sections, image_tags[0])
        if len(image_tags) > 1:
            for tag in image_tags[1:]:
                extra_node = new_nodes.pop()
                new_nodes.extend(
                    sections_to_nodes(
                        extra_node.text.split(f"![{tag[0]}]({tag[1]})", 1),
                        tag,
                    )
                )
        return new_nodes

    else:
        return [old_node]


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(split_single_node_image(node))

    return new_nodes


def split_single_node_link(old_node: TextNode) -> list[TextNode]:
    link_tags = extract_markdown_links(old_node.text)
    if link_tags:
        sections = old_node.text.split(f"[{link_tags[0][0]}]({link_tags[0][1]})", 1)
        new_nodes = sections_to_nodes(
            sections, link_tags[0], extracted_node_type=TextType.LINK
        )
        if len(link_tags) > 1:
            for tag in link_tags[1:]:
                extra_node = new_nodes.pop()
                new_nodes.extend(
                    sections_to_nodes(
                        extra_node.text.split(f"[{tag[0]}]({tag[1]})", 1),
                        tag,
                        extracted_node_type=TextType.LINK,
                    )
                )
        return new_nodes

    else:
        return [old_node]


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(split_single_node_link(node))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes_list = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_delimiter(nodes_list, "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "_", TextType.ITALIC)
    nodes_list = split_nodes_link(nodes_list)
    nodes_list = split_nodes_image(nodes_list)
    return nodes_list


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(None, map(str.strip, markdown.split("\n\n"))))
