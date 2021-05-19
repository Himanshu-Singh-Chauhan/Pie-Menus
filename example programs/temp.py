import sys
from PyQt5 import QtCore

from PyQt5.QtCore import QPoint, Qt, QVariantAnimation, QPointF
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._radius = 0

        self._animation = QVariantAnimation(startValue=0.0)
        self._animation.valueChanged.connect(self._handle_valueChanged)
        # self._animation.finished.connect(self._handle_finished)
        self._animation.setDuration(600)
        # self.pressed.connect(self._start_animation)
        self.released.connect(self._release)
    
    def _release(self):
        self._radius = 0
        self.update()

    def mousePressEvent(self, event) -> None:
        self.x = event.x()
        self.y = event.y()
        self._start_animation()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._radius = 0
        self.update()
        
        return super().mouseReleaseEvent(event)
        

    def _start_animation(self):
        self._animation.setDirection(QVariantAnimation.Forward)
        self._animation.setEndValue(self.width() / 1.0)
        self._animation.start()

    def _handle_valueChanged(self, value):
        self._radius = value
        self.update()

    def _handle_finished(self):
        self._animation.setDirection(QVariantAnimation.Backward)
        self._animation.start()
        # self._radius = 0
        # self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._radius:
            qp = QPainter(self)
            qp.setBrush(QColor(255, 255, 255, 20))
            qp.setPen(Qt.NoPen)
            # qp.drawEllipse(print(self.rect().center()), self._radius, self._radius)
            qp.drawEllipse(QPoint(self.x, self.y), self._radius, self._radius)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(Button("Start"))
    window.setStyleSheet(
        """
    QPushButton {
        color: #fff;
        background-color: #292E33;
        padding: 20px;
        font-size: 24pt;
        border-radius: 10px;
        border: none;
    }
    QPushButton:pressed {
        color: #F9E506;
    }"""
    )
    window.show()
    sys.exit(app.exec_())