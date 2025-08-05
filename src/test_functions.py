import unittest

from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes, extract_title

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
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("link", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_multiple_images(self):
        text = "Here's ![first](url1.png) and ![second](url2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "url1.png"), ("second", "url2.jpg")], matches)

    def test_extract_mixed_content(self):
        text = "A ![image](img.png) and a [link](site.com)"
        # Should only get the link, not the image
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "site.com")], matches)
    
    def test_extract_mixed_content_images(self):
        text = "Here's ![first](url1.png) and ![second](url2.jpg) from [link](https://google.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "url1.png"), ("second", "url2.jpg")], matches)
    
    def test_extract_empty_alt_images(self):
        text = "here's ![](url1.png) and ![second](url2.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "url1.png"), ("second", "url2.jpeg")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode("Links [link text](https://url.org) and second [link text 2](https://url2.org)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://url.org"),
                TextNode(" and second ", TextType.TEXT),
                TextNode("link text 2", TextType.LINK, "https://url2.org"),
            ],
              new_nodes
        )
    
    def test_split_links_with_images(self):
        node = TextNode("Links [link text](https://url.org), a image ![image text](https://url2.org) and second [link text 2](https://url2.org)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://url.org"),
                TextNode(", a image ![image text](https://url2.org) and second ", TextType.TEXT),
                TextNode("link text 2", TextType.LINK, "https://url2.org"),
            ],
              new_nodes
        )

    def test_split_one_link(self):
        node = TextNode("Links [link text](https://url.org) and this is the end", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://url.org"),
                TextNode(" and this is the end", TextType.TEXT),
            ],
              new_nodes
        )   
    
    def test_split_one_link_no_follow_on_text(self):
        node = TextNode("Links [link text](https://url.org)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://url.org"),
            ],
              new_nodes
        ) 
    
    def test_split_one_link_in_two_places(self):
        node = TextNode("Links [link text](https://url.org) and [link text](https://url.org)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://url.org"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://url.org"),
            ],
              new_nodes
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected_output)
    
    def test_extract_title_1(self):
        markdown = '''
# I am a header
hello
## not a header
'''
        self.assertEqual(extract_title(markdown), "I am a header")

    def test_extract_title_error(self):
        markdown = '''
## not a title
yep
'''
        with self.assertRaises(Exception):
            extract_title(markdown)
    

if __name__ == "__main__":
    unittest.main()