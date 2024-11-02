import cv2
import face_recognition

known_face_encodings = []
known_face_names = []

known_person1_image = face_recognition.load_image_file('images/head.jpg')
known_person2_image = face_recognition.load_image_file('images/alex.jpg')
known_person3_image = face_recognition.load_image_file('images/dip.jpg')
known_person4_image = face_recognition.load_image_file('images/enair.jpg')


known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
known_person3_encoding = face_recognition.face_encodings(known_person3_image)[0]
known_person4_encoding = face_recognition.face_encodings(known_person4_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)
known_face_encodings.append(known_person3_encoding)
known_face_encodings.append(known_person4_encoding)

known_face_names.append("riley")
known_face_names.append("alex")
known_face_names.append("dip")
known_face_names.append("eshaan")

#webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    #finding faces in frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    #loop throught each face in frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #check if face matches any known
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "unknown"

        #finding name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        #drawing box around face and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 255), 2)

    #display resulting frame
    cv2.imshow("Video", frame)

    #breaking loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#closing
video_capture.release()
cv2.destroyAllWindows()

info_to_store = [known_face_encodings, known_face_names]
for i in range(len(known_face_encodings)):
    print(known_face_names[i])
    print(known_face_encodings[i])
    