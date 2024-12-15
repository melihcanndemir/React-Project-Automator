# modern_icons.py
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QPainterPath, QBrush
from PyQt5.QtCore import QSize, Qt, QPoint, QPointF, QRect
import math

class ModernIcons:
    """Pixmap tabanlı modern ikonlar"""
    
    @staticmethod
    def create_play_icon(color: str = "#2563eb") -> QIcon:
        """Play ikonu oluştur"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(color))
            
            # Play üçgeni çiz
            points = [
                QPoint(int(size * 0.25), int(size * 0.2)),
                QPoint(int(size * 0.25), int(size * 0.8)),
                QPoint(int(size * 0.75), int(size * 0.5))
            ]
            painter.setBrush(QColor(color))
            painter.drawPolygon(points)
            painter.end()
            
            icon.addPixmap(pixmap)
            
        return icon
    
    @staticmethod
    def create_stop_icon(color: str = "#2563eb") -> QIcon:
        """Stop ikonu oluştur"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(color))
            
            # Stop karesi çiz
            rect = QRect(
                int(size * 0.25),
                int(size * 0.25),
                int(size * 0.5),
                int(size * 0.5)
            )
            painter.setBrush(QColor(color))
            painter.drawRect(rect)
            painter.end()
            
            icon.addPixmap(pixmap)
            
        return icon
    
    @staticmethod
    def create_browser_icon(color: str = "#2563eb") -> QIcon:
        """Browser ikonu oluştur"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(color))
            
            # Dünya ikonu çiz
            margin = int(size * 0.1)
            diameter = size - 2 * margin
            painter.drawEllipse(margin, margin, diameter, diameter)
            painter.drawLine(margin, size // 2, size - margin, size // 2)
            
            # Dikey çizgi
            painter.drawLine(size // 2, margin, size // 2, size - margin)
            
            painter.end()
            
            icon.addPixmap(pixmap)
            
        return icon
    
    @staticmethod
    def create_app_icon() -> QIcon:
        """Uygulama ikonu oluştur"""
        sizes = [16, 32, 48, 64, 128, 256]
        icon = QIcon()
        primary_color = "#2563eb"  # React mavisi
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Merkez nokta
            center = size // 2
            
            # Merkez daire
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
            
            # Yörüngeler
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
    

    @staticmethod
    def create_save_icon(color: str = "#2563eb") -> QIcon:
        """Modern kaydet ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Kalem ayarları
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            # Dış çerçeve
            margin = int(size * 0.15)
            frame_size = size - 2 * margin
            painter.drawRoundedRect(
                margin, margin,
                frame_size, frame_size,
                int(size * 0.1), int(size * 0.1)
            )
            
            # İç dikdörtgen (disket kısmı)
            inner_margin = int(size * 0.3)
            painter.drawRect(
                inner_margin,
                margin,
                size - 2 * inner_margin,
                int(size * 0.25)
            )
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_folder_icon(color: str = "#2563eb") -> QIcon:
        """Modern klasör ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Kalem ayarları
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            painter.setPen(pen)
            
            # Ana klasör şekli
            margin = int(size * 0.15)
            painter.drawRoundedRect(
                margin,
                int(size * 0.3),
                size - 2 * margin,
                int(size * 0.55),
                int(size * 0.1),
                int(size * 0.1)
            )
            
            # Üst kısım
            painter.drawRoundedRect(
                margin,
                int(size * 0.2),
                int(size * 0.4),
                int(size * 0.15),
                int(size * 0.05),
                int(size * 0.05)
            )
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_new_file_icon(color: str = "#2563eb") -> QIcon:
        """Modern yeni dosya ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Kalem ayarları
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            painter.setPen(pen)
            
            # Kağıt şekli
            margin = int(size * 0.15)
            painter.drawRoundedRect(
                margin,
                margin,
                size - 2 * margin,
                size - 2 * margin,
                int(size * 0.1),
                int(size * 0.1)
            )
            
            # Artı işareti
            center = size // 2
            line_length = int(size * 0.3)
            
            # Yatay çizgi
            painter.drawLine(
                center - line_length // 2,
                center,
                center + line_length // 2,
                center
            )
            
            # Dikey çizgi
            painter.drawLine(
                center,
                center - line_length // 2,
                center,
                center + line_length // 2
            )
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_close_icon(color: str = "#2563eb") -> QIcon:
        """Modern kapat ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Kalem ayarları
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            # Çarpı işareti
            margin = int(size * 0.2)
            painter.drawLine(margin, margin, size - margin, size - margin)
            painter.drawLine(size - margin, margin, margin, size - margin)
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon
    
    @staticmethod
    def create_search_icon(color: str = "#2563eb") -> QIcon:
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            # Büyüteç çemberi
            diameter = int(size * 0.6)
            painter.drawEllipse(
                int(size * 0.15),
                int(size * 0.15),
                diameter,
                diameter
            )
            
            # Büyüteç sapı
            start_x = int(size * 0.65)
            start_y = int(size * 0.65)
            end_x = size - int(size * 0.2)
            end_y = size - int(size * 0.2)
            painter.drawLine(start_x, start_y, end_x, end_y)
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_trash_icon(color: str = "#2563eb") -> QIcon:
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            painter.setPen(pen)
            
            # Çöp kutusu gövdesi
            body_margin = int(size * 0.2)
            body_width = size - 2 * body_margin
            body_height = int(size * 0.6)
            painter.drawRect(
                body_margin,
                size - body_height - body_margin,
                body_width,
                body_height
            )
            
            # Kapak
            lid_width = int(size * 0.7)
            lid_height = int(size * 0.1)
            lid_x = (size - lid_width) // 2
            lid_y = size - body_height - body_margin - lid_height
            painter.drawRect(lid_x, lid_y, lid_width, lid_height)
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_expand_icon(color: str = "#2563eb") -> QIcon:
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            margin = int(size * 0.2)
            arrow_size = int(size * 0.25)
            
            # Sol üst ok
            painter.drawLine(margin, margin + arrow_size, margin, margin)
            painter.drawLine(margin, margin, margin + arrow_size, margin)
            
            # Sağ üst ok
            painter.drawLine(size - margin - arrow_size, margin, size - margin, margin)
            painter.drawLine(size - margin, margin, size - margin, margin + arrow_size)
            
            # Sol alt ok
            painter.drawLine(margin, size - margin - arrow_size, margin, size - margin)
            painter.drawLine(margin, size - margin, margin + arrow_size, size - margin)
            
            # Sağ alt ok
            painter.drawLine(size - margin - arrow_size, size - margin, size - margin, size - margin)
            painter.drawLine(size - margin, size - margin - arrow_size, size - margin, size - margin)
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon
    
    @staticmethod
    def create_rocket_icon(color: str = "#FFFFFF") -> QIcon:
        """Modern ve şık roket ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Temel kalem ve fırça ayarları
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.06)))
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(QColor(color))
            
            # Roket gövdesi - daha yumuşak eğriler
            center_x = size / 2
            path = QPainterPath()
            
            # Roket burnu
            path.moveTo(center_x, size * 0.15)  # Üst nokta
            path.cubicTo(
                size * 0.6, size * 0.2,  # Kontrol noktası 1
                size * 0.7, size * 0.4,  # Kontrol noktası 2
                size * 0.7, size * 0.65  # Bitiş noktası
            )
            
            # Alt kısım
            path.lineTo(size * 0.8, size * 0.85)  # Alt kanat
            path.lineTo(center_x, size * 0.75)    # Gövde altı
            path.lineTo(size * 0.2, size * 0.85)  # Diğer kanat
            path.lineTo(size * 0.3, size * 0.65)  # Gövde sol
            
            # Sol eğri
            path.cubicTo(
                size * 0.3, size * 0.4,  # Kontrol noktası 1
                size * 0.4, size * 0.2,  # Kontrol noktası 2
                center_x, size * 0.15    # Başlangıç noktasına dönüş
            )
            
            # Gövdeyi çiz
            painter.drawPath(path)
            
            # Pencere
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(color).darker(150))
            painter.drawEllipse(
                QPointF(center_x, size * 0.4),
                size * 0.08,
                size * 0.08
            )
            
            # Alev efekti
            flame_path = QPainterPath()
            flame_path.moveTo(center_x - size * 0.15, size * 0.75)
            flame_path.cubicTo(
                center_x - size * 0.1, size * 0.9,
                center_x + size * 0.1, size * 0.9,
                center_x + size * 0.15, size * 0.75
            )
            painter.setBrush(QColor(color).lighter(150))
            painter.drawPath(flame_path)
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_refresh_icon(color: str = "#FFFFFF") -> QIcon:
        """Modern ve net yenileme ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Temel kalem ayarları
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.12)))  # Daha kalın çizgi
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            # İç yarıçap ve merkez
            center = size / 2
            radius = size * 0.3
            
            # Ana daire yayı
            painter.drawArc(
                int(center - radius),
                int(center - radius),
                int(radius * 2),
                int(radius * 2),
                45 * 16,    # Başlangıç açısı
                270 * 16    # Yay uzunluğu
            )
            
            # Ok başı
            arrow_size = size * 0.25
            arrow_x = center + radius * math.cos(math.radians(45))
            arrow_y = center - radius * math.sin(math.radians(45))
            
            # Ok başını çiz
            painter.setBrush(QColor(color))
            arrow_path = QPainterPath()
            arrow_path.moveTo(arrow_x - arrow_size * 0.2, arrow_y + arrow_size * 0.2)
            arrow_path.lineTo(arrow_x + arrow_size * 0.4, arrow_y - arrow_size * 0.2)
            arrow_path.lineTo(arrow_x + arrow_size * 0.1, arrow_y - arrow_size * 0.6)
            painter.drawPath(arrow_path)
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon
    
    @staticmethod
    def create_git_init_icon(color: str = "#FFFFFF") -> QIcon:
        """Modern git init ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(QColor(color))
            
            # Git branch yapısı
            center_x = int(size / 2)
            center_y = int(size / 2)
            radius = int(size * 0.15)
            
            # Ana daire
            painter.drawEllipse(
                QPointF(center_x, center_y),
                radius, radius
            )
            
            # Dallar
            painter.setPen(pen)
            painter.drawLine(
                int(center_x), int(center_y - radius),
                int(center_x), int(size * 0.2)
            )
            painter.drawLine(
                int(center_x), int(center_y + radius),
                int(center_x), int(size * 0.8)
            )
            
            # Yan dallar
            painter.drawLine(
                int(center_x + radius), int(center_y),
                int(size * 0.8), int(center_y)
            )
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_git_commit_icon(color: str = "#FFFFFF") -> QIcon:
        """Modern git commit ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            painter.setPen(pen)
            
            # Merkez commit noktası
            center_x = int(size / 2)
            center_y = int(size / 2)
            radius = int(size * 0.2)
            
            painter.setBrush(QColor(color))
            painter.drawEllipse(
                QPointF(center_x, center_y),
                radius, radius
            )
            
            # Commit çizgileri
            line_length = int(size * 0.25)
            painter.drawLine(
                int(center_x - radius - line_length), int(center_y),
                int(center_x - radius), int(center_y)
            )
            painter.drawLine(
                int(center_x + radius), int(center_y),
                int(center_x + radius + line_length), int(center_y)
            )
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon

    @staticmethod
    def create_git_push_icon(color: str = "#FFFFFF") -> QIcon:
        """Modern git push ikonu"""
        sizes = [16, 24, 32, 48]
        icon = QIcon()
        
        for size in sizes:
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            pen = QPen(QColor(color))
            pen.setWidth(max(1, int(size * 0.08)))
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            # Ok gövdesi
            center_x = int(size / 2)
            arrow_width = int(size * 0.25)
            
            # Dikey çizgi
            painter.drawLine(
                center_x, int(size * 0.8),
                center_x, int(size * 0.3)
            )
            
            # Ok başı
            painter.setBrush(QColor(color))
            arrow_path = QPainterPath()
            arrow_path.moveTo(center_x, int(size * 0.2))  # Üst nokta
            arrow_path.lineTo(center_x - arrow_width, int(size * 0.4))  # Sol alt
            arrow_path.lineTo(center_x + arrow_width, int(size * 0.4))  # Sağ alt
            arrow_path.lineTo(center_x, int(size * 0.2))  # Tekrar üst
            painter.drawPath(arrow_path)
            
            # Alt çizgi
            painter.drawLine(
                center_x - arrow_width, int(size * 0.8),
                center_x + arrow_width, int(size * 0.8)
            )
            
            painter.end()
            icon.addPixmap(pixmap)
        
        return icon