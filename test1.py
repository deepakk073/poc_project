import re
import json

def terraform_to_dict(file_path):
    terraform_dict = {}

    with open(file_path, 'r') as file:
        content = file.read()

    # Extracting `app_data` block and inner values
    app_data = re.findall(r'app_data\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if app_data:
        terraform_dict["app_data"] = []
        for entry in app_data[0].split('},'):
            entry = entry.strip()
            if entry:
                # Extract shrt_name and sae
                shrt_name = re.findall(r'shrt_name\s*=\s*"([^"]+)"', entry)
                sae = re.findall(r'put\s*=\s*"([^"]+)"', entry)

                terraform_dict["app_data"].append({
                    "shrt_name": shrt_name[0] if shrt_name else None,
                    "sae": sae
                })

    return terraform_dict

def extract_value_from_dict(terraform_dict, key):
    keys = key.split(".")
    value = terraform_dict
    for k in keys:
        value = value.get(k, {})
    return value

# Example usage
terraform_dict = terraform_to_dict('example.tf')

# Convert to JSON string for a clear view
print(json.dumps(terraform_dict, indent=4))

# Extract specific values
result_shrt_name = extract_value_from_dict(terraform_dict, 'app_data.0.shrt_name')
print("Extracted shrt_name:", result_shrt_name)

result_sae = extract_value_from_dict(terraform_dict, 'app_data.0.sae')
print("Extracted sae:", result_sae)
