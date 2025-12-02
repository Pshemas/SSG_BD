import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "Google", props={"href": "https://google.com"})
        expected_repr = "HTMLNode(a, Google, None, {'href': 'https://google.com'})"
        self.assertEqual(node.__repr__(), expected_repr)

    def test_props(self):
        sample_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "Google", props=sample_props)
        expected_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_result)

    def test_to_html(self):
        node = HTMLNode("a", "Google", props={"href": "https://google.com"})
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
