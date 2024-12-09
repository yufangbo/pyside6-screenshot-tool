from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QClipboard
from PySide6.QtCore import Slot
from ui_controlWidget import Ui_ControlWidget


class ControlWidget(Ui_ControlWidget, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.screen = None
        self.connectSignalAndSlot()

    def connectSignalAndSlot(self):
        self.cancelBtn.clicked.connect(self.cancelBtn_slot)
        self.saveBtn.clicked.connect(self.saveBtn_slot)
        self.finishBtn.clicked.connect(self.finishBtn_slot)
        self.drawLineBtn.clicked.connect(self.on_drawLineBtn_clicked)
        self.textEditBtn.clicked.connect(self.on_textEditBtn_clicked)
        self.rectangleBtn.clicked.connect(self.on_rectangleBtn_clicked)
        self.drawRoundBtn.clicked.connect(self.on_drawRoundBtn_clicked)
        self.arrowBtn.clicked.connect(self.on_arrowBtn_clicked)
        self.mosaicBtn.clicked.connect(self.on_mosaicBtn_clicked)
        self.returneditBtn.clicked.connect(self.on_returneditBtn_clicked)

    @Slot()
    def cancelBtn_slot(self):
        if self.screen:
            self.screen.close()
            self.screen.Exit()

    @Slot()
    def saveBtn_slot(self):
        if self.screen:
            self.screen.savePixmap()
            self.cancelBtn_slot()

    @Slot()
    def finishBtn_slot(self):
        clipboard = QClipboard()
        if self.screen:
            # 解决保存图片 保留编辑
            pixmap = self.screen.labelimage.resultPixmap()
            # pixmap = self.screen.getGrabPixmap()   保存不会保留编辑
            clipboard.setImage(pixmap.toImage())
            self.cancelBtn_slot()

    def setScreenQuote(self, screen):
        self.screen = screen

    @Slot()
    def on_drawLineBtn_clicked(self):
        if self.screen:
            self.screen.drawline()

    @Slot()
    def on_textEditBtn_clicked(self):
        if self.screen:
            self.screen.textedit()

    @Slot()
    def on_rectangleBtn_clicked(self):
        if self.screen:
            self.screen.drawrectang()

    @Slot()
    def on_drawRoundBtn_clicked(self):
        if self.screen:
            self.screen.drawround()

    @Slot()
    def on_arrowBtn_clicked(self):
        if self.screen:
            self.screen.drawarrow()

    @Slot()
    def on_mosaicBtn_clicked(self):
        if self.screen:
            self.screen.drawmosaic()

    @Slot()
    def on_returneditBtn_clicked(self):
        if self.screen:
            self.screen.returnEdit()
