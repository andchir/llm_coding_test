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
DEFAULT_RESULTS_TEMPLATE = Path(__file__).with_name('results_template.html')
PROJECT_ROOT = Path(__file__).resolve().parent


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
    results = sorted(
        data['results'],
        key=lambda item: str(item.get('model', '')).casefold(),
    )
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


def find_result_pages(root_dir):
    """Find index.html files in root-level directories named results*."""
    return sorted(
        directory.relative_to(root_dir) / 'index.html'
        for directory in root_dir.iterdir()
        if directory.is_dir()
        and directory.name.startswith('results')
        and (directory / 'index.html').is_file()
    )


def build_results_html(result_pages, template_text):
    """Render the root overview page with links to result index pages."""
    cards = []
    for page in result_pages:
        directory_name = page.parent.name
        href = quote(page.as_posix(), safe='/')
        cards.append(
            '<article class="result-card">'
            f'<h2>{html.escape(directory_name)}</h2>'
            f'<a href="{href}">Открыть результаты <span aria-hidden="true">→</span></a>'
            '</article>'
        )

    cards_html = '\n'.join(cards) or (
        '<p class="empty">Папки результатов с файлом index.html пока не найдены.</p>'
    )
    return Template(template_text).substitute(
        result_count=len(result_pages),
        result_cards=cards_html,
    )


def generate_results_overview(root_dir, template_path):
    """Create root/results.html from every results*/index.html page."""
    result_pages = find_result_pages(root_dir)
    template_text = template_path.read_text(encoding='utf-8')
    output_path = root_dir / 'results.html'
    output_path.write_text(
        build_results_html(result_pages, template_text),
        encoding='utf-8',
    )
    return output_path, len(result_pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'json_file', type=Path, nargs='?', help='path to token_usage.json',
    )
    parser.add_argument(
        '-o', '--output', type=Path,
        help='output HTML path (default: index.html next to the JSON file)',
    )
    parser.add_argument(
        '--template', type=Path, default=DEFAULT_TEMPLATE,
        help=f'HTML template path (default: {DEFAULT_TEMPLATE.name})',
    )
    parser.add_argument(
        '--results-template', type=Path, default=DEFAULT_RESULTS_TEMPLATE,
        help=f'root overview template (default: {DEFAULT_RESULTS_TEMPLATE.name})',
    )
    parser.add_argument(
        '--overview-only', action='store_true',
        help='only generate root results.html; no token_usage.json is required',
    )
    args = parser.parse_args()

    if not args.overview_only and args.json_file is None:
        parser.error('json_file is required unless --overview-only is used')

    try:
        if not args.overview_only:
            output_path = args.output or args.json_file.with_name('index.html')
            data = load_summary_data(args.json_file)
            template_text = args.template.read_text(encoding='utf-8')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                build_summary_html(data, template_text),
                encoding='utf-8',
            )
            print(f'Created: {output_path}')

        results_path, result_count = generate_results_overview(
            PROJECT_ROOT,
            args.results_template,
        )
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

    print(f'Created: {results_path} ({result_count} result pages)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
