import time
import csv
import os
import platform
import struct
from pyfingerprint.pyfingerprint import PyFingerprint

def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def load_registered_fingerprints():
    registered_templates = []
    registered_names = []

    try:
        with open('registered_fingerprints.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                registered_names.append(row[0])
                fingerprint = bytes.fromhex(row[1])
                registered_templates.append(fingerprint)
    except Exception as e:
        print("Error occurred while loading registered fingerprints:", e)
        return None, None

    return registered_names, registered_templates

def authenticate_fingerprint(input_template, registered_templates, registered_names, finished_voting):
    if finished_voting:
        print("Voting has already finished. Please try again later.")
        time.sleep(2)
        return None

    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return None

    print('Place finger on sensor...')
    while not f.readImage():
        pass

    f.convertImage(0x01)
    print('Remove finger...')
    time.sleep(2)

    print('Place same finger again...')
    while not f.readImage():
        pass

    f.convertImage(0x02)

    f.uploadCharacteristics(0x02, input_template)

    for i, template in enumerate(registered_templates):
        f.uploadCharacteristics(0x01, template)
        if f.compareCharacteristics() == 0:
            print('Fingerprint recognized successfully!')
            return registered_names[i]

    print('Fingerprint not recognized or user not registered!')
    return None

def vote(max_votes, registered_templates, registered_names):
    vote_count = {'Party A': 0, 'Party B': 0, 'Party C': 0}

    counter = 0
    finished_voting = False

    while counter < max_votes:
        clear_terminal()
        print("Please authenticate with your registered fingerprint (Vote {}/{}).".format(counter+1, max_votes))
        name = authenticate_fingerprint(registered_templates[counter], registered_templates, registered_names, finished_voting)
        if name:
            print(f"\nWelcome, To voting System")
            print("\nPlease cast your vote:")
            print("1. Party A")
            print("2. Party B")
            print("3. Party C")
            
            vote_input = input("Enter your vote (1/2/3): ")
            
            if vote_input in ['1', '2', '3']:
                if vote_input == '1':
                    vote_count['Party A'] += 1
                elif vote_input == '2':
                    vote_count['Party B'] += 1
                elif vote_input == '3':
                    vote_count['Party C'] += 1
                
                counter += 1
                print("Your vote has been recorded.")
            else:
                print("Invalid vote choice. Please enter 1, 2, or 3.")
            time.sleep(2)  # Add delay before proceeding to next vote
        else:
            print("Authentication failed or user not registered. Please try again with a different fingerprint.")

        if counter == max_votes:
            finished_voting = True

    try:
        with open('finger_votes.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Party', 'Votes'])
            for party, votes in vote_count.items():
                writer.writerow([party, votes])
        print("Voting completed. Results saved to finger_votes.csv")
    except Exception as e:
        print("Error occurred while writing to finger_votes.csv:", e)

    # Clear terminal after voting
    clear_terminal()

if __name__ == "__main__":
    max_votes = 3  # Adjust the number of votes based on the number of registered fingerprints
    print("Welcome to the Voting System!")
    print("Please authenticate with your registered fingerprint to cast your vote.")
    
    registered_names, registered_templates = load_registered_fingerprints()

    if registered_templates:
        print("Fingerprint loading completed.")
        vote(max_votes, registered_templates, registered_names)
    else:
        print("Fingerprint loading failed. Please check the registered_fingerprints.csv file.")
