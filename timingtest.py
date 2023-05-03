from datetime import datetime, timedelta
import csv

time_str = "06:49" # Example time string without AM/PM
first_row = f"Meydan Kohan, {time_str}"
first_row_list = first_row.split(",")

print(first_row) # Print the first base time
time_format = "%H:%M" # Example time format with 24-hour notation
max_iterations = 51 # Example maximum number of iterations

# Parse the time string and convert it to datetime object
time_obj = datetime.strptime(time_str, time_format)

with open('El-Goli-Line.csv', mode='a', newline='') as file:

    writer = csv.writer(file)
    writer.writerow(first_row_list)

    for i in range(max_iterations):
        # Add 16 minutes to the time
        time_obj += timedelta(minutes=16)

        # Convert the datetime object back to string
        new_time_str = time_obj.strftime(time_format)

        row = f"Meydan Kohan, {new_time_str}"
        row_list = row.split(",")
        writer.writerow(row_list)

        print(row_list) # Print the updated time for each iteration of the loop

file.close()
