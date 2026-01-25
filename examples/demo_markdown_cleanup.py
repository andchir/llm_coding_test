#!/usr/bin/env python3
"""
Demo script showing the Markdown code block cleanup functionality.
This demonstrates the fix for issue #7.
"""

import sys
sys.path.insert(0, '..')
from llm_runner import clean_markdown_code_blocks


def print_demo(title, input_text, output_text):
    """Print a demo example."""
    print("=" * 80)
    print(f"Demo: {title}")
    print("=" * 80)
    print("\n--- INPUT ---")
    print(repr(input_text))
    print("\n--- OUTPUT ---")
    print(repr(output_text))
    print("\n--- VISUAL OUTPUT ---")
    print(output_text)
    print("\n")


def main():
    """Run demo examples."""
    print("Markdown Code Block Cleanup Demo")
    print("Issue #7: Remove Markdown tags from beginning and end\n")

    # Example 1: HTML code block
    example1_input = """```html
<!DOCTYPE html>
<html>
<head>
    <title>Tetris Game</title>
</head>
<body>
    <canvas id="tetris"></canvas>
</body>
</html>
```"""
    example1_output = clean_markdown_code_blocks(example1_input)
    print_demo("HTML code block", example1_input, example1_output)

    # Example 2: Generic code block
    example2_input = """```
<div class="container">
    <h1>Hello World</h1>
</div>
```"""
    example2_output = clean_markdown_code_blocks(example2_input)
    print_demo("Generic code block", example2_input, example2_output)

    # Example 3: JavaScript code block
    example3_input = """```javascript
function initGame() {
    const canvas = document.getElementById('tetris');
    const ctx = canvas.getContext('2d');
    // Game logic here
}
```"""
    example3_output = clean_markdown_code_blocks(example3_input)
    print_demo("JavaScript code block", example3_input, example3_output)

    # Example 4: Already clean content (no code block)
    example4_input = """<!DOCTYPE html>
<html>
<body>Already clean HTML</body>
</html>"""
    example4_output = clean_markdown_code_blocks(example4_input)
    print_demo("Already clean content", example4_input, example4_output)

    # Example 5: Code block with extra whitespace
    example5_input = """

```html
<div>Content with whitespace</div>
```

"""
    example5_output = clean_markdown_code_blocks(example5_input)
    print_demo("Code block with extra whitespace", example5_input, example5_output)

    print("=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()
