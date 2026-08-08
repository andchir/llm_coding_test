# llm_coding_test

Python script for running LLM API calls with different models and saving responses to HTML files.

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env-example` to `.env`:
```bash
cp .env-example .env
```

2. Edit `.env` file with your settings:
   - `BASE_URL` - API endpoint URL
   - `API_KEY` - Your API key
   - `MODELS` - Comma-separated list of models to test
   - `PROMPT` - The prompt to send to all models
   - `SYSTEM_PROMPT` - System prompt that defines the AI behavior
   - `TEMPERATURE` - Temperature parameter for API calls (default: 0.3)
   - `FOLDER_NAME` - Folder name where results are saved (default: output)
   - `CURRENCY` - Currency unit for prices (default: RUB)

## Usage

Run the script:
```bash
python llm_runner.py
```

The script will:
1. Load configuration from `.env` file
2. Process each model sequentially
3. Create HTML files in the `output/` directory
4. Save the current prompt, currency, and output token counts to `output/token_usage.json`;
   its `results` list contains the model name, output token count, and a `price`
   field initialized to `0`
5. Name each HTML file according to the model name (with `/` replaced by `_`)

Generate `index.html` next to the JSON file using `summary_template.html`:
```bash
python3 generate_summary.py output/token_usage.json
```

Use another template if needed:
```bash
python3 generate_summary.py output/token_usage.json --template custom_template.html
```

## Example

For model `openai/gpt-5.2`, the output file will be `output/openai_gpt-5.2.html`
