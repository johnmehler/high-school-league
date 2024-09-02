import pandas as pd
import sys

def lookup_value(file_path, search_value):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Check if the DataFrame has at least three columns
    if df.shape[1] < 3:
        print("Error: The Excel file must have at least three columns.")
        return

    # Search for the value in the first column
    matching_rows = df[df.iloc[:, 0] == search_value]

    if matching_rows.empty:
        print(f"No match found for {search_value}.")
    else:
        # Print values from the 2nd and 3rd columns for the matching rows
        for _, row in matching_rows.iterrows():
            print(f"Value in 2nd column: {row.iloc[1]}")
            print(f"Value in 3rd column: {row.iloc[2]}")

if __name__ == "__main__":
    # File path to the Excel file
    file_path = 'school-lookup.xlsx'

    # Check if the correct number of command-line arguments were provided
    if len(sys.argv) != 2:
        print("Usage: python lookup.py <search_value>")
        sys.exit(1)

    # Retrieve search value from command line arguments
    try:
        search_value = int(sys.argv[1])
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        sys.exit(1)

    # Perform the lookup
    lookup_value(file_path, search_value)
