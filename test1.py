import re

def extract_data_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split content based on '*****'
    blocks = re.split(r'\*{5,}', content)

    extracted_data = []

    for block in blocks:
        # Extract short_name
        short_name_match = re.search(r'short_name\s*=\s*"([^"]+)"', block)
        short_name = short_name_match.group(1) if short_name_match else None

        # Extract sae_def content
        sae_def_match = re.search(r'sae_def\s*=\s*(\[\{.*?\}\])', block, re.DOTALL)
        sae_def_values = sae_def_match.group(1) if sae_def_match else None

        # Store results only if short_name exists
        if short_name:
            extracted_data.append({"short_name": short_name, "sae_def": sae_def_values})

    return extracted_data

# Example usage
file_path = "your_file.txt"  # Replace with actual file path
data = extract_data_from_file(file_path)

# Print results
for item in data:
    print(item)
