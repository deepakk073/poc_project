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
-------------------------------------------------------------------------------------------------------------------------
import re
from google.cloud import bigquery

# Set up BigQuery Client (Ensure your service account key is set up correctly)
client = bigquery.Client()

# Replace with your BigQuery details
PROJECT_ID = "your_project_id"
DATASET_ID = "your_dataset_id"
TABLE_ID = "your_table_id"

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

def insert_into_bigquery(data):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Define rows to insert
    rows_to_insert = [
        {"short_name": item["short_name"], "sae_def": item["sae_def"]}
        for item in data
    ]

    # Insert data
    errors = client.insert_rows_json(table_ref, rows_to_insert)

    if errors:
        print("Errors while inserting rows:", errors)
    else:
        print("Data inserted successfully into BigQuery.")

# Example usage
file_path = "your_file.txt"  # Replace with actual file path
extracted_data = extract_data_from_file(file_path)

if extracted_data:
    insert_into_bigquery(extracted_data)
else:
    print("No valid data found to insert.")
---------------------------------------------------------------------------------------------------
import re
from google.cloud import bigquery

# Set up BigQuery Client
client = bigquery.Client()

# Replace with your BigQuery details
PROJECT_ID = "your_project_id"
DATASET_ID = "your_dataset_id"
TABLE_ID = "your_table_id"

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

        # Extract sae_def content spanning multiple lines
        sae_def_match = re.search(r'sae_def\s*=\s*\[(.*?)\]', block, re.DOTALL)
        sae_def_values = sae_def_match.group(1).strip() if sae_def_match else None

        # Store results only if short_name exists
        if short_name:
            extracted_data.append({"short_name": short_name, "sae_def": sae_def_values})

    return extracted_data

def overwrite_bigquery_table(data):
    # Define the table reference
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Create the BigQuery table schema
    schema = [
        bigquery.SchemaField("short_name", "STRING"),
        bigquery.SchemaField("sae_def", "STRING")
    ]

    # Prepare the rows to insert
    rows_to_insert = [
        {"short_name": item["short_name"], "sae_def": item["sae_def"]}
        for item in data
    ]

    # Set the configuration for table overwrite
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # This will overwrite the table
    )

    # Insert data and overwrite the table
    errors = client.load_table_from_json(rows_to_insert, table_ref, job_config=job_config)

    if errors:
        print("Errors while overwriting the table:", errors)
    else:
        print("Table overwritten successfully with the new data.")

# Example usage
file_path = "your_file.txt"  # Replace with actual file path
extracted_data = extract_data_from_file(file_path)

if extracted_data:
    overwrite_bigquery_table(extracted_data)
else:
    print("No valid data found to overwrite the table.")
------------------------------------------------------------------------------------------------
import re
from google.cloud import bigquery

# Set up BigQuery Client (Ensure service account key is set up)
client = bigquery.Client()

# Replace with your BigQuery details
PROJECT_ID = "your_project_id"
DATASET_ID = "your_dataset_id"
TABLE_ID = "your_table_id"

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

        # Extract sae_def (handling multi-line and nested lists)
        sae_def_match = re.search(r'sae_def\s*=\s*\[\s*(.*?)\s*\]', block, re.DOTALL)

        if sae_def_match:
            sae_def_content = sae_def_match.group(1)

            # Preserve formatting while removing unwanted lone "]"
            sae_def_lines = [line.strip() for line in sae_def_content.split("\n") if line.strip() != "]"]
            sae_def_values = "\n".join(sae_def_lines)  # Join as multi-line string

        else:
            sae_def_values = None

        # Store results only if short_name exists
        if short_name:
            extracted_data.append({"short_name": short_name, "sae_def": sae_def_values})

    return extracted_data

def insert_into_bigquery(data):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Define rows to insert
    rows_to_insert = [
        {"short_name": item["short_name"], "sae_def": item["sae_def"]}
        for item in data
    ]

    # Insert data into BigQuery
    errors = client.insert_rows_json(table_ref, rows_to_insert)

    if errors:
        print("Errors while inserting rows:", errors)
    else:
        print("Data inserted successfully into BigQuery.")

# Example usage
file_path = "your_file.txt"  # Replace with actual file path
extracted_data = extract_data_from_file(file_path)

if extracted_data:
    insert_into_bigquery(extracted_data)
else:
    print("No valid data found to insert.")
