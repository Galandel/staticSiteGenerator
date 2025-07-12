import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        tag = 'p'
        value = 'Hello my name is:'
        children = None
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(tag, value, children, props)
        expected_output = f"HTLMNode({tag}, {value}, {children}, {props})"
        self.assertEqual(expected_output, repr(node))
    
    def test_props_to_html(self):
        tag = 'p'
        value = 'Hello my name is:'
        children = None
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(tag, value, children, props)
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected_output, node.props_to_html())
    
    def test_to_html(self):
        tag = 'p'
        value = 'Hello my name is:'
        children = None
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(tag, value, children, props)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "google", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">google</a>')

    def test_value_exception(self):
        node = LeafNode("a",None, {"href": "www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_repr(self):
        node = LeafNode("a", "google", {"href": "www.google.com"})
        self.assertEqual(
            repr(node),
            "LeafNode(a, google, {'href': 'www.google.com'})"
        )
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()