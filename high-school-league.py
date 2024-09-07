import subprocess
from tkinter import messagebox
import time

def run_create_sheet(email_pair, school_pair):
    result = subprocess.run(['python', 'create-sheet.py', *school_pair], capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.split('\n'):
            if line.startswith("Spreadsheet created:"):
                return line.split(": ")[1].strip()
    else:
        messagebox.showerror("Error", f"Error in create-sheet.py:\n{result.stderr}")
    return None

def run_give_access(spreadsheet_url, emails):
    if isinstance(emails, tuple):
        emails = list(emails)

    command = ['python', 'give-access.py', spreadsheet_url] + emails
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_send_emails(spreadsheet_url, emails):
    # Ensure emails is a list
    if isinstance(emails, tuple):
        emails = list(emails)

    command = ['python', 'send-emails.py', spreadsheet_url] + emails
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            messagebox.showerror("Error", f"Error in send-emails.py:\n{result.stderr}")
        else:
            print("Emails sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred while sending emails: {e}")

def on_submit(email_pair, school_pair):
    print(f"Received email pair: {email_pair}")
    print(f"Received school pair: {school_pair}")
    if not isinstance(email_pair, (tuple, list)) or len(email_pair) != 2:
        messagebox.showwarning("Warning", "Invalid input format. Please provide a tuple or list with exactly two email addresses.")
        return

    team1_email, team2_email = email_pair
    if team1_email and team2_email:
        print(f"Valid email pair: {email_pair}")

        # Create a spreadsheet for the email pair
        spreadsheet_url = run_create_sheet(email_pair, school_pair)
        if spreadsheet_url:
            # Grant access to the emails
            run_give_access(spreadsheet_url, email_pair)

            # Send emails
            run_send_emails(spreadsheet_url, email_pair)
            
            messagebox.showinfo("Success", "Spreadsheet created, access granted, and emails sent successfully")
        else:
            messagebox.showerror("Error", "Failed to create spreadsheet. Emails not sent.")
    else:
        messagebox.showwarning("Warning", "Invalid email pair. Both email addresses must be provided.")

if __name__ == "__main__":
    import gui
    gui.run_gui(on_submit)
