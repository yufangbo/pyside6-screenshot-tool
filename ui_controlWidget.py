# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_controlWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget, QPushButton)

from qfluentwidgets import (ToolButton, TransparentToolButton, InfoBarIcon, FluentIcon)
from PySide6.QtCore import QResource
import controlWidget_rc


class Ui_ControlWidget(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(729, 72)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rectangleBtn = TransparentToolButton(Form)
        self.rectangleBtn.setObjectName(u"rectangleBtn")
        self.rectangleBtn.setIconSize(QSize(25, 25))
        self.rectangleBtn.setIcon(QIcon(":/images/images/rectangle.png"))

        self.horizontalLayout.addWidget(self.rectangleBtn)

        self.drawRoundBtn = TransparentToolButton(Form)
        self.drawRoundBtn.setObjectName(u"drawRoundBtn")
        self.drawRoundBtn.setIconSize(QSize(25, 25))
        self.drawRoundBtn.setIcon(QIcon(":/images/images/round.png"))

        self.horizontalLayout.addWidget(self.drawRoundBtn)

        self.drawLineBtn = TransparentToolButton(Form)
        self.drawLineBtn.setObjectName(u"drawLineBtn")
        self.drawLineBtn.setIconSize(QSize(25, 25))
        self.drawLineBtn.setIcon(QIcon(":/images/images/pen.png"))

        self.horizontalLayout.addWidget(self.drawLineBtn)

        self.mosaicBtn = TransparentToolButton(Form)
        self.mosaicBtn.setObjectName(u"mosaicBtn")
        self.mosaicBtn.setIconSize(QSize(25, 25))
        self.mosaicBtn.setIcon(QIcon(":/images/images/mosaic.png"))

        self.horizontalLayout.addWidget(self.mosaicBtn)

        self.arrowBtn = TransparentToolButton(Form)
        self.arrowBtn.setObjectName(u"arrowBtn")
        self.arrowBtn.setIconSize(QSize(25, 25))
        self.arrowBtn.setIcon(QIcon(":/images/images/arrow.png"))

        self.horizontalLayout.addWidget(self.arrowBtn)

        self.textEditBtn = TransparentToolButton(Form)
        self.textEditBtn.setObjectName(u"textEditBtn")
        self.textEditBtn.setIconSize(QSize(25, 25))
        self.textEditBtn.setIcon(QIcon(":/images/images/text.png"))

        self.horizontalLayout.addWidget(self.textEditBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMaximumSize(QSize(50, 50))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.returneditBtn = TransparentToolButton(Form)
        self.returneditBtn.setObjectName(u"returneditBtn")
        self.returneditBtn.setIconSize(QSize(25, 25))
        self.returneditBtn.setIcon(QIcon(":/images/images/return.png"))

        self.horizontalLayout.addWidget(self.returneditBtn)

        self.saveBtn = TransparentToolButton(Form)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setIconSize(QSize(25, 25))
        self.saveBtn.setIcon(QIcon(":/images/images/download.png"))

        self.horizontalLayout.addWidget(self.saveBtn)

        self.cancelBtn = TransparentToolButton(Form)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setIconSize(QSize(25, 25))
        self.cancelBtn.setIcon(QIcon(":/images/images/cancel.png"))

        self.horizontalLayout.addWidget(self.cancelBtn)

        self.finishBtn = TransparentToolButton(Form)
        self.finishBtn.setObjectName(u"finishBtn")
        self.finishBtn.setIconSize(QSize(25, 25))
        self.finishBtn.setIcon(QIcon(":/images/images/finish.png"))

        self.horizontalLayout.addWidget(self.finishBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi


# class ControlWidgetWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_ControlWidget()
#         self.ui.setupUi(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ControlWidgetWindow()
#     window.show()
#     sys.exit(app.exec())