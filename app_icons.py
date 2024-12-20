import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSvg import QSvgRenderer

class AppIcons:
    """Application icons handler"""
    
    # İkon dosyalarının bulunduğu dizin
    ICON_DIR = os.path.join(os.path.dirname(__file__), 'icons')
    
    @classmethod
    def load_icon(cls, name: str) -> QIcon:
        """Load icon from icons directory"""
        icon_path = os.path.join(cls.ICON_DIR, f"{name}.svg")
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icon not found: {icon_path}")
            
        icon = QIcon(icon_path)
        # Farklı boyutlarda otomatik ölçeklendirme
        for size in [16, 24, 32, 48, 64, 128]:
            icon.addPixmap(icon.pixmap(QSize(size, size)))
        return icon
    
    @classmethod
    def get_play_icon(cls) -> QIcon:
        return cls.load_icon('play')
    
    @classmethod
    def get_stop_icon(cls) -> QIcon:
        return cls.load_icon('stop')
    
    @classmethod
    def get_folder_icon(cls) -> QIcon:
        return cls.load_icon('folder')
    
    @classmethod
    def get_save_icon(cls) -> QIcon:
        return cls.load_icon('save')
    
    @classmethod
    def get_refresh_icon(cls) -> QIcon:
        return cls.load_icon('refresh')
    
    @classmethod
    def get_git_init_icon(cls) -> QIcon:
        return cls.load_icon('git-init')
    
    @classmethod
    def get_git_commit_icon(cls) -> QIcon:
        return cls.load_icon('git-commit')
    
    @classmethod
    def get_git_push_icon(cls) -> QIcon:
        return cls.load_icon('git-push')

    
    @classmethod
    def get_settings_icon(cls) -> QIcon:
        return cls.load_icon('settings')
    
    @classmethod
    def get_search_icon(cls) -> QIcon:
        return cls.load_icon('search')
    
    @classmethod    
    def get_app_icon(cls) -> QIcon:
        return cls.load_icon('app-icon')
    
    @classmethod    
    def get_browser_icon(cls) -> QIcon:
        return cls.load_icon('globe')
    
    @classmethod    
    def get_terminal_icon(cls) -> QIcon:
        return cls.load_icon('terminal')
    
    @classmethod
    def get_trash_icon(cls) -> QIcon:
        return cls.load_icon("trash")
    
    @classmethod
    def get_expand_icon(cls) -> QIcon:
        return cls.load_icon("maximize")
    
    @classmethod
    def get_clean_icon(cls) -> QIcon:
        return cls.load_icon("clean")
    
    @classmethod
    def get_add_icon(cls) -> QIcon:
        return cls.load_icon("add")
    
    @classmethod
    def get_theme_icon(cls) -> QIcon:
        return cls.load_icon("theme")
    
    @classmethod
    def get_light_icon(cls) -> QIcon:
        return cls.load_icon("light")
    
    @classmethod
    def get_dark_icon(cls) -> QIcon:
        return cls.load_icon("theme")
    
    @classmethod
    def get_about_icon(cls) -> QIcon:
        return cls.load_icon("about")
    
    @classmethod    
    def get_exit_icon(cls) -> QIcon:
        return cls.load_icon('exit')

# Kullanım örneği:
"""
from app_icons import AppIcons

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(AppIcons.get_app_icon())
        
        # Toolbar ikonları
        self.play_button.setIcon(AppIcons.get_play_icon())
        self.folder_button.setIcon(AppIcons.get_folder_icon())
"""