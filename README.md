SELECT
  dataset_id,
  ARRAY_AGG(STRUCT(label_key, label_value)) AS labels
FROM
  `region-us`.INFORMATION_SCHEMA.LABELS
WHERE
  project_id = 'your_project_id'
  AND dataset_id = 'your_dataset_id'
GROUP BY
  dataset_id;
