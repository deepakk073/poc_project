WITH ExtractedQueries AS (
  SELECT
    protopayload_auditlog.authenticationInfo.principalEmail AS user_email,
    protopayload_auditlog.serviceData_v1_bigquery.jobCompletedEvent.job.jobConfiguration.query.query AS query_text,
    resource.labels.project_id AS project_id,
    TIMESTAMP(protoPayload.serviceData_v1_bigquery.jobCompletedEvent.job.jobStatistics.createTime) AS query_time
  FROM
    `project.dataset.bigquery_logs`
  WHERE
    protoPayload.serviceName = "bigquery.googleapis.com"
    AND protoPayload.methodName = "jobservice.jobcompleted" -- Focus only on completed jobs
    AND protopayload_auditlog.serviceData_v1_bigquery.jobCompletedEvent.job.jobConfiguration.query IS NOT NULL
),
PIIColumns AS (
  SELECT
    table_name,
    column_name
  FROM
    `project.dataset.pii_columns_table`
),
MatchedAccess AS (
  SELECT
    eq.user_email,
    eq.query_text,
    pii.table_name,
    pii.column_name,
    eq.query_time
  FROM
    ExtractedQueries eq
  JOIN
    PIIColumns pii
  ON
    eq.query_text LIKE CONCAT('%', pii.table_name, '%')
    AND eq.query_text LIKE CONCAT('%', pii.column_name, '%')
)
SELECT
  user_email,
  table_name,
  column_name,
  query_time,
  query_text
FROM
  MatchedAccess
ORDER BY
  query_time DESC;

#!/bin/bash

# Configuration for SMTP
SMTP_SERVER="smtp.example.com"
SMTP_PORT=587
SMTP_USER="your_smtp_user"
SMTP_PASSWORD="your_smtp_password"
SENDER_EMAIL="your_email@example.com"

# Function to send email using mailx
send_email() {
  local to=$1
  local subject=$2
  local body=$3

  echo "$body" | mailx -s "$subject" -S smtp="smtp://$SMTP_SERVER:$SMTP_PORT" \
    -S smtp-auth=login -S smtp-auth-user="$SMTP_USER" \
    -S smtp-auth-password="$SMTP_PASSWORD" -S from="$SENDER_EMAIL" "$to"

  return $?
}

# Test values
TEST_EMAIL_TO="recipient@example.com"
TEST_EMAIL_SUBJECT="Test Email"
TEST_EMAIL_BODY="This is a test email sent from the shell script using mailx."

# Sending test email
send_email "$TEST_EMAIL_TO" "$TEST_EMAIL_SUBJECT" "$TEST_EMAIL_BODY"
if [ $? -eq 0 ]; then
  echo "Test email sent successfully to $TEST_EMAIL_TO."
else
  echo "Failed to send test email to $TEST_EMAIL_TO."
fi



#!/bin/bash

# Configuration
PROJECT_ID="your_project_id"
DATASET_ID="your_dataset_id"
TABLE_ID="email_outbox"
SMTP_SERVER="smtp.example.com"
SMTP_PORT=587
SMTP_USER="your_smtp_user"
SMTP_PASSWORD="your_smtp_password"
SENDER_EMAIL="your_email@example.com"

# Temporary files
QUERY_RESULT="emails_to_send.json"

# Query BigQuery to get all unsent emails
echo "Fetching unsent emails from BigQuery..."
bq query --nouse_legacy_sql --format=json "
SELECT email_to, email_subject, Email_text
FROM \`${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\`
WHERE is_sent = 0
" > $QUERY_RESULT

# Check if there are any emails to send
if [[ ! -s $QUERY_RESULT ]]; then
  echo "No unsent emails found."
  exit 0
fi

# Function to send email
send_email() {
  local to=$1
  local subject=$2
  local body=$3

  echo -e "To: $to\nSubject: $subject\n\n$body" | msmtp --host=$SMTP_SERVER --port=$SMTP_PORT --auth=on \
    --user=$SMTP_USER --passwordeval="echo $SMTP_PASSWORD" --from=$SENDER_EMAIL --tls=on $to

  return $?
}

# Iterate over the emails and send them
for row in $(cat $QUERY_RESULT | jq -r '.[] | @base64'); do
  _jq() {
    echo ${row} | base64 --decode | jq -r ${1}
  }

  EMAIL_TO=$(_jq '.email_to')
  EMAIL_SUBJECT=$(_jq '.email_subject')
  EMAIL_TEXT=$(_jq '.Email_text')

  echo "Sending email to $EMAIL_TO with subject: $EMAIL_SUBJECT"
  
  # Send email
  send_email "$EMAIL_TO" "$EMAIL_SUBJECT" "$EMAIL_TEXT"
  if [ $? -eq 0 ]; then
    echo "Email sent successfully to $EMAIL_TO."
    
    # Update the BigQuery table to mark the email as sent
    echo "Updating BigQuery for $EMAIL_TO..."
    bq query --nouse_legacy_sql "
    UPDATE \`${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\`
    SET is_sent = 1
    WHERE email_to = '$EMAIL_TO' AND is_sent = 0
    "
  else
    echo "Failed to send email to $EMAIL_TO."
  fi
done

echo "Email sending process completed."
