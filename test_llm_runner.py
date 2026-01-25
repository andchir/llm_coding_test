#!/usr/bin/env python3
"""
Unit tests for llm_runner.py
"""

import unittest
from llm_runner import clean_markdown_code_blocks


class TestCleanMarkdownCodeBlocks(unittest.TestCase):
    """Test cases for the clean_markdown_code_blocks function."""

    def test_clean_html_code_block(self):
        """Test cleaning HTML code block."""
        input_text = """```html
<!DOCTYPE html>
<html>
<body>
<h1>Test</h1>
</body>
</html>
```"""
        expected = """<!DOCTYPE html>
<html>
<body>
<h1>Test</h1>
</body>
</html>"""
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_clean_generic_code_block(self):
        """Test cleaning generic code block without language."""
        input_text = """```
<div>Content</div>
```"""
        expected = "<div>Content</div>"
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_clean_javascript_code_block(self):
        """Test cleaning JavaScript code block."""
        input_text = """```javascript
function test() {
    console.log('Hello');
}
```"""
        expected = """function test() {
    console.log('Hello');
}"""
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_no_code_block(self):
        """Test content without code blocks."""
        input_text = "<html><body>Test</body></html>"
        expected = "<html><body>Test</body></html>"
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_with_whitespace(self):
        """Test cleaning with extra whitespace."""
        input_text = """
```html
<div>Test</div>
```
  """
        expected = "<div>Test</div>"
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_empty_string(self):
        """Test with empty string."""
        result = clean_markdown_code_blocks("")
        self.assertEqual(result, "")

    def test_none_value(self):
        """Test with None value."""
        result = clean_markdown_code_blocks(None)
        self.assertIsNone(result)

    def test_code_block_with_backticks_inside(self):
        """Test code block containing backticks in content."""
        input_text = """```html
<pre><code>
const x = `template ${string}`;
</code></pre>
```"""
        expected = """<pre><code>
const x = `template ${string}`;
</code></pre>"""
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_only_opening_fence(self):
        """Test with only opening fence (malformed)."""
        input_text = """```html
<div>Test</div>"""
        expected = "<div>Test</div>"
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)

    def test_multiline_content(self):
        """Test with complex multiline HTML content."""
        input_text = """```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tetris</title>
</head>
<body>
    <canvas id="game"></canvas>
    <script>
        // Game code here
    </script>
</body>
</html>
```"""
        expected = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tetris</title>
</head>
<body>
    <canvas id="game"></canvas>
    <script>
        // Game code here
    </script>
</body>
</html>"""
        result = clean_markdown_code_blocks(input_text)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
