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
        self.xintervalStart = None
        self.xintervalEnd = None
        self.yintervalStart = None
        self.yintervalEnd = None



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

        # If user has selected an area to zoom in on, calculate new interval to iterate function over
        if self.releasePos:
            x1 = self.xintervalStart + (self.xintervalEnd - self.xintervalStart)*((self.pressPos[0]-1)/(size.width()-1))
            x2 = self.xintervalStart + (self.xintervalEnd - self.xintervalStart)*((self.releasePos[0]-1)/(size.width()-1))
            y1 = self.yintervalStart - (self.yintervalStart - self.yintervalEnd)*((self.pressPos[1]-1)/(size.height()-1))
            y2 = self.yintervalStart - (self.yintervalStart - self.yintervalEnd)*((self.releasePos[1]-1)/(size.height()-1))

            self.xintervalStart = x1
            self.xintervalEnd = x2
            self.yintervalStart = y1
            self.yintervalEnd = y2

        # If program has just been initialized, use the fully 'zoomed out' interval:  (-2 < x < 1) and (-1 < y < 1)
        else:
            self.xintervalStart = -2
            self.xintervalEnd = 1
            self.yintervalEnd = -1
            self.yintervalStart = 1

            x1 = self.xintervalStart
            x2 = self.xintervalEnd
            y1 = self.yintervalStart
            y2 = self.yintervalEnd

        # i and ii loop over every horizontal and vertical pixel coordinate in the widget, filling in an image. x and y are the
        # actual values that are used in the mandlebrot function. For each pixel, mandlebrotColor is called, iterating the
        # mandlebrot function and assigning the pixel a color based on the 'speed' at which the function diverges
        for i in range(1, size.width() -1):
            x = x1 + (x2 - x1)*((i-1)/(size.width()-1))

            for ii in range( 1, size.height() -1):
                y = y1 - (y1 - y2)*((ii-1)/(size.height()-1))

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
