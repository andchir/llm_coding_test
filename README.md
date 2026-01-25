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

## Usage

Run the script:
```bash
python llm_runner.py
```

The script will:
1. Load configuration from `.env` file
2. Process each model sequentially
3. Create HTML files in the `output/` directory
4. Name each file according to the model name (with `/` replaced by `_`)

## Example

For model `openai/gpt-5.2`, the output file will be `output/openai_gpt-5.2.html`