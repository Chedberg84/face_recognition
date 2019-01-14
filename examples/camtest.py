import face_recognition
import cv2
import time

video_capture = cv2.VideoCapture('rtsp://10.0.1.43:8554/unicast')

# Load a sample picture and learn how to recognize it.
chris_image = face_recognition.load_image_file("Chris.jpg")
chris_face_encoding = face_recognition.face_encodings(chris_image)[0]

stevie_image = face_recognition.load_image_file("Stevie.jpg")
stevie_face_encoding = face_recognition.face_encodings(stevie_image)[0]

alexis_image = face_recognition.load_image_file("Alexis.jpg")
alexis_face_encoding = face_recognition.face_encodings(alexis_image)[0]

fiona_image = face_recognition.load_image_file("Fiona.jpg")
fiona_face_encoding = face_recognition.face_encodings(fiona_image)[0]

oliver_image = face_recognition.load_image_file("Oliver.jpg")
oliver_face_encoding = face_recognition.face_encodings(oliver_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    chris_face_encoding,
    stevie_face_encoding,
    alexis_face_encoding,
    fiona_face_encoding,
    oliver_face_encoding
]
known_face_names = [
    "Chris Hedberg",
    "Stevie Hedberg",
    "Alexis Hedberg",
    "Fiona Hedberg",
    "Oliver Hedberg"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    if ret:
        print("ret:true")
        #print("frame:" + str(frame))

        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        #print("small_frame:" + str(small_frame))

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = frame[:, :, ::-1]

        #print("rgb_small_frame:" + str(rgb_small_frame))

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        #face_locations = face_recognition.face_locations(frame)

        #print("face_locations:" + str(face_locations))

        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        #face_encodings = face_recognition.face_encodings(frame, face_locations)

        #print("face_encodings:" + str(face_encodings))

        face_names = []
        for face_encoding in face_encodings:

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

            print("name:" + str(name))

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #top *= 4
            #right *= 4
            #bottom *= 4
            #left *= 4

            print("Found This Person: " + name)

            # Draw a box around the face
            #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #font = cv2.FONT_HERSHEY_DUPLEX
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        #cv2.imshow('Video', frame)

    print("sleep")

    #wait 1/2 of a second?
    time.sleep(2.0)

    print("restart")

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
