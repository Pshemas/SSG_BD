import unittest

from markdown_to_html import *


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraph(self):
        md = """This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
            """
        html = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        htmlnodes_from_md = markdown_to_html_node(md)
        self.assertEqual(htmlnodes_from_md.to_html(), html)

    def test_codeblock(self):
        html = (
            "<div><pre><code>\nfor i in range(10):\n    print(i)\n</code></pre></div>"
        )
        md = """
```
for i in range(10):
    print(i)
```
"""
        aaa = markdown_to_html_node(md).to_html()
        self.assertEqual(aaa, html)

    def test_lists(self):
        html = "<div><ul><li>ulist first</li><li>ulist second</li><li>ulist third</li></ul><ol><li>Ordered first</li><li>Ordered second</li><li>Ordered third</li></ol></div>"
        md = """
- ulist first
- ulist second
- ulist third

1. Ordered first
2. Ordered second
3. Ordered third
        """
        aaa = markdown_to_html_node(md).to_html()
        self.assertEqual(aaa, html)

    def test_heading(self):
        html = "<div><h2>H2 Heading</h2></div>"
        md = "## H2 Heading"
        conv_html = markdown_to_html_node(md).to_html()
        self.assertEqual(conv_html, html)


if __name__ == "__main__":
    unittest.main()
