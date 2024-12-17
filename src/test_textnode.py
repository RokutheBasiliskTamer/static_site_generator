import unittest
from textnode import TextNode, TextType

class TestTextNose(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertIn("TextNode(", f"{node}")
    
    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
    
    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This could be a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_diff_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "./src")
        node2 = TextNode("This is a text node", TextType.BOLD, "./content")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()