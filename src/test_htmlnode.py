import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    
    def test_repr(self):
        node = LeafNode("b", "This is a leaf node")
        self.assertIn("LeafNode(", f"{node}")
    
    def test_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", node.to_html())

    def test_no_value(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentCase(unittest.TestCase):
    
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),                    
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

    def test_nested_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),                    
                LeafNode(None, "Normal text"),
                ParentNode("p", 
                           [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                           ])
            ],
        )
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text</p></p>", node.to_html())

    def test_no_children(self):
        node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_no_tag(self):
        node = ParentNode(None, "This is a parent node")
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_deep_nested_parents(self):
        node = ParentNode("p",
                          [
                            ParentNode("b",
                                        [
                                            ParentNode("i",
                                                        [
                                                            LeafNode(None, "Normal text")
                                                        ]),
                                            LeafNode(None, "Normal text")
                                        ]),
                            LeafNode(None, "Normal text")
                          ])
        self.assertEqual("<p><b><i>Normal text</i>Normal text</b>Normal text</p>", node.to_html())

        

   

if __name__ == "__main__":
    unittest.main()