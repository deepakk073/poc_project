import re
import json

def terraform_to_dict(file_path):
    terraform_dict = {}

    with open(file_path, 'r') as file:
        content = file.read()

    # Extract resource blocks
    resources = re.findall(r'resource\s+"([^"]+)"\s+"([^"]+)"\s*{([^}]+)}', content)
    if resources:
        terraform_dict["resources"] = {}
        for resource_type, resource_name, resource_content in resources:
            terraform_dict["resources"][resource_name] = {
                "type": resource_type,
                "content": resource_content.strip()
            }

    # Extract variable blocks
    variables = re.findall(r'variable\s+"([^"]+)"\s*{([^}]+)}', content)
    if variables:
        terraform_dict["variables"] = {}
        for variable_name, variable_content in variables:
            terraform_dict["variables"][variable_name] = {
                "content": variable_content.strip()
            }

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

# Extract specific value (example: resources > "my_resource_name")
result = extract_value_from_dict(terraform_dict, 'resources.my_resource_name')
print("Extracted value:", result)
