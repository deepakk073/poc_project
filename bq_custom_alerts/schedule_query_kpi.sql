Declare var_emailmessage string;
set var_emailmessage ="""
Hi {user_email},
Below Query is running from more than 5 min. Please review the Query and Optimize the query and re-run the Query.
Query:- 
{query}


Thanks & Regards
Bigquery Admin Support
""";
with cte as(
  select max(id) max_id from cloud_run_tmp.email_outbox
)
SELECT
max_id + row_number() over(order by job_id)
  "Slow Running Query",
  user_email,
replace(replace(var_emailmessage,'{user_email}', user_email),'{query}') Email_Message,
  --timestamp_diff(current_timestamp,start_timestamp interval second) AS elapsed_time
  0
FROM
  `project_id.dataset_id.JOBS_BY_PROJECTS`
WHERE
  end_time IS NULL
GROUP BY
  query_id
HAVING
  timestamp_diff(current_timestamp,start_timestamp interval second) > 300
