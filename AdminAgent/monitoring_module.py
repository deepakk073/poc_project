from google.cloud import bigquery
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
from dotenv import load_dotenv

def fetch_slow_queries_bigquery(threshold_ms=5000):
    client = bigquery.Client()
    query = """
    SELECT job_id, user_email, query, total_slot_ms, creation_time 
    FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT 
    WHERE 
        state = 'DONE' 
        AND job_type = 'QUERY' 
        AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 HOUR) 
        AND total_slot_ms > @threshold
        limit 1
    """
    job = client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("threshold", "INT64", threshold_ms)
        ]
    ))
    return [dict(row.items()) for row in job.result()]

def generate_email_content(queries: list):
    lines = ["🚨 Slow Queries Detected in BigQuery\n\n"]
    for q in queries:
        query_url = f"https://console.cloud.google.com/bigquery?j=your_project:region:{q['job_id']}"
        abort_cmd = f"bq cancel -j {q['job_id']}"
        lines.append(
            f"""
User: {q['user_email']}
Job ID: {q['job_id']}
Slot Time: {q['total_slot_ms']} ms
URL: {query_url}
Abort: {abort_cmd}
Query:
{q['query']}
---
"""
        )
    return "\n".join(lines)
def send_email( to_email,  message_body):
    load_dotenv()
    # Create a client instance
    SENDGRID_API_KEY=os.getenv("SENDGRID_API_KEY")
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    #ssl._create_default_https_context = ssl._create_unverified_context
    # Create a Mail object
    mail = Mail(
        from_email="deepakk073@gmail.com",
        subject='"Slow Queries Alert"',
        plain_text_content=message_body
    )
    
    # Add the recipient's email address
    mail.add_to(to_email)
    
    try:
        # Send the email
        response = sg.send(mail)
        
        print(f"Email sent successfully. Response status: {response.status_code}")
        
    except Exception as e:
        print(f"Error sending email: {e}")

# # Usage example
# send_email(
#     subject="Hello from Python!",
#     to_email="deepakk073@gmail.com",
#     from_email="deepakk073@gmail.com",
#     message_body="This is a test email sent using SendGrid."
# )

# def send_email(to: str, content: str):
#     import smtplib
#     from email.mime.text import MIMEText

#     msg = MIMEText(content)
#     msg["Subject"] = "Slow Queries Alert"
#     msg["From"] = "dba@yourcompany.com"
#     msg["To"] = to

#     with smtplib.SMTP("smtp.yourcompany.com") as server:
