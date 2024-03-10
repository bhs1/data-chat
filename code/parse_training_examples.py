import json
import re

def fix_and_parse_json(file_path):
    """
    Fixes a text file by removing all double newlines, ensuring proper separation between JSON objects,
    removing all new lines and square brackets, handling multiple JSON arrays and objects concatenated without proper separation,
    and parses it into a list of dictionaries.
    
    Args:
    - file_path (str): The path to the text file.
    
    Returns:
    - List[dict]: A list of dictionaries parsed from the fixed JSON content.
    """
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Remove all double newlines
        content = content.replace('\n\n', '\n')
        
        # Remove all new lines
        content = content.replace('\n', '').replace('```', '').replace('json', '')
        
        # Remove all square brackets
        content = content.replace('[', '').replace(']', '')
        
        # Ensure proper separation between JSON objects
        content = re.sub(r'}\s*{', '},{', content)  # Handles }{
        content = re.sub(r'}\s*\n\s*{', '},\n{', content)  # Handles }\n{
        
        # Remove stray "json" strings
        content = re.sub(r'\"\s*json\s*\"', '', content)
        
        # Remove commas at the end of lines that start with "...":
        content = re.sub(r'("[^"]+":\s*[^,]+),\s*$', r'\1', content, flags=re.MULTILINE)
        
        # Insert a comma between any two adjacent curly braces that don't already have a comma
        content = re.sub(r'}\s*(?=\{)','}\n,', content)
        
        # Wrap the entire content in square brackets to form a valid JSON array
        fixed_content = f'[{content}]'
        
        try:
            # Attempt to parse the fixed content as JSON
            json_data = json.loads(fixed_content)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(fixed_content)
            return []

# Example usage
# TODO: Proceed with fine tuning.
data = fix_and_parse_json('data/scott_chunked.txt')
print(data)
