# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

import qrcode
import cv2
import webbrowser
import sys
import time
from pyzbar.pyzbar import decode

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("QR_code.ui", self)
        self.show()

        self.current_file = ""
        self.actionLOAD.triggered.connect(self.load_image)
        self.actionSAVE.triggered.connect(self.save_image)
        self.actionQUIT.triggered.connect(self.quit_window)
        self.pushButton.clicked.connect(self.generate_code)
        self.pushButton_2.clicked.connect(self.read_code)
        self.pushButton_3.clicked.connect(self.scan_qr)
        
    # function for loading image from device

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = (QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*)", options=options))
        print(filename)
        
        if filename != "":
            self.current_file = filename[0]
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(400, 400)
            self.label.setScaledContents(True)
            print(pixmap)
            self.label.setPixmap(pixmap)
        else:
            print("some unexpected error occurred. TRY AGAIN!!")

    #function for saving the generated qr in device

    def save_image(self):
        print("saving generated qr......")
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG (*.png)", options=options)

        if filename != "":
            img = self.label.pixmap()
            img.save(filename, "PNG")

    #function for generating the qr code

    def generate_code(self):
        print("generating qr......")
        time.sleep(1)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=2)
        qr.add_data(self.textEdit.toPlainText())
        qr.make(fit=True)

        img = qr.make_image(fill_colr="black", back_color="white")
        img.save("currentqr.png")
        pixmap = QtGui.QPixmap("currentqr.png")
        pixmap = pixmap.scaled(400, 400)
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)

    #function for reading the given qr code

    def read_code(self):
        print("reading qr.......")
        time.sleep(2)
        img = cv2.imread(self.current_file)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        if data:
            self.textEdit.setText(data)
        else:
            print("can't read the qr code!!")

    #function for scanning the qr from device camera

    def scan_qr(self):
        print("opening camera......")
        cam = cv2.VideoCapture(1)
        detector = cv2.QRCodeDetector()
        camera = True
        print("scanning...")
        while camera == True:
             _, frame = cam.read()
             data,one,_ = detector.detectAndDecode(frame)
             if data:
                self.textEdit.setText(data)
                a = data
                self.generate_code()
                break
             cv2.imshow("Scan QR", frame)
             if cv2.waitKey(1) == ord('q'):
                break
        b = webbrowser.open(str(a))
        # cam.release(a)
        cv2.destroyAllWindows()

    #function for exitting the program

    def quit_window(self):
        print("exiting.....")
        time.sleep(2)
        cv2.destroyAllWindows()
        sys.exit(0)



def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()
