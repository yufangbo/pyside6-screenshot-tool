from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen


class MyRect:
    def __init__(self, rect=None):
        """
        Constructor for MyRect.
        :param rect: Optional QRectF instance for initialization.
        """
        if rect is not None:
            self.rect = QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        else:
            self.rect = QRectF()
        self.str = ""

    def setText(self, text):
        """
        Set the text to be displayed inside the rectangle.
        :param text: Text to display.
        """
        self.str = text

    def setLocation(self, x, y):
        """
        Set the location of the rectangle and adjust its dimensions.
        :param x: x-coordinate for the rectangle.
        :param y: y-coordinate for the rectangle.
        """
        self.rect.setX(x)
        self.rect.setY(y - 21)
        self.rect.setWidth(85)
        self.rect.setHeight(21)

    def drawMe(self, painter: QPainter):
        """
        Draw the rectangle and its text using the provided QPainter.
        :param painter: QPainter instance for drawing.
        """
        painter.save()
        painter.setPen(QPen())  # Default pen
        painter.setBrush(QColor(0, 0, 0, 150))  # Semi-transparent black
        painter.drawRect(self.rect)

        # Set text color to white
        painter.setPen(QColor(255, 255, 255))
        # Draw text centered within the rectangle
        painter.drawText(self.rect, Qt.AlignCenter, self.str)
        painter.restore()
