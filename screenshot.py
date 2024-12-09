import random
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from PySide6.QtGui import QPainter, QPixmap, QPainterPath, QColor
from PySide6.QtCore import Qt, QRectF, QPoint, QRect
from controlWidget import ControlWidget
from qsLabel import QSLabel
from myRect import MyRect


class Screen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap()
        self.pressedPoint = QPoint()
        self.movePoint = QPoint()
        self.globalPath = QPainterPath()
        self.oncePress = True
        self.widthInfoRect = MyRect()
        self.rect1 = QRectF()
        self.rect2 = QRectF()
        self.rect3 = QRectF()
        self.rect4 = QRectF()
        self.rect = QRectF()
        self.type = Type.NO
        self.oldPoint = QPoint()
        self.control = None
        self.controlUi = None
        self.style = None
        self.styleUi = None
        self.rec = QRect()
        self.labelimage = QSLabel(self)

        # 获取所有屏幕信息
        screens = QApplication.screens()
        self.combined_geometry = QRect()
        for screen in screens:
            self.combined_geometry = self.combined_geometry.united(screen.geometry())

        # 创建全屏截图
        self.pixmap = QPixmap(self.combined_geometry.size())
        painter = QPainter(self.pixmap)
        for screen in screens:
            geometry = screen.geometry()
            screen_pixmap = screen.grabWindow(0)
            # 将每个屏幕的截图绘制到全局 pixmap 的相应位置
            painter.drawPixmap(
                geometry.topLeft() - self.combined_geometry.topLeft(),
                screen_pixmap
            )
        painter.end()

        self.globalPath.lineTo(self.pixmap.width(), 0)
        self.globalPath.lineTo(self.pixmap.width(), self.pixmap.height())
        self.globalPath.lineTo(0, self.pixmap.height())
        self.globalPath.lineTo(0, 0)

        self.setGeometry(self.combined_geometry)

        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.setPen(Qt.blue)
        painter.setBrush(QColor(0, 0, 0, 100))
        path = self.getPath()
        painter.drawPath(path)
        self.widthInfoRect.drawMe(painter)
        self.drawControlArea(painter)

    def drawControlArea(self, painter):
        rect1 = QRectF(self.movePoint.x() - 3, self.pressedPoint.y() - 3, 6, 6)
        rect2 = QRectF(self.pressedPoint.x() - 3, self.pressedPoint.y() - 3, 6, 6)
        rect3 = QRectF(self.pressedPoint.x() - 3, self.movePoint.y() - 3, 6, 6)
        rect4 = QRectF(self.movePoint.x() - 3, self.movePoint.y() - 3, 6, 6)
        painter.save()
        painter.setBrush(Qt.blue)
        painter.drawRect(rect1)
        painter.drawRect(rect2)
        painter.drawRect(rect3)
        painter.drawRect(rect4)
        painter.restore()

    def getPath(self):
        path = QPainterPath()
        path.moveTo(self.pressedPoint.x(), self.pressedPoint.y())
        path.lineTo(self.movePoint.x(), self.pressedPoint.y())
        path.lineTo(self.movePoint.x(), self.movePoint.y())
        path.lineTo(self.pressedPoint.x(), self.movePoint.y())
        path.lineTo(self.pressedPoint.x(), self.pressedPoint.y())
        return self.globalPath.subtracted(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.oncePress:
            self.pressedPoint = event.position()
        else:
            self.oldPoint = event.position()

    def mouseReleaseEvent(self, event):
        self.oncePress = False
        if not self.control:
            self.control = QWidget(self)
            self.controlUi = ControlWidget(self.control)
            layout = QVBoxLayout()
            layout.addWidget(self.controlUi)
            layout.setContentsMargins(0, 0, 0, 0)
            self.control.setLayout(layout)
            self.control.setObjectName("control")
            self.control.setStyleSheet("QWidget#control{background-color: #eaecf0;}")
            self.controlUi.setScreenQuote(self)
        self.control.setGeometry(self.movePoint.x() - 543, self.movePoint.y() + 6, 543, 50)
        self.control.show()

    def mouseMoveEvent(self, event):
        tempPoint = event.position()
        self.setselectimagelabel(event)

        if event.buttons() & Qt.LeftButton:
            x = abs(self.movePoint.x() - self.pressedPoint.x())
            y = abs(self.movePoint.y() - self.pressedPoint.y())
            self.widthInfoRect.setText(f"{x} * {y}")
            if self.comparePoint(self.pressedPoint, self.movePoint):
                self.widthInfoRect.setLocation(self.pressedPoint.x(), self.pressedPoint.y())
                rect = QRectF(self.pressedPoint.x(), self.pressedPoint.y(), self.movePoint.x() - self.pressedPoint.x(), self.movePoint.y() - self.pressedPoint.y())
            else:
                self.widthInfoRect.setLocation(self.movePoint.x(), self.movePoint.y())
                rect = QRectF(self.movePoint.x(), self.movePoint.y(), self.pressedPoint.x() - self.movePoint.x(), self.pressedPoint.y() - self.movePoint.y())

            if self.oncePress:
                self.movePoint = event.position()
            else:
                if self.control:
                    self.control.hide()
                moveX = tempPoint.x() - self.oldPoint.x()
                moveY = tempPoint.y() - self.oldPoint.y()
                if self.type == Type.RECT1:
                    self.pressedPoint.setY(self.pressedPoint.y() + moveY)
                    self.movePoint.setX(self.movePoint.x() + moveX)
                elif self.type == Type.RECT2:
                    self.pressedPoint.setX(self.pressedPoint.x() + moveX)
                    self.pressedPoint.setY(self.pressedPoint.y() + moveY)
                elif self.type == Type.RECT3:
                    self.pressedPoint.setX(self.pressedPoint.x() + moveX)
                    self.movePoint.setY(self.movePoint.y() + moveY)
                elif self.type == Type.RECT4:
                    self.movePoint.setX(self.movePoint.x() + moveX)
                    self.movePoint.setY(self.movePoint.y() + moveY)
                elif self.type == Type.RECT:
                    tempPressX = self.pressedPoint.x() + moveX
                    tempPressY = self.pressedPoint.y() + moveY
                    tempMoveX = self.movePoint.x() + moveX
                    tempMoveY = self.movePoint.y() + moveY
                    deskWidth = self.pixmap.width()
                    deskHeight = self.pixmap.height()
                    if tempPressX < 0:
                        tempPressX = 0
                        tempMoveX = self.movePoint.x()
                    if tempPressX > deskWidth:
                        tempPressX = deskWidth
                    if tempPressY < 0:
                        tempPressY = 0
                        tempMoveY = self.movePoint.y()
                    if tempPressY > deskHeight:
                        tempPressY = deskHeight
                    if tempMoveX < 0:
                        tempMoveX = 0
                    if tempMoveX > deskWidth:
                        tempMoveX = deskWidth
                        tempPressX = self.pressedPoint.x()
                    if tempMoveY < 0:
                        tempMoveY = 0
                    if tempMoveY > deskHeight:
                        tempMoveY = deskHeight
                        tempPressY = self.pressedPoint.y()
                    self.pressedPoint.setX(tempPressX)
                    self.pressedPoint.setY(tempPressY)
                    self.movePoint.setX(tempMoveX)
                    self.movePoint.setY(tempMoveY)
                self.oldPoint = tempPoint
        else:
            self.type = self.pointInWhere(event.position())
            if self.type == Type.RECT1:
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.type == Type.RECT2:
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.type == Type.RECT3:
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.type == Type.RECT4:
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.type == Type.RECT:
                self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        self.repaint()

    def compareRect(self, r1, r2):
        return False

    def pointInWhere(self, p):
        if self.pointInRect(p, self.rect1):
            return Type.RECT1
        elif self.pointInRect(p, self.rect2):
            return Type.RECT2
        elif self.pointInRect(p, self.rect3):
            return Type.RECT3
        elif self.pointInRect(p, self.rect4):
            return Type.RECT4
        elif self.pointInRect(p, self.rect):
            return Type.RECT
        else:
            return Type.NO

    def pointInRect(self, p, r):
        return r.contains(p)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key in [Qt.Key_Enter, Qt.Key_Return]:
            if self.controlUi:
                self.controlUi.finishBtn_slot()

    def comparePoint(self, p1, p2):
        return p1.x() < p2.x() and p1.y() < p2.y()

    def setselectimagelabel(self, event):
        wid = abs(self.movePoint.x() - self.pressedPoint.x())
        hei = abs(self.movePoint.y() - self.pressedPoint.y())
        x = min(self.pressedPoint.x(), self.movePoint.x())
        y = min(self.pressedPoint.y(), self.movePoint.y())
        selectimage = self.pixmap.copy(x, y, wid, hei).toImage()
        self.labelimage.setImageToLabel(selectimage)
        self.labelimage.setFixedSize(wid, hei)
        self.labelimage.move(QPoint(x, y))
        self.labelimage.show()

    def savePixmap(self):
        picName = ''
        # 获取当前时间
        current_time = datetime.now()
        # 设置随机数种子
        seed = current_time.microsecond + current_time.second * 1000
        random.seed(seed)
        # 生成随机数并转换为字符串
        randStr = str(random.randint(0, 2 ** 31 - 1))
        picName += randStr
        filename = QFileDialog.getSaveFileName(self, "保存截图", picName, "JPEG Files (*.jpg)")
        print(filename[0])
        if filename[0]:
            pimage = self.labelimage.resultImage()
            pimage.save(filename[0], "jpg")

    def getGrabPixmap(self):
        return self.pixmap.copy(self.pressedPoint.x(), self.pressedPoint.y(), self.movePoint.x() - self.pressedPoint.x(), self.movePoint.y() - self.pressedPoint.y())

    def drawline(self):
        self.labelimage.setDrawLineEnable()

    def textedit(self):
        self.labelimage.setTextEditEnable()

    def drawarrow(self):
        self.labelimage.setDrawArrowEnable()

    def drawmosaic(self):
        self.labelimage.setMosaicEnable()

    def returnEdit(self):
        self.labelimage.setReturnEditEnable()

    def drawround(self):
        self.labelimage.setRoundEnable()

    def drawrectang(self):
        self.labelimage.setRectangleEnable()

    def Exit(self):
        if self.labelimage:
            self.labelimage.close()

class Type:
    RECT1 = 0
    RECT2 = 1
    RECT3 = 2
    RECT4 = 3
    RECT = 4
    NO = 5

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Screen()
    screen.show()
    sys.exit(app.exec())
