import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("b", "This is a HTML Node")
        self.assertIn("HTMLNode(", f"{node}")
    
    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)


    def test_props_to_html(self):
        node = HTMLNode("i", "This is a HTML Node", props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node.props_to_html())
    
    def test_to_html(self):
        node = HTMLNode(None, "This is an HTML Node")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_leaf_repr(self):
        node = LeafNode("b", "This is a leaf node")
        self.assertIn("LeafNode(", f"{node}")
    
    def test_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", node.to_html())

    def test_leaf_no_value(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()
   

if __name__ == "__main__":
    unittest.main()