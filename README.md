WITH example_data AS (
  SELECT '[STRUCT("a","ad001"), STRUCT("category-1", "fie"), STRUCT("category-2", "fice"), STRUCT("data_classification", "highly-confidential"), STRUCT("environment", "development"), STRUCT("has_pi", "false"), STRUCT("segment", "sandbox")]' AS struct_text
)
SELECT
  REGEXP_EXTRACT(struct_text, r'STRUCT\("data_classification",\s*"([^"]*)"\)') AS data_classification
FROM
  example_data;
