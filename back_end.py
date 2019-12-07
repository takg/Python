import os
import face_recognition
import cv2


def get_files_from_folder(folder):
    names = get_folders_from_folder(folder)
    files = {}
    for name in names:
        path = folder + '/' + name + '/'
        files[name] = [path + x for x in os.listdir(path)]

    return files


def get_folders_from_folder(folder):
    folders = os.listdir(folder)
    return [x for x in folders]


def encode_faces(image_files):
    knownEncodings = []
    knownNames = []
    for name in image_files.keys():
        for image_path in image_files[name]:
            image_path = image_path.replace('/', '\\\\')
            #print(name, image_path)
            encodings, boxes, image = encode_face(image_path)
            # loop over the encodings
            #print('abc')
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                #print('def')
                knownEncodings.append(encoding)
                #print('ghi')
                knownNames.append(name)

    return knownNames, knownEncodings

def encode_face(image_path):
    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    print('Encoding image ', image_path, '...')
    image = cv2.imread(image_path, 1)
    #rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    # model = cnn, hog
    #The CNN method is more accurate but slower. HOG is faster but less accurate.
    boxes = face_recognition.face_locations(image, model="cnn")
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(image, boxes)

    return encodings, boxes, image


def recognize_face(image_path, known_names, known_encoding):
    encodings, boxes, image = encode_face(image_path.replace("/", "\\\\"))
    names = []

    print("Starting face recognition...")
    #print(type(encodings), len(encodings))
    #print(type(known_encoding), len(known_encoding))
    #print(type(known_names), len(known_names))

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        #print("one")
        #print(known_encoding[0])
        matches = face_recognition.compare_faces(known_encoding, encoding)
        name = "Unknown"
        #print(name)
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matched_ids = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matched_ids:
                name = known_names[i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)

    print(names)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)