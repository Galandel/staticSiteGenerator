import unittest

from textnode import TextNode, TextType
from functions import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes,expected_output)
    
    def test_split_nodes_delimiter_error_check(self):
        node = TextNode("This is text with a `code` block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
        
    def test_split_nodes_delimiter_text(self):
        node = TextNode("This is a full line of text and only text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [TextNode("This is a full line of text and only text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_output)
    
    def test_split_modes_delimiter_multiple(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block2` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected_output = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block2", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_delimiter_non_text_nodes(self):
        # Test that non-TEXT nodes are passed through unchanged
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_delimiter_empty_segments(self):
        # Test handling of empty segments (like "``word``")
        node = TextNode("text ``word`` more", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("text ", TextType.TEXT),
            TextNode("word", TextType.TEXT),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_output)


if __name__ == "__main__":
    unittest.main()