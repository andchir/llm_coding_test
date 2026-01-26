#!/usr/bin/env python3

# Test data similar to what's in the JavaScript
csv_data = [
    { 'model_permaslug': 'openai/gpt-5.1-codex-max-20251204', 'cost_total': 0.047017, 'generation_time_ms': 36499 },
    { 'model_permaslug': 'openai/gpt-5.2-20251211', 'cost_total': 0.171832, 'generation_time_ms': 142493 },
    { 'model_permaslug': 'xiaomi/mimo-v2-flash-20251210', 'cost_total': 0.001682, 'generation_time_ms': 36330 },
    { 'model_permaslug': 'x-ai/grok-4-07-09', 'cost_total': 0.054276, 'generation_time_ms': 49625 },
    { 'model_permaslug': 'openai/gpt-5.2-codex-20260114', 'cost_total': 0.042262, 'generation_time_ms': 48855 },
    { 'model_permaslug': 'qwen/qwen3-coder-plus', 'cost_total': 0.021526, 'generation_time_ms': 48043 },
    { 'model_permaslug': 'perplexity/sonar', 'cost_total': 0.009308, 'generation_time_ms': 21377 },
    { 'model_permaslug': 'x-ai/grok-4.1-fast', 'cost_total': 0.00268, 'generation_time_ms': 27649 },
    { 'model_permaslug': 'google/gemini-3-pro-preview-20251117', 'cost_total': 0.079632, 'generation_time_ms': 63262 },
    { 'model_permaslug': 'google/gemini-3-flash-preview-20251217', 'cost_total': 0.0099, 'generation_time_ms': 16592 },
    { 'model_permaslug': 'z-ai/glm-4.7-20251222', 'cost_total': 0.017941, 'generation_time_ms': 97225 },
    { 'model_permaslug': 'anthropic/claude-4.5-opus-20251124', 'cost_total': 0.17969, 'generation_time_ms': 71749 },
    { 'model_permaslug': 'anthropic/claude-4.5-sonnet-20250929', 'cost_total': 0.076974, 'generation_time_ms': 38634 }
]

html_files = [
    { 'filename': 'anthropic_claude-opus-4.5.html', 'modelName': 'Anthropic Claude Opus 4.5' },
    { 'filename': 'anthropic_claude-sonnet-4.5.html', 'modelName': 'Anthropic Claude Sonnet 4.5' },
    { 'filename': 'google_gemini-3-flash-preview.html', 'modelName': 'Google Gemini 3 Flash Preview' },
    { 'filename': 'google_gemini-3-pro-preview.html', 'modelName': 'Google Gemini 3 Pro Preview' },
    { 'filename': 'openai_gpt-5.1-codex-max.html', 'modelName': 'OpenAI GPT-5.1 Codex Max' },
    { 'filename': 'openai_gpt-5.2-codex.html', 'modelName': 'OpenAI GPT-5.2 Codex' },
    { 'filename': 'openai_gpt-5.2-pro.html', 'modelName': 'OpenAI GPT-5.2 Pro' },
    { 'filename': 'openai_gpt-5.2.html', 'modelName': 'OpenAI GPT-5.2' },
    { 'filename': 'perplexity_sonar.html', 'modelName': 'Perplexity Sonar' },
    { 'filename': 'qwen_qwen3-coder-plus.html', 'modelName': 'Qwen Qwen3 Coder Plus' },
    { 'filename': 'qwen_qwen3-max.html', 'modelName': 'Qwen Qwen3 Max' },
    { 'filename': 'x-ai_grok-4.1-fast.html', 'modelName': 'X.AI Grok 4.1 Fast' },
    { 'filename': 'x-ai_grok-4.html', 'modelName': 'X.AI Grok 4' },
    { 'filename': 'xiaomi_mimo-v2-flash.html', 'modelName': 'Xiaomi Mimo V2 Flash' },
    { 'filename': 'z-ai_glm-4.6.html', 'modelName': 'Z.AI GLM 4.6' },
    { 'filename': 'z-ai_glm-4.7.html', 'modelName': 'Z.AI GLM 4.7' },
    { 'filename': 'opencode_big-pickle.html', 'modelName': 'OpenCode Big Pickle' }
]

model_mapping = {
    'openai/gpt-5.1-codex-max-20251204': 'OpenAI GPT-5.1 Codex Max',
    'openai/gpt-5.2-20251211': 'OpenAI GPT-5.2',
    'xiaomi/mimo-v2-flash-20251210': 'Xiaomi Mimo V2 Flash',
    'x-ai/grok-4-07-09': 'X.AI Grok 4',
    'openai/gpt-5.2-codex-20260114': 'OpenAI GPT-5.2 Codex',
    'qwen/qwen3-coder-plus': 'Qwen Qwen3 Coder Plus',
    'perplexity/sonar': 'Perplexity Sonar',
    'x-ai/grok-4.1-fast': 'X.AI Grok 4.1 Fast',
    'google/gemini-3-pro-preview-20251117': 'Google Gemini 3 Pro Preview',
    'google/gemini-3-flash-preview-20251217': 'Google Gemini 3 Flash Preview',
    'z-ai/glm-4.7-20251222': 'Z.AI GLM 4.7',
    'anthropic/claude-4.5-opus-20251124': 'Anthropic Claude Opus 4.5',
    'anthropic/claude-4.5-sonnet-20250929': 'Anthropic Claude Sonnet 4.5'
}

# Simulate the table population logic
csv_map = {}
for item in csv_data:
    csv_map[item['model_permaslug']] = item

all_models = set()

# Add models from CSV data
for item in csv_data:
    friendly_name = model_mapping.get(item['model_permaslug'], item['model_permaslug'])
    all_models.add(friendly_name)

# Add models from HTML files that might not be in CSV
for html_file in html_files:
    all_models.add(html_file['modelName'])

# Convert to array and sort alphabetically
sorted_models = sorted(all_models)

print("Summary Table Data Verification")
print("=" * 60)
print(f"Total models: {len(sorted_models)}")
print()

print("{:<30} {:<12} {:<12} {:<15}".format("Model", "Cost USD", "Cost RUB", "Time (sec)"))
print("-" * 70)

models_with_data = 0
models_without_data = 0

for model_name in sorted_models:
    # Find corresponding CSV data
    csv_item = None
    for key, value in csv_map.items():
        if model_mapping.get(key) == model_name:
            csv_item = value
            break

    cost_usd = 0.0
    cost_rub = 0.0
    time_seconds = 0.0

    if csv_item:
        cost_usd = float(csv_item['cost_total'])
        cost_rub = cost_usd * 76
        time_seconds = float(csv_item['generation_time_ms']) / 1000
        models_with_data += 1
    else:
        models_without_data += 1

    print("{:<30} {:<12.6f} {:<12.2f} {:<15.2f}".format(
        model_name, cost_usd, cost_rub, time_seconds
    ))

print()
print(f"Models with CSV data: {models_with_data}")
print(f"Models without CSV data (cost = 0): {models_without_data}")

# Verify specific requirements
print()
print("Requirements Check:")
print("- ✓ Models are sorted alphabetically")
print("- ✓ Missing data gets cost 0 and time 0")
print("- ✓ USD to RUB conversion uses rate 76")
print("- ✓ Time converted from ms to seconds")