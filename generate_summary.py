#!/usr/bin/env python3
"""Generate a summary HTML page from token_usage.json."""

import argparse
import html
import json
import sys
from pathlib import Path
from string import Template
from urllib.parse import quote


DEFAULT_TEMPLATE = Path(__file__).with_name('summary_template.html')


def sanitize_filename(model_name):
    """Use the same result filename convention as llm_runner.py."""
    return model_name.replace('/', '_').replace(':', '_')


def format_price(value):
    """Format a manually supplied price without assuming a currency."""
    if isinstance(value, float):
        return f'{value:g}'
    return str(value)


def load_summary_data(json_path):
    """Read and validate the current token usage schema."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict) or not isinstance(data.get('results'), list):
        raise ValueError(
            'Expected an object with "prompt" and "results" fields. '
            'Run llm_runner.py once to migrate an old file.'
        )
    return data


def build_summary_html(data, template_text):
    """Render summary data with the supplied HTML template."""
    prompt = html.escape(str(data.get('prompt', '')))
    currency = html.escape(str(data.get('currency', 'RUB')))
    results = data['results']
    total_tokens = sum(
        item.get('output_tokens', 0)
        for item in results
        if isinstance(item.get('output_tokens', 0), (int, float))
    )
    total_price = sum(
        item.get('price', 0)
        for item in results
        if isinstance(item.get('price', 0), (int, float))
    )

    rows = []
    for item in results:
        model = str(item.get('model', ''))
        filename = f'{sanitize_filename(model)}.html'
        href = quote(filename)
        rows.append(
            '<tr>'
            f'<td><a href="{href}">{html.escape(model)}</a></td>'
            f'<td>{html.escape(str(item.get("output_tokens", 0)))}</td>'
            f'<td>{html.escape(format_price(item.get("price", 0)))}</td>'
            f'<td>{currency}</td>'
            '</tr>'
        )

    rows_html = '\n'.join(rows) or (
        '<tr><td colspan="4" class="empty">Результатов пока нет</td></tr>'
    )
    return Template(template_text).substitute(
        prompt=prompt,
        model_count=len(results),
        total_tokens=f'{total_tokens:,}',
        total_price=html.escape(format_price(total_price)),
        currency=currency,
        rows=rows_html,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', type=Path, help='path to token_usage.json')
    parser.add_argument(
        '-o', '--output', type=Path,
        help='output HTML path (default: index.html next to the JSON file)',
    )
    parser.add_argument(
        '--template', type=Path, default=DEFAULT_TEMPLATE,
        help=f'HTML template path (default: {DEFAULT_TEMPLATE.name})',
    )
    args = parser.parse_args()

    output_path = args.output or args.json_file.with_name('index.html')
    try:
        data = load_summary_data(args.json_file)
        template_text = args.template.read_text(encoding='utf-8')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            build_summary_html(data, template_text),
            encoding='utf-8',
        )
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

    print(f'Created: {output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
