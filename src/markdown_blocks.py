from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(None, map(str.strip, markdown.split("\n\n"))))


def is_unordered_list(markdown_text: str) -> bool:
    # TODO: simplify with startswith, keeping option to start with number greater than 1
    segments = markdown_text.split("\n")
    first_before_dot = []
    for segment in segments:
        first_before_dot.append(segment.split(". ", maxsplit=1)[0])
    try:
        convereted_firsts = [int(x) for x in first_before_dot if x]
        if len(convereted_firsts) == 1:
            return True
    except:
        return False
    idx = 0
    for number in convereted_firsts[1:]:
        if number != convereted_firsts[idx] + 1:
            return False
        idx += 1
    return True


def block_to_block_type(markdown_text: str) -> BlockType:
    if markdown_text[:7] == "###### ":
        return BlockType.HEADING
    if markdown_text[:6] == "##### ":
        return BlockType.HEADING
    if markdown_text[:5] == "#### ":
        return BlockType.HEADING
    if markdown_text[:4] == "### ":
        return BlockType.HEADING
    if markdown_text[:3] == "## ":
        return BlockType.HEADING
    if markdown_text[:2] == "# ":
        return BlockType.HEADING
    if markdown_text[:3] == "```" and markdown_text[-3:] == "```":
        return BlockType.CODE
    if all([x.startswith(">") for x in markdown_text.split("\n")]):
        return BlockType.QUOTE
    if all([x.startswith("- ") for x in markdown_text.split("\n")]):
        return BlockType.UNORDERED_LIST
    if is_unordered_list(markdown_text):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
