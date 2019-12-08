from gui import FaceRecognitionGUI
from PyQt5.QtWidgets import QApplication
from back_end import parse_args
import sys

args = parse_args()
app = QApplication(sys.argv)
gui = FaceRecognitionGUI(args.input_path, args.output_path, args.image_path_to_be_recognized)
gui.show()
app.exec_()
