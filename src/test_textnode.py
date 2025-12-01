import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_same_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("Different text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_noteq_difftype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_noteq_one_lacks_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, "https://google.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
