import csv
from collections import defaultdict

def summarize_daily_hours(log_file):
    # Dictionary to store total minutes per user per date
    daily_summary = defaultdict(lambda: defaultdict(int))  # {user_id: {date: total_minutes}}

    # Read the log file
    try:
        with open(log_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_id = row["User ID"]
                date = row["Date"]
                time_spent = float(row["Time Spent (minutes)"])
                daily_summary[user_id][date] += time_spent

    except FileNotFoundError:
        print(f"Error: File {log_file} not found.")
        return

    '''# Generate the summary report
    print("Daily Summary Report (Hours):")
    print("User ID     Date           Total Hours")
    print("--------------------------------------")
    for user_id, dates in daily_summary.items():
        for date, total_minutes in dates.items():
            #total_hours = total_minutes // 60  # Convert minutes to full hours
            print(f"{user_id:<11} {date:<13} {total_minutes:>10}h") #Changed to minutes'''
    
    #Save the summary to a file
    with open("daily_summary.csv", "w") as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(["User ID", "Date", "Total Hours"])
        for user_id, dates in daily_summary.items():
            for date, total_minutes in dates.items():
                total_hours = total_minutes // 60
                writer.writerow([user_id, date, total_hours])

if __name__ == "__main__":
    log_file = "punch_clock_log_v2.csv"  # Path to your log file
    summarize_daily_hours(log_file)