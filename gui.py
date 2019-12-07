from PyQt5.QtWidgets import QLabel, QGroupBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap

from back_end import get_files_from_folder, recognize_face, encode_faces

import cv2
import datetime
import os


class FaceRecognitionGUI(QWidget):
    def __init__(self, input_path, output_path, parent=None):
        super(FaceRecognitionGUI, self).__init__(parent)

        self.input_path = input_path
        self.output_path = output_path
        self.image_files = {}
        self.combo_box = QComboBox()
        self.line_edit = QLineEdit(self)
        self.displayed_images = 0
        self.setup_home_screen()

    def get_images_from_library(self):
        self.image_files = get_files_from_folder(self.input_path)

    # sample code to test if things are working fine for PyQT
    def setup_home_screen(self):
        self.setWindowTitle('Welcome to face recognition program!')
        grid_layout = QGridLayout(self)

        grid_layout.addWidget(self.combo_box, 0, 1)
        button = QPushButton("View Library")
        button.clicked.connect(self.show_images_for_selected_name)
        grid_layout.addWidget(button, 0, 2)
        button = QPushButton("Recognize faces")
        button.clicked.connect(self.recognize_faces)
        grid_layout.addWidget(button, 0, 3)
        button = QPushButton("Exit", self)
        button.clicked.connect(self.exit)
        grid_layout.addWidget(button, 0, 4)

        grid_layout.addWidget(QLabel("Enter name", self), 1, 1)
        grid_layout.addWidget(self.line_edit, 1, 2)
        button = QPushButton("Add new faces", self)
        button.clicked.connect(self.capture_image)
        grid_layout.addWidget(button, 1, 3)
        self.setLayout(grid_layout)
        self.refresh_items_in_combo_box()

    def recognize_faces(self):
        images_path = get_files_from_folder('C:/git/github/face_recognition/pictures/live/')

        known_names, known_encoding = encode_faces(self.image_files)

        for name in images_path.keys():
            for filin images_path[name]:
                recognize_face(file, known_names, known_encoding)

    def refresh_items_in_combo_box(self):
        self.get_images_from_library()
        self.combo_box.clear()

        for name in self.image_files.keys():
            self.combo_box.addItem(name)

        self.show_images_for_selected_name()

    def show_images_for_selected_name(self):
        grid_layout = self.layout()
        self.displayed_images = len(self.image_files[self.combo_box.currentText()])
        loop = 0

        for image in self.image_files[self.combo_box.currentText()]:
            if loop > 4: # five images are good for library
                break

            label = QLabel(image)
            label.setPixmap(QPixmap(image.replace("/", "\\")))
            label.setFixedWidth(150)
            label.setFixedHeight(150)
            label.setScaledContents(True)

            grid_layout.addWidget(label, 2, loop)
            loop = loop + 1

    # for displaying the image library
    def exit(self):
        os._exit(0)

    # for capturing the images from the camera for individuals
    def capture_image(self):
        name = self.line_edit.text()
        capture = cv2.VideoCapture(0)
        full_path = self.input_path + "/" + name

        if not os.path.exists(full_path):
            os.mkdir(full_path)

        while True:
            ret, image = capture.read()
            if ret:
                cv2.imshow("Capture", image)
                # Wait to press 'q' key for capturing
                x = cv2.waitKey(1) & 0xFF
                if x == ord('c'):
                    # Set the image name to the date it was captured
                    image_name = full_path + '/' + str(
                        datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")) + '.jpg'
                    # Save the image
                    cv2.imwrite(image_name, image)
                elif x == ord('q') or x == ord('x'):
                    break

        # close and release the resources
        cv2.destroyAllWindows()
        capture.release()
        self.refresh_items_in_combo_box()
