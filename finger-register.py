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

def register_fingerprints(max_registrations):
    registered_templates = []
    registered_names = []
    
    for i in range(max_registrations):
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if not f.verifyPassword():
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            return False

        print(f'Place finger {i+1} on sensor...')
        while not f.readImage():
            pass

        f.convertImage(0x01)
        print('Remove finger...')
        time.sleep(2)

        print('Place same finger again...')
        while not f.readImage():
            pass

        f.convertImage(0x02)

        characterics = f.downloadCharacteristics()
        serialized_data = struct.pack('B'*len(characterics), *characterics)

        name = input("Enter the name of the person: ")

        registered_templates.append(serialized_data)
        registered_names.append(name)
        print(f'Fingerprint registered successfully for {name}')

    try:
        with open('registered_fingerprints.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Fingerprint'])
            for name, fingerprint in zip(registered_names, registered_templates):
                writer.writerow([name, fingerprint.hex()])
        print("Fingerprints registration completed. Data saved to registered_fingerprints.csv")
    except Exception as e:
        print("Error occurred while writing to registered_fingerprints.csv:", e)

if __name__ == "__main__":
    max_registrations = int(input("Enter the number of members to register: "))
    print("Welcome to the Fingerprint Registration System!")
    print("Please register fingerprints for all members.")
    
    register_fingerprints(max_registrations)
