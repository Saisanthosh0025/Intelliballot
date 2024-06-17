import os
import random
import smtplib
import csv
from email.mime.text import MIMEText

def clear_terminal():
    # Clear terminal screen based on platform
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:
        os.system('clear')  # For Linux/MacOS

def generate_random_code():
    """Generate a random 10-character secret code."""
    characters = "abcdef@#123456789"
    return ''.join(random.choices(characters, k=10))

def send_email(receiver_email, secret_code):
    """Send an email with the secret code to the specified recipient."""
    sender_email = "intelliballot.voting@outlook.com"
    sender_password = "Sai1799@"

    # Compose the email message
    message = MIMEText(f"Your secret code is: {secret_code}")
    message['Subject'] = 'Secret Code for Voting'
    message['From'] = sender_email
    message['To'] = receiver_email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def merge_votes():
    # Read finger_votes.csv
    with open('finger_votes.csv', newline='') as finger_file:
        finger_reader = csv.DictReader(finger_file)
        finger_data = {row['Party']: int(row['Votes']) for row in finger_reader}

    # Read votes.csv
    with open('votes.csv', newline='') as votes_file:
        votes_reader = csv.DictReader(votes_file)
        for row in votes_reader:
            party = row['Party']
            votes = int(row['Votes'])
            if party in finger_data:
                finger_data[party] += votes
            else:
                finger_data[party] = votes

    # Write merged data to merged_votes.csv
    with open('merged_votes.csv', 'w', newline='') as merged_file:
        fieldnames = ['Party', 'Votes']
        merged_writer = csv.DictWriter(merged_file, fieldnames=fieldnames)
        merged_writer.writeheader()
        for party, votes in finger_data.items():
            merged_writer.writerow({'Party': party, 'Votes': votes})

def main():
    print("Welcome to the Voting System!")
    face = finger = 0
    
    while True:
        print("\nSelect an option:")
        print("1. Face Vote")
        print("2. Fingerprint Vote")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1" and face == 0:
            face += 1
            clear_terminal()
            print("Running Face Vote...")
            os.system("python face-vote.py")
            clear_terminal()
        elif choice == "2" and finger == 0:
            finger += 1
            clear_terminal()
            print("Running Fingerprint Vote...")
            os.system("python finger-vote.py")
            clear_terminal()
        elif choice == "3":
            print("Exiting...")

            # Generate random secret codes
            first_secret_code = generate_random_code()
            second_secret_code = generate_random_code()

            # Send email for the first secret code
            send_email("pichikasaisantosh2003@gmail.com", first_secret_code)
            sec1 = input("Enter the first secret code sent to your email: ")

            if sec1 == first_secret_code:
                # Send email for the second secret code
                send_email("pichikasaisantosh2003@gmail.com", second_secret_code)
                sec2 = input("Enter the second secret code sent to your email: ")

                if sec2 == second_secret_code:
                    print("Welcome, election officer! The result is running...")
                    os.system("python result.py")
                    merge_votes()  # Merge the votes after the results are obtained
                else:
                    print("Oops! The entered second secret code is wrong :(")
            else:
                print("Oops! The entered first secret code is wrong :(")
            break
        elif face == 1 or finger == 1:
            if face == 1:
                print("Face voting is already finished!")
            if finger == 1:
                print("Fingerprint voting is already finished!")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
