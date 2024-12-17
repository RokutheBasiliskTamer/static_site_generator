import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
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

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text_to_html(self):
        normal_text = TextNode("hello world", TextType.NORMAL)
        bold_text = TextNode("hello world", TextType.BOLD)
        italic_text = TextNode("hello world", TextType.ITALIC)
        code_text = TextNode("hello world", TextType.CODE)
        link_text = TextNode("hello world", TextType.LINK, "./src")
        image_text = TextNode("hello world", TextType.IMAGE, "./src")

        normal_html = LeafNode(None, "hello world")
        bold_html = LeafNode("b", "hello world")
        italic_html = LeafNode("i", "hello world")
        code_html = LeafNode("code", "hello world")
        link_html = LeafNode("a", "hello world", {"href": "./src"})
        image_html = LeafNode("img", "", {"src": "./src", "alt": "hello world"})

        self.assertEqual(text_node_to_html_node(normal_text), normal_html)
        self.assertEqual(text_node_to_html_node(bold_text), bold_html)
        self.assertEqual(text_node_to_html_node(italic_text), italic_html)
        self.assertEqual(text_node_to_html_node(code_text), code_html)
        self.assertEqual(text_node_to_html_node(link_text), link_html)
        self.assertEqual(text_node_to_html_node(image_text), image_html)

    def test_invalid_type(self):
        node = TextNode("hello world", "huhu")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
        

if __name__ == "__main__":
    unittest.main()