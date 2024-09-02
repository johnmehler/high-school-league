import smtplib, sys, configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(spreadsheet_link, recipients):
    # Read configuration
    config = configparser.ConfigParser()
    config.read('~/config.ini')
    sender_email = config['EMAIL']['sender_email']
    sender_password = config['EMAIL']['sender_password']
    
    # Email content
    subject = "High School League Spreadsheet"
    body = f"""Hello,

    The High School League spreadsheet has been created. You can access it using the following link:

    {spreadsheet_link}

    Please let me know if you have any questions or need any assistance.

    Best regards,
    John Mehler"""

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    # Attach the body to the message
    message.attach(MIMEText(body, "plain"))

    # Create a secure connection with the server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login to the email server
            text = message.as_string()
            server.sendmail(sender_email, recipients, text)  # Send the email
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Check if the spreadsheet link and recipients are provided as command-line arguments
if len(sys.argv) < 3:
    print("Usage: python send-emails.py <spreadsheet_link> <recipient1> <recipient2> ...")
    sys.exit(1)

spreadsheet_link = sys.argv[1]
recipients = [email for email in sys.argv[2:] if email.strip()]  # Filter out empty entries

# Check if there are any valid recipients
if not recipients:
    print("No valid recipients provided.")
    sys.exit(1)

# Check if the number of recipients is even
if len(recipients) % 2 != 0:
    print("The number of recipients must be even to form complete pairs.")
    sys.exit(1)

# Send emails in pairs
try:
    for i in range(0, len(recipients), 2):
        email_pair = recipients[i:i+2]
        send_email(spreadsheet_link, email_pair)
except Exception as e:
    print(f"An error occurred while processing the email pairs: {e}")
