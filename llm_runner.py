#!/usr/bin/env python3
"""
Script for running LLM API calls with different models.
Creates HTML files with responses for each model.
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv


def sanitize_filename(model_name):
    """Convert model name to a valid filename."""
    return model_name.replace('/', '_').replace(':', '_')


def create_html_file(model_name, response_content, output_dir='output'):
    """Create HTML file with the model response."""
    Path(output_dir).mkdir(exist_ok=True)

    filename = f"{sanitize_filename(model_name)}.html"
    filepath = Path(output_dir) / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response_content)

    return filepath


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
        'stream': False
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()

        # Extract content from response
        if 'choices' in data and len(data['choices']) > 0:
            content = data['choices'][0]['message']['content']
            return content
        else:
            return f"Error: Unexpected response format: {data}"

    except requests.exceptions.RequestException as e:
        return f"Error calling API: {str(e)}"


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

    # Process each model
    for i, model in enumerate(models, 1):
        print(f"[{i}/{len(models)}] Processing model: {model}")

        # Call API
        response_content = call_llm_api(base_url, api_key, model, prompt, system_prompt, temperature)

        # Create HTML file
        filepath = create_html_file(model, response_content, folder_name)

        print(f"  → Created: {filepath}")

    print("\nAll models processed successfully!")


if __name__ == '__main__':
    main()
