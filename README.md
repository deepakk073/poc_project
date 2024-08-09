CREATE FUNCTION `your_project.your_dataset.cleanme` (input STRING) 
RETURNS STRING
LANGUAGE sql AS (
  REGEXP_REPLACE(input, r'[^a-zA-Z0-9]', '')
);
 poc_project