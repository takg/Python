from back_end import get_files_from_folder, get_folders_from_folder
from gui import FaceRecognitionGUI
from PyQt5.QtWidgets import QApplication
import sys

input_path = 'C:/git/github/face_recognition/pictures/library'
output_path = 'C:/git/github/face_recognition/pictures/output'

app = QApplication(sys.argv)
gui = FaceRecognitionGUI(input_path, output_path)
gui.show()
app.exec_()
