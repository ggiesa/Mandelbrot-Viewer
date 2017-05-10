# The script calculates and displays the mandlebrot
# set via PyQt5. Goal: implement zoom functionality

import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class mandlebrot(QWidget):


    def __init__(self):
        super().__init__()

        self.initUI()
        self.pressPos = None
        self.releasePos = None
        self.a = None
        self.b = None



    def initUI(self):
        self.setGeometry(50, 50, 600, 400)
        self.show()



    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()



    def drawPoints(self, qp):

        size = self.size()
        print(size)
        if self.releasePos:
            width = self.releasePos[0] - self.pressPos[0]
            height = width*(size.height()/size.width())
        else:
            width = size.width()
            height = size.height()
            self.a = -2
            self.b = 1


        for i in range(1, size.width() -1):

            x = self.a + 3*((i-1)/(size.width()-1))

            for ii in range( 1, size.height() -1):

                y = self.b - 2*((ii-1)/(height-1))


                color = self.mandlebrotColor(x,y)
                qp.setPen(QColor(color[0], color[1], color[2]))
                qp.drawPoint(i, ii)



    def mandlebrotColor(self, a, b):
        c = complex(a,b)
        z = complex(0,0)

        # If the number does not blow up in 100 iterations, point is in set and is colored black.
        # Otherwise point is excluded from set and color is white
        for i in range(100):
            z = z**2 + c
            if abs(z) >= 2:
                return [80 + i, 140, 150 + i]
        return [0,0,0]



    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        pos = [x,y]

        self.pressPos = pos



    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        pos = [x,y]

        self.releasePos = pos
        if self.pressPos != self.releasePos:
            self.update()
        else:
            None

    def drawRect(self, qp):

        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        if self.releasePos:
            xstart = self.pressPos[0]
            ystart = self.pressPos[1]
            width = self.releasePos[0] - xstart
            height = self.releasePos[1] - ystart
            qp.drawRect(xstart, ystart, width , height)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mandlebrot()
    sys.exit(app.exec_())
