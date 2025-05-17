# Copyright 2021 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START eventarc_gcs_server]
import os
from flask import Flask, request
import json
from google.cloud import bigquery
import sendgrid
from sendgrid.helpers.mail import Mail
from google.cloud import bigquery 
from secerate_key import sg_key
import ssl
app = Flask(__name__)


# [END eventarc_gcs_server]


# [START eventarc_gcs_handler]
@app.route('/', methods=['POST'])
def index():
    # Gets the Payload data from the Audit Log
    content = request.json
    try:
        print(content)
        ds = content['resource']['labes']['dataset_id']
        proj = content['resource']['labels']['project_id']
        tbl = content['protoPayload']['resourceName']
        rows = int(content['protoPayload']['metadata']['tableDataChange']['insertedRowsCount'])
        if ds == 'cloud_run_tmp' and tbl.endswith('tables/aborted_email') and rows > 0:
            msg = send_email_to_aborted_user()
            return msg, 200
    except:
        # if these fields are not in the JSON, ignore
        pass
    return "ok", 200


# [END eventarc_gcs_handler]

def send_email_to_aborted_user():
    msg=""
    ssl._create_default_https_context = ssl._create_unverified_context
    client = bigquery.Client()
    query = """
    SELECT id, Email_Subject, Email_to, Email_message
    FROM `cloud_run_tmp.email_outbox`
    WHERE email_sent = 0
"""
    # Execute the query
    query_job = client.query(query)
    results = query_job.result()
    SENDGRID_API_KEY = sg_key
    def send_email(to, subject, message):
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        email = Mail(
            from_email='deepakk073@gmail.com',  # Replace with your email
            to_emails=to,
            subject=subject,
            html_content=message
        )
        try:
            response = sg.send(email)
            return response.status_code == 202  # 202 indicates the email was accepted
        except Exception as e:
            print(f"Error sending email to {to}: {e}")
            msg=msg+"Line no - 81"+"Error sending email to {to}: {e}"
            return False
    sent_email_ids = []
    # Send emails and collect ids of sent emails
    for row in results:
        if send_email(row.Email_to, row.Email_Subject, row.Email_message):
            sent_email_ids.append(row.id)
        else:
            print(f"Failed to send email to {row.Email_to}")
            msg=msg+"Line no - 90"+"Failed to send email to {row.Email_to}"

    # Update the BigQuery table to mark emails as sent
    if sent_email_ids:
        update_query = """
            UPDATE `cloud_run_tmp.email_outbox`
            SET email_sent = 1
            WHERE id IN UNNEST(@ids)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("ids", "INT64", sent_email_ids)
            ]
        )
        update_job = client.query(update_query, job_config=job_config)
        update_job.result()  # Wait for the job to complete

        print(f"Updated {len(sent_email_ids)} records to mark emails as sent.")
        msg=msg+"Line no - 108"+"Updated {len(sent_email_ids)} records to mark emails as sent."
    else:
        print("No emails were sent.")
        msg=msg+"Line no - 111"+"No emails were sent."
    return msg


# [START eventarc_gcs_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END eventarc_gcs_server]
