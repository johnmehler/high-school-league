import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def run_gui(on_submit_callback):
    # Function to perform lookup and update the output
    def update_output(*args):
        try:
            # Retrieve the integer value from the entry box
            search_value = int(team1_code_entry.get().strip())
            
            # Call lookup.py script and get the output
            result = subprocess.run(['python', 'lookup.py', str(search_value)], capture_output=True, text=True)
            if result.returncode == 0:
                # Update the output labels with the values retrieved
                output_lines = result.stdout.split('\n')
                if len(output_lines) >= 2:
                    output_1_var.set(output_lines[0].replace('Value in 2nd column: ', '').strip())
                    output_2_var.set(output_lines[1].replace('Value in 3rd column: ', '').strip())
                else:
                    output_1_var.set("No data")
                    output_2_var.set("No data")
            else:
                messagebox.showerror("Error", f"Error in lookup.py:\n{result.stderr}")
        except ValueError:
            output_1_var.set("Invalid input")
            output_2_var.set("Invalid input")
        
        # Update output for team 2 code
        try:
            search_value_2 = int(team2_code_entry.get().strip())
            
            # Call lookup.py script and get the output
            result_2 = subprocess.run(['python', 'lookup.py', str(search_value_2)], capture_output=True, text=True)
            if result_2.returncode == 0:
                # Update the output labels with the values retrieved
                output_lines_2 = result_2.stdout.split('\n')
                if len(output_lines_2) >= 2:
                    output_3_var.set(output_lines_2[0].replace('Value in 2nd column: ', '').strip())
                    output_4_var.set(output_lines_2[1].replace('Value in 3rd column: ', '').strip())
                else:
                    output_3_var.set("No data")
                    output_4_var.set("No data")
            else:
                messagebox.showerror("Error", f"Error in lookup.py:\n{result_2.stderr}")
        except ValueError:
            output_3_var.set("Invalid input")
            output_4_var.set("Invalid input")
    
    # Set up the GUI
    root = tk.Tk()
    root.title("High School League")

    # Top row with match headers
    tk.Label(root, text=" ").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(root, text="Team 1:").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(root, text="Output 1").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(root, text="Output 2").grid(row=0, column=3, padx=10, pady=5)

    # Labels and Entry fields for team 1 code
    tk.Label(root, text="Team 1:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    team1_code_entry = tk.Entry(root, width=10)
    team1_code_entry.grid(row=1, column=1, padx=10, pady=5)

    # Output boxes for team 1
    output_1_var = tk.StringVar()
    output_2_var = tk.StringVar()

    tk.Label(root, textvariable=output_1_var).grid(row=1, column=2, padx=10, pady=5, sticky="e")
    tk.Label(root, textvariable=output_2_var).grid(row=1, column=3, padx=10, pady=5, sticky="e")

    # Labels and Entry fields for team 2 code
    tk.Label(root, text="Team 2:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    team2_code_entry = tk.Entry(root, width=10)
    team2_code_entry.grid(row=2, column=1, padx=10, pady=5)

    # Output boxes for team 2
    output_3_var = tk.StringVar()
    output_4_var = tk.StringVar()

    tk.Label(root, textvariable=output_3_var).grid(row=2, column=2, padx=10, pady=5, sticky="e")
    tk.Label(root, textvariable=output_4_var).grid(row=2, column=3, padx=10, pady=5, sticky="e")

    # Trace the entry fields to call update_output function on changes
    team1_code_entry_var = tk.StringVar()
    team1_code_entry_var.trace_add('write', update_output)
    team1_code_entry.config(textvariable=team1_code_entry_var)

    team2_code_entry_var = tk.StringVar()
    team2_code_entry_var.trace_add('write', update_output)
    team2_code_entry.config(textvariable=team2_code_entry_var)

    def collect_emails():
        school_pair = (
            output_1_var.get().strip(),
            output_3_var.get().strip()
        )
        email_pair = (
            output_2_var.get().strip(),
            output_4_var.get().strip()
        )
        on_submit_callback(email_pair, school_pair)

    # Submit button
    submit_button = tk.Button(root, text="Send Spreadsheets", command=collect_emails)
    submit_button.grid(row=5, column=0, columnspan=6, pady=20)

    root.mainloop()

if __name__ == "__main__":
    def dummy_callback(email_pair, school_pair):
        print(f"Submitted email pair: {email_pair}")
        print(f"Submitted school pair: {school_pair}")
    
    run_gui(dummy_callback)