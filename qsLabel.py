from PySide6.QtWidgets import QLabel, QTextEdit
from PySide6.QtGui import QPainter, QMouseEvent, QPaintEvent, QPen, QColor, QFont, QImage, QPixmap
from PySide6.QtCore import Qt, QPoint, QRect, QPointF
import math


class MyLine:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint


class MyRectangle:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint


class MyRound:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint


class MyArrow:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint


class MyText:
    def __init__(self, mText, mRect):
        self.mText = mText
        self.mRect = mRect


class QSLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.ispressed = False
        self.isdrawline = False
        self.isdrawrectangle = False
        self.isdrawround = False
        self.istextedit = False
        self.isdrawarrow = False
        self.isreturnedit = False
        self.isdrawmosaic = False  # 是否启用马赛克功能
        self.mosaicBrushSize = 20  # 小圆球的直径
        self.m_plaintextedit = QTextEdit(self)
        self.m_plaintextedit.hide()
        self.m_plaintextedit.resize(60, 40)
        palette = self.m_plaintextedit.palette()
        palette.setBrush(self.m_plaintextedit.backgroundRole(), QColor(255, 0, 0, 0))
        self.m_plaintextedit.setPalette(palette)
        self.m_plaintextedit.setStyleSheet(
            "QTextEdit { background-color: transparent;border: 1px solid red;font-family: 'Microsoft YaHei';font-size: 14px;color: #ff0000; }")
        self.m_plaintextedit.textChanged.connect(self.on_text_changed)
        self.lines = []
        self.mosaicPath = []  # 记录鼠标移动轨迹
        self.mosaicTempPath = []
        self.temp_line = []  # 新增：存储当前鼠标拖动中的线段
        self.rectangles = []
        self.rounds = []
        self.texts = []
        self.arrows = []
        self.actionVec = []
        self.selectimage = QImage()
        self.startPoint = QPoint(0, 0)
        self.endPoint = QPoint(0, 0)

    def on_text_changed(self):
        if len(self.m_plaintextedit.toPlainText()) < 10:
            self.m_plaintextedit.resize(len(self.m_plaintextedit.toPlainText()) * 10 + 50, 40)
        else:
            self.m_plaintextedit.resize(len(self.m_plaintextedit.toPlainText()) * 15 + 20,
                                        self.m_plaintextedit.document().size().height() + 10)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isdrawline or self.isdrawrectangle or self.isdrawround or self.istextedit or self.isdrawarrow:
            self.setCursor(Qt.CrossCursor)
        if self.ispressed:
            if self.isdrawline:
                self.endPoint = event.pos()
                line = MyLine(self.startPoint, self.endPoint)
                self.temp_line.append(line)  # 暂存当前线段
                self.startPoint = self.endPoint
            elif self.isdrawrectangle or self.isdrawround or self.isdrawarrow:
                self.endPoint = event.pos()
            elif self.isdrawmosaic:
                self.mosaicTempPath.append(event.pos())
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        self.startPoint = event.pos()
        self.endPoint = event.pos()
        self.ispressed = True
        if self.istextedit:
            if self.m_plaintextedit.toPlainText():
                text = MyText(self.m_plaintextedit.toPlainText(),
                              QRect(QPoint(self.m_plaintextedit.x(), self.m_plaintextedit.y()),
                                    self.m_plaintextedit.size()))
                self.texts.append(text)
                self.actionVec.append("text")
                self.update()
            self.m_plaintextedit.move(self.startPoint)
            self.m_plaintextedit.show()
            self.m_plaintextedit.clear()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.ispressed = False
        if self.isdrawline:
            self.lines.append(self.temp_line.copy())  # 将整段线保存到 lines
            self.actionVec.append("lines")
            self.temp_line.clear()  # 清空临时线段列表
            self.update()
        elif self.isdrawrectangle:
            self.endPoint = event.pos()
            rectangle = MyRectangle(self.startPoint, self.endPoint)
            self.rectangles.append(rectangle)
            self.actionVec.append("rectangles")
            self.update()
        elif self.isdrawround:
            self.endPoint = event.pos()
            round_ = MyRound(self.startPoint, self.endPoint)
            self.rounds.append(round_)
            self.actionVec.append("rounds")
            self.update()
        elif self.isdrawarrow:
            self.endPoint = event.pos()
            arrow = MyArrow(self.startPoint, self.endPoint)
            self.arrows.append(arrow)
            self.actionVec.append("arrows")
            self.update()
        elif self.isdrawmosaic:
            self.mosaicPath.append(self.mosaicTempPath.copy())  # 将当前马赛克路径保存到 mosaicPaths
            self.actionVec.append("mosaic")
            self.mosaicTempPath.clear()  # 清空临时马赛克路径
            self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.selectimage)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(Qt.red))
        pen.setWidth(2)
        painter.setPen(pen)
        # 绘制马赛克
        for path in self.mosaicPath:
            for point in path:
                self.applyMosaic(point, painter)

        # 绘制临时马赛克
        for point in self.mosaicTempPath:
            self.applyMosaic(point, painter)

        for line_segment in self.lines:  # 修改：遍历线段集合
            for line in line_segment:
                painter.drawLine(line.startPoint, line.endPoint)
        for line in self.temp_line:  # 临时线段也需要绘制
            painter.drawLine(line.startPoint, line.endPoint)
        for rectangle in self.rectangles:
            x1 = min(rectangle.startPoint.x(), rectangle.endPoint.x())
            y1 = min(rectangle.startPoint.y(), rectangle.endPoint.y())
            painter.drawRect(x1, y1, abs(rectangle.endPoint.x() - rectangle.startPoint.x()),
                             abs(rectangle.endPoint.y() - rectangle.startPoint.y()))
        for round_ in self.rounds:
            x2 = min(round_.startPoint.x(), round_.endPoint.x())
            y2 = min(round_.startPoint.y(), round_.endPoint.y())
            painter.drawEllipse(x2, y2, abs(round_.endPoint.x() - round_.startPoint.x()),
                                abs(round_.endPoint.y() - round_.startPoint.y()))
        for arrow in self.arrows:
            self.draw_arrow(arrow.startPoint, arrow.endPoint, painter)
        for text in self.texts:
            painter.drawText(text.mRect, Qt.TextWrapAnywhere, text.mText)
        if self.isdrawrectangle:
            x1 = min(self.startPoint.x(), self.endPoint.x())
            y1 = min(self.startPoint.y(), self.endPoint.y())
            painter.drawRect(x1, y1, abs(self.endPoint.x() - self.startPoint.x()),
                             abs(self.endPoint.y() - self.startPoint.y()))
        elif self.isdrawround:
            x2 = min(self.startPoint.x(), self.endPoint.x())
            y2 = min(self.startPoint.y(), self.endPoint.y())
            painter.drawEllipse(x2, y2, abs(self.endPoint.x() - self.startPoint.x()),
                                abs(self.endPoint.y() - self.startPoint.y()))
        elif self.isdrawarrow:
            self.draw_arrow(self.startPoint, self.endPoint, painter)

    def applyMosaic(self, center: QPoint, painter: QPainter, block_size: int = 10, ):
        brush_radius = self.mosaicBrushSize // 2

        for y in range(center.y() - brush_radius, center.y() + brush_radius, block_size):
            for x in range(center.x() - brush_radius, center.x() + brush_radius, block_size):
                # 只处理圆形区域内的像素
                if (x - center.x()) ** 2 + (y - center.y()) ** 2 <= brush_radius ** 2:
                    block = QRect(x, y, block_size, block_size)
                    color = QColor(self.selectimage.pixel(block.center()))  # 获取该区域的颜色
                    painter.fillRect(block, color)  # 用颜色填充马赛克区域

    def draw_arrow(self, start_point: QPoint, end_point: QPoint, painter: QPainter):
        par = 15.0
        slope = math.atan2((end_point.y() - start_point.y()), (end_point.x() - start_point.x()))
        cos_slope = math.cos(slope)
        sin_slope = math.sin(slope)
        point1 = QPoint(end_point.x() + int(-par * cos_slope - (par / 2.0 * sin_slope)),
                        end_point.y() + int(-par * sin_slope + (par / 2.0 * cos_slope)))
        point2 = QPoint(end_point.x() + int(-par * cos_slope + (par / 2.0 * sin_slope)),
                        end_point.y() - int(par / 2.0 * cos_slope + par * sin_slope))
        points = [end_point, point1, point2]
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(QColor(Qt.red))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPolygon(points)
        offset_x = int(par * sin_slope / 3)
        offset_y = int(par * cos_slope / 3)
        point3 = QPoint(end_point.x() + int(-par * cos_slope - (par / 2.0 * sin_slope)) + offset_x,
                        end_point.y() + int(-par * sin_slope + (par / 2.0 * cos_slope)) - offset_y)
        point4 = QPoint(end_point.x() + int(-par * cos_slope + (par / 2.0 * sin_slope) - offset_x),
                        end_point.y() - int(par / 2.0 * cos_slope + par * sin_slope) + offset_y)
        arr_body_points = [start_point, point3, point4]
        painter.drawPolygon(arr_body_points)

    def setImageToLabel(self, image: QImage):
        self.selectimage = image
        self.endPoint = QPoint(0, 0)
        self.startPoint = QPoint(0, 0)

    def setDrawLineEnable(self):
        self.setTextEditTovector()
        self.isdrawline = True
        self.isdrawrectangle = False
        self.isdrawround = False
        self.istextedit = False
        self.isdrawarrow = False
        self.isreturnedit = False
        self.isdrawmosaic = False
        self.m_plaintextedit.hide()

    def setRectangleEnable(self):
        self.setTextEditTovector()
        self.isdrawline = False
        self.isdrawrectangle = True
        self.isdrawround = False
        self.istextedit = False
        self.isdrawarrow = False
        self.isreturnedit = False
        self.isdrawmosaic = False
        self.m_plaintextedit.hide()

    def setDrawArrowEnable(self):
        self.setTextEditTovector()
        self.isdrawline = False
        self.isdrawarrow = True
        self.isdrawrectangle = False
        self.isdrawround = False
        self.istextedit = False
        self.isreturnedit = False
        self.isdrawmosaic = False
        self.m_plaintextedit.hide()

    def setRoundEnable(self):
        self.setTextEditTovector()
        self.isdrawline = False
        self.isdrawrectangle = False
        self.isdrawround = True
        self.isdrawarrow = False
        self.istextedit = False
        self.isreturnedit = False
        self.isdrawmosaic = False
        self.m_plaintextedit.hide()

    def setTextEditEnable(self):
        self.setTextEditTovector()
        self.isdrawline = False
        self.isdrawrectangle = False
        self.isdrawround = False
        self.isdrawarrow = False
        self.istextedit = True
        self.isreturnedit = False
        self.isdrawmosaic = False
        self.m_plaintextedit.hide()

    def setMosaicEnable(self):
        self.setTextEditTovector()
        self.isdrawline = False
        self.isdrawrectangle = False
        self.isdrawround = False
        self.isdrawarrow = False
        self.istextedit = False
        self.isdrawmosaic = True
        self.isreturnedit = False
        self.m_plaintextedit.hide()

    def setTextEditTovector(self):
        if self.istextedit and self.m_plaintextedit.toPlainText():
            text = MyText(self.m_plaintextedit.toPlainText(),
                          QRect(QPoint(self.m_plaintextedit.x(), self.m_plaintextedit.y()),
                                self.m_plaintextedit.size()))
            self.texts.append(text)
            self.update()

    def setReturnEditEnable(self):
        self.isreturnedit = True
        if self.actionVec:
            action = self.actionVec.pop()
            if action == "rectangles":
                self.rectangles.pop()
            elif action == "rounds":
                self.rounds.pop()
            elif action == "arrows":
                self.arrows.pop()
            elif action == "lines":
                self.lines.pop()
            elif action == "mosaic":
                self.mosaicPath.pop()
            elif action == "text":
                self.texts.pop()
            self.update()
        self.m_plaintextedit.hide()

    def resultImage(self):
        return QImage(self.grab().toImage())

    def resultPixmap(self):
        return self.grab()
