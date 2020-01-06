from PyQt5 import QtCore, QtGui
import cv2
from pyzbar import pyzbar

class CameraThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    sendUPC = QtCore.pyqtSignal(str)

    captureVid = True

    def run(self):
        cap = cv2.VideoCapture(0)

        while self.captureVid:
            captured, frame = cap.read()

            if captured:
                if self.rotation:
                   frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                cv2.waitKey(30)


                barcodes = pyzbar.decode(frame)

                for barcode in barcodes:
                    barcodeData = barcode.data.decode('utf-8')

                    self.sendUPC.emit(barcodeData)
                    self.captureVid = False

        cap.release()
        cv2.destroyAllWindows()

    @QtCore.pyqtSlot(bool)
    def receive_rotation(self, rotation):
        self.rotation = rotation
