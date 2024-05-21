# Trigger a Cloud Run from a BigQuery event


This shows you how to trigger a Cloud Run container whenever an insert happens into a BigQuery table.


1. Run ```bq_cloud_run.sh```

2. In BigQuery web console, create a email_outbox table:

```
Create or replace table cloud_run_tmp.email_outbox(
  id int64,
  Email_Subject String,
  Email_To String,
  Email_Message String,
  email_sent int64
)
```

4. Visit Cloud Run web console and verify service has been launched and there are no triggers yet.
Make sure to look at logs and triggers to ensure service has been launched.

5. Insert a new row into the table:
```
insert into  cloud_run_tmp.email_outbox  values (5,'Test Email Subject','deepak_kumar4@XXXXXX.com','This is an auto generated email. Generated from Bigquery',0)
```

6. Look at Cloud Run web console for the service and see that it has been triggered

7. you can check your email, you will receive the email notification..

