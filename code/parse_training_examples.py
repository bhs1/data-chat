import json
import re

def fix_and_parse_json(file_path):
    """
    Fixes a text file and parses it into a list of dictionaries.
    
    Args:
    - file_path (str): The path to the text file to be fixed and parsed.
    
    Returns:
    - List[dict] or None: A list of dictionaries parsed from the fixed JSON content, or None if an error occurs.
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
            return None

def write_json_to_file(json_data, output_file_path):
    """
    Writes JSON data to a specified file.
    
    Args:
    - json_data (List[dict]): The JSON data to write.
    - output_file_path (str): The path to the output file.
    
    Returns:
    - bool: True if the file was successfully written, False otherwise.
    """
    if json_data is None:
        print("No JSON data to write.")
        return False
    
    try:
        with open(output_file_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return True
    except Exception as e:
        print(f"Error writing JSON to file: {e}")
        return False

# Example usage
for file_prefix in ('data/scott_chunked', 'data/ben_chunked', 'data/greg_chunked'):
    json_data = fix_and_parse_json(file_prefix + '.txt')
    if write_json_to_file(json_data, file_prefix + '.json'):
        print("Data successfully written to file.")
    else:
        print(f'Failed to write data to file for {file_prefix}')
