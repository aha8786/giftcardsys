import os

from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication, QIcon, QPixmap


class FloatingReturnButton(QWidget):
    """항상 화면 위에 떠 있는 복귀 버튼 창."""

    restore_requested = Signal()

    _LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "img", "logo.png")
    _SIZE = 60

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
        )
        self.setFixedSize(self._SIZE, self._SIZE)

        btn = QPushButton(self)
        btn.setFixedSize(self._SIZE, self._SIZE)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        pix = QPixmap(self._LOGO_PATH)
        if not pix.isNull():
            btn.setIcon(QIcon(pix))
            btn.setIconSize(btn.size())
            btn.setText("")
        else:
            btn.setText("복귀")

        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 8px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        btn.clicked.connect(self.restore_requested)

        self._reposition()

    def _reposition(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        margin = 20
        self.move(
            screen.right() - self.width() - margin,
            screen.bottom() - self.height() - margin,
        )
