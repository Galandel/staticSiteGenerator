import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def testrepr(self):
        tag = 'p'
        value = 'Hello my name is:'
        children = None
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(tag, value, children, props)
        expected_output = f"HTLMNode({tag}, {value}, {children}, {props})"
        self.assertEqual(expected_output, repr(node))
    
    def testprops_to_html(self):
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

if __name__ == "__main__":
    unittest.main()