import face_recognition
import cv2
import os
import pickle
import csv
import platform

def clear_terminal():
    # Clear terminal screen based on platform
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def display_recognized_person(frame, name, face_location):
    # Draw a rectangle around the detected face
    top, right, bottom, left = face_location
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the name of the recognized person
    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display the frame with the detected face
    cv2.imshow('Face Detection', frame)
    cv2.waitKey(2000)  # Show for 2 seconds

def register_faces():
    faces_directory = "faces"  # Directory where face images are stored
    all_face_encodings = {}

    # Iterate through each file in the directory
    for filename in os.listdir(faces_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            person_name = os.path.splitext(filename)[0]
            image_path = os.path.join(faces_directory, filename)

            # Load the image
            image = face_recognition.load_image_file(image_path)

            # Find face locations and encodings
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if len(face_encodings) > 0:
                # Take the first face encoding (assuming only one face per image)
                face_encoding = face_encodings[0]
                all_face_encodings[person_name] = face_encoding

    # Save the face encodings to a file
    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)

def vote(max_votes):
    # Load the saved face encodings
    with open('dataset_faces.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)

    # Initialize variables for voting
    vote_count = {'Party A': 0, 'Party B': 0, 'Party C': 0}
    recognized_users = []
    counter = 0

    video_capture = cv2.VideoCapture(0)

    while counter < max_votes:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Convert the frame to RGB color space
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all the faces in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare the face encoding with known face encodings
            matches = face_recognition.compare_faces(list(all_face_encodings.values()), face_encoding, tolerance=0.50)

            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = list(all_face_encodings.keys())[first_match_index]

            if name != "Unknown" and name not in recognized_users:
                recognized_users.append(name)

                # Display the recognized person's image
                display_recognized_person(frame, name, face_location)

                # Allow the recognized user to vote
                print("\nWelcome, {}! Please cast your vote:".format(name))
                print("1. Party A")
                print("2. Party B")
                print("3. Party C")

                while True:
                    vote_input = input("Enter your vote (1/2/3): ")

                    if vote_input in ['1', '2', '3']:
                        break
                    else:
                        print("Invalid vote choice. Please enter 1, 2, or 3.")

                # Increment the vote count based on the user's choice
                if vote_input == '1':
                    vote_count['Party A'] += 1
                elif vote_input == '2':
                    vote_count['Party B'] += 1
                elif vote_input == '3':
                    vote_count['Party C'] += 1

                # Clear the terminal after each vote
                clear_terminal()

                counter += 1  # Increment the counter after each vote

                # Close the window after voting
                cv2.destroyWindow('Face Detection')

                # Break out of the loop if the maximum votes limit is reached
                if counter >= max_votes:
                    break

        # Check for key press to exit or continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    video_capture.release()
    cv2.destroyAllWindows()

    # Write the vote count to a CSV file
    with open('votes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Party', 'Votes'])
        for party, votes in vote_count.items():
            writer.writerow([party, votes])

if __name__ == "__main__":
    #register_faces()
    max_votes = 2  # Set the maximum number of votes
    vote(max_votes)
