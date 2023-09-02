import csv
import os

# Specify the input CSV file and the output delimiter
input_file = r'c:\Users\5\AppData\Local\Programs\Python\Python311\projects\css_public_all_ofos_locations.csv'
output_delimiter = '\x01'  # Ctrl + A character
output_file = 'delimited_data.csv'  # Name of the output CSV file

# Get the directory path of the input file
input_directory = os.path.dirname(input_file)

# Construct the full path of the output file in the same directory
output_file_path = os.path.join(input_directory, output_file)

# Open the input CSV file and read its contents
with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader object with the specified delimiter
    csvreader = csv.reader(csvfile, delimiter=output_delimiter)
    
    # Initialize a counter for the number of processed rows
    row_count = 0
    
    # Create a new output CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        # Create a CSV writer object for the output file
        csvwriter = csv.writer(outfile)
        
        # Loop through each row in the input CSV file
        for row in csvreader:
            # Write the row to the output CSV file
            csvwriter.writerow(row)
            
            # Increment the row count
            row_count += 1
            