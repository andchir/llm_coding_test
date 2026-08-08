#!/usr/bin/env python3
"""
Script for running LLM API calls with different models.
Creates HTML files with responses for each model.
"""

import json
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv


def sanitize_filename(model_name):
    """Convert model name to a valid filename."""
    return model_name.replace('/', '_').replace(':', '_')


def clean_markdown_code_blocks(content):
    """Remove Markdown code blocks from the beginning and end of content.

    Args:
        content: String content that may contain Markdown code blocks

    Returns:
        Cleaned content without Markdown code block delimiters
    """
    if not content:
        return content

    # Strip whitespace first
    cleaned = content.strip()

    # Remove opening code block (```language or just ```)
    # Match ``` followed by optional language identifier and newline
    if cleaned.startswith('```'):
        # Find the end of the first line (opening fence)
        first_newline = cleaned.find('\n')
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1:]

    # Remove closing code block (```)
    # Only remove if it's at the end and on its own line
    if cleaned.endswith('```'):
        # Find the last occurrence of ``` that's at the start of a line
        lines = cleaned.split('\n')
        if lines and lines[-1].strip() == '```':
            cleaned = '\n'.join(lines[:-1])

    # Strip any remaining whitespace
    return cleaned.strip()


def create_html_file(model_name, response_content, output_dir='output'):
    """Create HTML file with the model response."""
    Path(output_dir).mkdir(exist_ok=True)

    filename = f"{sanitize_filename(model_name)}.html"
    filepath = Path(output_dir) / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response_content)

    return filepath


def load_usage_data(usage_path, prompt, currency='RUB'):
    """Load usage data and migrate the old list format in memory."""
    usage_data = {'prompt': prompt, 'currency': currency, 'results': []}
    if not usage_path.exists():
        return usage_data

    try:
        with open(usage_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  Warning: could not read {usage_path}: {e}; resetting it")
        return usage_data

    if isinstance(loaded_data, list):
        # Backward compatibility with the original token_usage.json format.
        usage_data['results'] = loaded_data
    elif isinstance(loaded_data, dict) and isinstance(loaded_data.get('results'), list):
        usage_data = loaded_data
        usage_data['prompt'] = prompt
        usage_data['currency'] = currency
    else:
        print(f"  Warning: {usage_path} has an unexpected format; resetting it")

    return usage_data


def write_usage_data(usage_path, usage_data):
    """Atomically write shared usage data."""
    temporary_path = usage_path.with_suffix('.json.tmp')
    with open(temporary_path, 'w', encoding='utf-8') as f:
        json.dump(usage_data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    temporary_path.replace(usage_path)


def update_usage_prompt(prompt, output_dir='output', currency='RUB'):
    """Create the usage file and update its shared prompt and currency."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    usage_path = output_path / 'token_usage.json'
    usage_data = load_usage_data(usage_path, prompt, currency)
    write_usage_data(usage_path, usage_data)
    return usage_path


def save_token_usage(
    model_name,
    output_tokens,
    output_dir='output',
    prompt='',
    currency='RUB',
):
    """Save output token usage for a model to the shared JSON file.

    Existing prices are intentionally preserved because they are filled in
    separately. A model has a single result file, so its usage entry is updated
    instead of duplicated when the model is run again.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    usage_path = output_path / 'token_usage.json'

    usage_data = load_usage_data(usage_path, prompt, currency)
    results = usage_data['results']

    existing_entry = next(
        (entry for entry in results if entry.get('model') == model_name),
        None,
    )
    if existing_entry is None:
        results.append({
            'model': model_name,
            'output_tokens': output_tokens,
            'price': 0,
        })
    else:
        existing_entry['output_tokens'] = output_tokens
        existing_entry.setdefault('price', 0)

    write_usage_data(usage_path, usage_data)

    return usage_path


def call_llm_api(base_url, api_key, model, prompt, system_prompt, temperature=0.3):
    """Make API call to LLM service."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': model,
        'messages': [
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': temperature,
        'stream': False,
        'reasoning': {
            'enabled': True
        }
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()

        # Extract content and output token count from response
        if 'choices' in data and len(data['choices']) > 0:
            content = data['choices'][0]['message']['content']
            usage = data.get('usage') or {}
            output_tokens = usage.get(
                'completion_tokens',
                usage.get('output_tokens', 0),
            )
            return content, output_tokens
        else:
            return f"Error: Unexpected response format: {data}", 0

    except requests.exceptions.RequestException as e:
        return f"Error calling API: {str(e)}", 0


def main():
    """Main function to process all models."""
    # Load environment variables
    load_dotenv()

    base_url = os.getenv('BASE_URL')
    api_key = os.getenv('API_KEY')
    models_str = os.getenv('MODELS')
    prompt = os.getenv('PROMPT')
    system_prompt = os.getenv('SYSTEM_PROMPT')
    temperature = float(os.getenv('TEMPERATURE', '0.3'))
    folder_name = os.getenv('FOLDER_NAME', 'output')
    currency = os.getenv('CURRENCY', 'RUB').strip() or 'RUB'

    # Validate required parameters
    if not base_url:
        print("Error: BASE_URL not found in .env file")
        sys.exit(1)

    if not api_key:
        print("Error: API_KEY not found in .env file")
        sys.exit(1)

    if not models_str:
        print("Error: MODELS not found in .env file")
        sys.exit(1)

    if not prompt:
        print("Error: PROMPT not found in .env file")
        sys.exit(1)

    if not system_prompt:
        print("Error: SYSTEM_PROMPT not found in .env file")
        sys.exit(1)

    # Parse models list
    models = [model.strip() for model in models_str.split(',')]

    print(f"Starting LLM API calls for {len(models)} models...")
    print(f"Base URL: {base_url}")
    print(f"Prompt: {prompt}\n")

    # Keep the shared prompt current even when every model is skipped.
    usage_path = update_usage_prompt(prompt, folder_name, currency)
    print(f"Usage data: {usage_path}\n")

    # Process each model
    for i, model in enumerate(models, 1):
        print(f"[{i}/{len(models)}] Processing model: {model}")
        filename = f"{sanitize_filename(model)}.html"
        filepath = Path(folder_name) / filename
        if os.path.isfile(filepath):
            print(f'SKIP {model}')
            continue

        # Call API
        response_content, output_tokens = call_llm_api(
            base_url,
            api_key,
            model,
            prompt,
            system_prompt,
            temperature,
        )

        # Clean Markdown code blocks from response
        cleaned_content = clean_markdown_code_blocks(response_content)

        # Create HTML file
        filepath = create_html_file(model, cleaned_content, folder_name)

        # Store token usage in a shared JSON file.
        usage_path = save_token_usage(
            model,
            output_tokens,
            prompt=prompt,
            output_dir=folder_name,
            currency=currency,
        )

        print(f"  → Created: {filepath}")
        print(f"  → Output tokens: {output_tokens} ({usage_path})")

    print("\nAll models processed successfully!")


if __name__ == '__main__':
    main()
