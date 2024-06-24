#!/bin/bash

# Define the metadata table details
PROJECT_ID="my-project-id"
METADATA_DATASET="my-metadata-dataset"
METADATA_TABLE="my-metadata-table"

# Query the metadata table to get the list of tables to be backed up
bq query --use_legacy_sql=false --format=csv "SELECT source_project, source_dataset, source_table, target_project, target_dataset, target_table FROM \`${PROJECT_ID}.${METADATA_DATASET}.${METADATA_TABLE}\` where is_active =true" | tail -n +2 | while IFS=, read -r source_project source_dataset source_table target_project target_dataset target_table
do
  # Construct the source and target table references
  SOURCE_TABLE="${source_project}:${source_dataset}.${source_table}"
  TARGET_TABLE="${target_project}:${target_dataset}.${target_table}"

  # Run the bq copy command to create the backup table
  echo "Backing up ${SOURCE_TABLE} to ${TARGET_TABLE}..."
  bq cp -f "${SOURCE_TABLE}" "${TARGET_TABLE}"

  # Check if the command was successful
  if [ $? -eq 0 ]; then
    echo "Backup of ${SOURCE_TABLE} to ${TARGET_TABLE} completed successfully."
  else
    echo "Error: Backup of ${SOURCE_TABLE} to ${TARGET_TABLE} failed."
  fi
done
