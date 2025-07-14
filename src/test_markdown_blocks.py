import unittest

from markdown_blocks import markdown_to_blocks

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_excess_newlines(self):
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.




 - This is the first list item in a list block
 - This is a list item
 - This is another list item'''
        expected_output = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.', '- This is the first list item in a list block\n - This is a list item\n - This is another list item']
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

if __name__ == "__main__":
    unittest.main()