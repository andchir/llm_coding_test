#!/usr/bin/env python3
import re

# Read the HTML file
with open('/tmp/gh-issue-solver-1769453764623/results/index.html', 'r') as f:
    content = f.read()

# Extract JavaScript data and logic
print("Checking if CSV data is embedded in JavaScript...")
csv_data_match = re.search(r'const csvData = \[(.*?)\];', content, re.DOTALL)
if csv_data_match:
    print("✓ CSV data found in JavaScript")
    csv_content = csv_data_match.group(1)
    # Count number of data entries
    entries = csv_content.count('{ model_permaslug:')
    print(f"✓ Found {entries} CSV data entries")
else:
    print("✗ CSV data not found")

print("\nChecking if HTML file mapping is present...")
html_files_match = re.search(r'const htmlFiles = \[(.*?)\];', content, re.DOTALL)
if html_files_match:
    print("✓ HTML files mapping found")
    html_content = html_files_match.group(1)
    # Count number of HTML files
    files = html_content.count('{ filename:')
    print(f"✓ Found {files} HTML file entries")
else:
    print("✗ HTML files mapping not found")

print("\nChecking if model mapping is present...")
model_mapping_match = re.search(r'const modelMapping = \{(.*?)\};', content, re.DOTALL)
if model_mapping_match:
    print("✓ Model mapping found")
    mapping_content = model_mapping_match.group(1)
    # Count number of mappings
    mappings = mapping_content.count("': '")
    print(f"✓ Found {mappings} model mappings")
else:
    print("✗ Model mapping not found")

print("\nChecking if table population function exists...")
populate_function_match = re.search(r'function populateSummaryTable\(\)', content)
if populate_function_match:
    print("✓ populateSummaryTable function found")
else:
    print("✗ populateSummaryTable function not found")

print("\nChecking if DOMContentLoaded event listener exists...")
dom_ready_match = re.search(r'document\.addEventListener\(\'DOMContentLoaded\'', content)
if dom_ready_match:
    print("✓ DOMContentLoaded event listener found")
else:
    print("✗ DOMContentLoaded event listener not found")

print("\nVerifying required columns are present...")
required_columns = ["Модель", "Цена, USD", "Цена, рубли РФ", "Время генерации, сек"]
for col in required_columns:
    if col in content:
        print(f"✓ Column '{col}' found")
    else:
        print(f"✗ Column '{col}' not found")

print("\nVerifying conversion rates...")
if "* 76" in content:
    print("✓ USD to RUB conversion (rate 76) found")
else:
    print("✗ USD to RUB conversion not found")

if "/ 1000" in content:
    print("✓ MS to seconds conversion found")
else:
    print("✗ MS to seconds conversion not found")