from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import  Qt, QRect

class AppIcon:
    @staticmethod
    def create_app_icon() -> QIcon:
        sizes = [16, 32, 48, 64, 128, 256]
        icon = QIcon()
        primary_color = "#2563eb"
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            center = size // 2
            
            circle_size = int(size * 0.2)
            circle_pos = center - circle_size // 2
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(primary_color))
            painter.drawEllipse(
                circle_pos,
                circle_pos,
                circle_size,
                circle_size
            )
            
            pen = QPen(QColor(primary_color))
            pen.setWidth(max(1, int(size * 0.02)))
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            orbit_size = int(size * 0.8)
            orbit_rect = QRect(
                center - orbit_size // 2,
                center - orbit_size // 4,
                orbit_size,
                orbit_size // 2
            )
            
            for angle in [0, 60, 120]:
                painter.save()
                painter.translate(center, center)
                painter.rotate(angle)
                painter.translate(-center, -center)
                painter.drawEllipse(orbit_rect)
                painter.restore()
            
            painter.end()
            icon.addPixmap(pixmap)
            
        return icon