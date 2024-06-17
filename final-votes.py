import csv

def merge_csv_files(file1, file2, output_file):
    # Dictionary to store Party as key and Votes as value
    party_votes = {}

    # Read data from finger-votes.csv
    with open(file1, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            party = row[0]
            votes = int(row[1])
            if party not in party_votes:
                party_votes[party] = votes
            else:
                party_votes[party] += votes

    # Read data from votes.csv
    with open(file2, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            party = row[0]
            votes = int(row[1])
            if party not in party_votes:
                party_votes[party] = votes
            else:
                party_votes[party] += votes

    # Write merged data to output file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Party', 'Votes'])
        for party, votes in party_votes.items():
            writer.writerow([party, votes])

# File paths
file1 = 'finger_votes.csv'
file2 = 'votes.csv'
output_file = 'merged_votes.csv'

# Merge CSV files
merge_csv_files(file1, file2, output_file)
