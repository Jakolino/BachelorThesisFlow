import json
import os
from datetime import datetime
import re

def html_form_to_json(html_file_path, output_json_path=None):
    """
    Extract form structure from HTML file and create a JSON template/schema.
    This is useful for understanding the form fields before collecting data.
    """
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Extract form fields using regex patterns
    form_fields = {}
    
    # Find all input fields (text, number, email, radio, checkbox)
    input_pattern = r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>'
    inputs = re.findall(input_pattern, html_content)
    
    # Find all select fields
    select_pattern = r'<select[^>]*name=["\']([^"\']*)["\'][^>]*>'
    selects = re.findall(select_pattern, html_content)
    
    # Find all textarea fields
    textarea_pattern = r'<textarea[^>]*name=["\']([^"\']*)["\'][^>]*>'
    textareas = re.findall(textarea_pattern, html_content)
    
    # Create a schema
    schema = {
        "form_fields": {
            "inputs": list(set(inputs)),
            "selects": list(set(selects)),
            "textareas": list(set(textareas))
        },
        "all_fields": list(set(inputs + selects + textareas)),
        "timestamp": datetime.now().isoformat(),
        "form_structure": {}
    }
    
    # Add field types where possible
    for field in set(inputs):
        # Try to determine input type
        type_match = re.search(rf'<input[^>]*name=["\']{field}["\'][^>]*type=["\']([^"\']*)["\']', html_content)
        field_type = type_match.group(1) if type_match else "unknown"
        schema["form_structure"][field] = {"type": "input", "input_type": field_type}
    
    for field in set(selects):
        schema["form_structure"][field] = {"type": "select"}
    
    for field in set(textareas):
        schema["form_structure"][field] = {"type": "textarea"}
    
    # Save schema if output path provided
    if output_json_path:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        print(f"Schema saved to {output_json_path}")
    
    return schema

# Example usage
html_file = "demographics_questionnaire.html"
schema = html_form_to_json(html_file, "demographics_schema.json")
print("Form fields found:", schema["all_fields"])