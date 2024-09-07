import smtplib
import sys
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

def read_config():
    config = configparser.ConfigParser()
    config_path = Path.home() / 'config.ini'
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    config.read(config_path)
    if 'EMAIL' not in config:
        raise KeyError("'EMAIL' section not found in the configuration file")
    return config['EMAIL']

def send_email(spreadsheet_link, recipients):
    try:
        email_config = read_config()
        sender_email = email_config['sender_email']
        sender_password = email_config['sender_password']
    except (FileNotFoundError, KeyError) as e:
        print(f"Configuration error: {e}")
        return

    subject = "High School League Spreadsheet"
    body = f"""
    <html>
    <body>
    <p>Team line-ups should be completed <strong>two days before the match</strong>. Please ensure that students in the line-up are registered to play for your team <strong>at least one week before the match</strong>.</p>

    <p>Students register once per academic year through:<br>
    <a href="https://chessctr.org/play/macl-player/">https://chessctr.org/play/macl-player/</a></p>

    <p>Each student must have an appropriate lichess.org account. We have assigned a school code for each school, and the username will be the school code followed by an underscore and the student's first name.<br>
    For example: <strong>Bay_George</strong> (where the school code is "Bay" and the student's first name is "George").<br>
    If a student played in a previous year, they should use their existing account rather than creating a new one.</p>

    <p>Captains and coaches from both schools should arrange a mutually acceptable time for the match. The school's dismissal times and preferred match days are listed in the spreadsheet linked below:</p>

    <p><a href="{spreadsheet_link}">Match Schedule Spreadsheet</a></p>

    <p>Thanks,<p>
    <p>John Mehler<p>
    </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    # Attach the HTML version of the message
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipients, text)
        print(f"Email sent successfully to {', '.join(recipients)}.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the email server. Please check your email and password.")
    except smtplib.SMTPException as e:
        print(f"An error occurred while sending the email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python send-emails.py <spreadsheet_link> <recipient1> <recipient2> ...")
        sys.exit(1)

    spreadsheet_link = sys.argv[1]
    recipients = [email for email in sys.argv[2:] if email.strip()]

    if not recipients:
        print("No valid recipients provided.")
        sys.exit(1)

    if len(recipients) % 2 != 0:
        print("The number of recipients must be even to form complete pairs.")
        sys.exit(1)

    for i in range(0, len(recipients), 2):
        email_pair = recipients[i:i+2]
        send_email(spreadsheet_link, email_pair)

if __name__ == "__main__":
    main()